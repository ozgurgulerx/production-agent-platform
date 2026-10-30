"""One invocation surface. Calls whichever B03 agents exist (Runtime from 02, Harness from 01)
through the data plane and shows the four controls: runtimeSessionId (server-side state per
microVM), a second turn on the same session, a fresh session, and `qualifier` (DEFAULT or a
named endpoint). Nothing here depends on how the agent was built.
"""
from __future__ import annotations

import json
import os

from _common import data, new_session_id, read_body

dp = data()
runtime_arn = os.environ.get("TICKET_AGENT_RUNTIME_ARN")
harness_arn = os.environ.get("TICKET_AGENT_HARNESS_ARN")


def invoke_runtime(arn: str, sid: str, prompt: str, qualifier: str = "DEFAULT") -> str:
    resp = dp.invoke_agent_runtime(
        agentRuntimeArn=arn,
        runtimeSessionId=sid,
        qualifier=qualifier,
        contentType="application/json",
        accept="application/json, text/event-stream",
        payload=json.dumps({"prompt": prompt}).encode(),
    )
    return read_body(resp)


if runtime_arn:
    print(f"== Runtime {runtime_arn}")
    sid = new_session_id()
    print("turn 1:", invoke_runtime(runtime_arn, sid, "My name is Ayşe. What is ticket T-1001 about?"))
    print("turn 2 (same session, state kept in the microVM):", invoke_runtime(runtime_arn, sid, "What was my name?"))
    print("new session (no memory):", invoke_runtime(runtime_arn, new_session_id(), "What was my name?"))
    for q in ("DEFAULT", "stable"):  # `stable` exists only after 05-versions-and-endpoints.py --keep
        try:
            print(f"qualifier={q}:", invoke_runtime(runtime_arn, new_session_id(), "List open tickets.", q)[:200])
        except Exception as e:  # noqa: BLE001
            print(f"qualifier={q}: {type(e).__name__}: {e}")
    dp.stop_runtime_session(agentRuntimeArn=runtime_arn, runtimeSessionId=sid)
    print("session stopped explicitly (otherwise idle timeout 15 min, max 8 h)")
else:
    print("no TICKET_AGENT_RUNTIME_ARN in .env: run 02-runtime-code-deploy.py --keep")

if harness_arn:
    print(f"\n== Harness {harness_arn}")
    sid = new_session_id()
    text = []
    for event in dp.invoke_harness(harnessArn=harness_arn, runtimeSessionId=sid,
                                   messages=[{"role": "user", "content": [{"text": "Which policies do you know?"}]}])["stream"]:
        if "contentBlockDelta" in event and "text" in event["contentBlockDelta"]["delta"]:
            text.append(event["contentBlockDelta"]["delta"]["text"])
        elif "metadata" in event:
            print("usage:", event["metadata"].get("usage"))
    print("".join(text))
else:
    print("\nno TICKET_AGENT_HARNESS_ARN in .env: run 01-harness-sdk.py --keep")
