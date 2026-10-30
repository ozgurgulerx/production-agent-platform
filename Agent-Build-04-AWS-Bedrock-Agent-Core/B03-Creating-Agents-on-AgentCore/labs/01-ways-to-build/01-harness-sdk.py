"""Way 1: an AgentCore Harness, the managed agent loop. Creates the ticket harness with boto3
(the twin of `agentcore add harness` + `agentcore deploy`), invokes it with the Converse-shaped
InvokeHarness stream, and answers inline-function tool calls from this process.
Proves: the definition (model, system prompt, tools) lives in AgentCore, the loop runs in
AgentCore, and inline functions are return-of-control: the harness asks, you execute, you reply.
Usage: python 01-harness-sdk.py [--keep] [--cleanup]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "agent"))
from _common import MODEL_ID, ROLE_ARN, SUPPORT_INSTRUCTIONS, control, data, new_session_id, require, write_env  # noqa: E402
from main import get_policy, get_ticket, issue_refund, list_tickets  # noqa: E402

NAME = "ticket_agent_harness"
LOCAL_TOOLS = {"get_ticket": get_ticket, "list_tickets": list_tickets, "get_policy": get_policy, "issue_refund": issue_refund}
require("AGENTCORE_RUNTIME_ROLE_ARN")


def inline(name: str, description: str, props: dict, required: list[str]) -> dict:
    return {"type": "inline_function", "name": name, "config": {"inlineFunction": {
        "description": description,
        "inputSchema": {"json": {"type": "object", "properties": props, "required": required}},  # verify: inputSchema wrapper key
    }}}


TOOLS = [
    inline("get_ticket", "Return one support ticket by id", {"ticket_id": {"type": "string"}}, ["ticket_id"]),
    inline("list_tickets", "List tickets by status", {"status": {"type": "string"}}, []),
    inline("get_policy", "Return a named policy text", {"name": {"type": "string"}}, ["name"]),
    inline("issue_refund", "Issue a refund; >250 GBP is refused", {"ticket_id": {"type": "string"}, "amount_gbp": {"type": "number"}}, ["ticket_id", "amount_gbp"]),
]


def find_harness(cp):
    for h in cp.list_harnesses(maxResults=100).get("harnesses", []):
        if h["harnessName"] == NAME:
            return cp.get_harness(harnessId=h["harnessId"])["harness"]  # verify: get_harness key name
    return None


def create(cp) -> dict:
    resp = cp.create_harness(
        harnessName=NAME,
        executionRoleArn=ROLE_ARN,
        model={"bedrockModelConfig": {"modelId": MODEL_ID, "maxTokens": 600}},
        systemPrompt=[{"text": SUPPORT_INSTRUCTIONS}],
        tools=TOOLS,
        maxIterations=8,
    )
    hid = resp["harness"]["harnessId"] if "harness" in resp else resp["harnessId"]  # verify
    while True:
        h = cp.get_harness(harnessId=hid)["harness"]
        print(f"  status={h['status']}")
        if h["status"] in ("READY", "ACTIVE"):
            return h
        if "FAIL" in h["status"]:
            raise SystemExit(h.get("failureReason"))
        time.sleep(10)


def run_turn(dp, arn: str, sid: str, messages: list[dict]) -> tuple[str, list[dict]]:
    """Stream one InvokeHarness; collect text and any toolUse blocks (Converse stream shape)."""
    text, tool_uses, current = [], [], {}
    for event in dp.invoke_harness(harnessArn=arn, runtimeSessionId=sid, messages=messages)["stream"]:
        if "contentBlockStart" in event and "toolUse" in event["contentBlockStart"].get("start", {}):
            current = dict(event["contentBlockStart"]["start"]["toolUse"], input="")
        elif "contentBlockDelta" in event:
            d = event["contentBlockDelta"]["delta"]
            if "text" in d:
                text.append(d["text"])
            if "toolUse" in d:
                current["input"] += d["toolUse"].get("input", "")
        elif "contentBlockStop" in event and current:
            tool_uses.append(current)
            current = {}
        elif "hookEvent" in event:
            print("  hook:", event["hookEvent"])
    return "".join(text), tool_uses


def chat(dp, arn: str, sid: str, prompt: str) -> str:
    messages = [{"role": "user", "content": [{"text": prompt}]}]
    for _ in range(6):
        answer, tool_uses = run_turn(dp, arn, sid, messages)
        if not tool_uses:
            return answer
        results = []
        for tu in tool_uses:
            args = json.loads(tu["input"] or "{}")
            out = LOCAL_TOOLS[tu["name"]](**args)
            print(f"  tool {tu['name']}({args}) -> {out}")
            results.append({"toolResult": {"toolUseId": tu["toolUseId"], "content": [{"json": out}]}})
        messages = [{"role": "assistant", "content": [{"toolUse": tu} for tu in tool_uses]}, {"role": "user", "content": results}]
    return answer


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--cleanup", action="store_true")
    args = ap.parse_args()
    cp, dp = control(), data()
    h = find_harness(cp)
    if args.cleanup:
        if h:
            cp.delete_harness(harnessId=h["harnessId"])
            print("[cleanup] harness deleted")
        raise SystemExit(0)
    h = h or create(cp)
    write_env("TICKET_AGENT_HARNESS_ARN", h["arn"])
    sid = new_session_id()
    for p in ["What is ticket T-1003 about?", "Refund the full amount on it."]:
        print(f"\n> {p}\n{chat(dp, h['arn'], sid, p)}")
    if not args.keep:
        cp.delete_harness(harnessId=h["harnessId"])
