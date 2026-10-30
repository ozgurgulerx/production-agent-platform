"""Ask the ticket agent the three canonical questions through Direct-to-Engine and print text plus citations.

Proves: a Standard-harness agent is callable from code with a delegated user token (no Direct Line secret);
grounded answers carry citations; the Peru question is refused when "Allow ungrounded responses" is off (B1).
Run it once against the connector-source agent and once against the uploaded-files copy (--agent <schema name>).
"""

import argparse
import asyncio
import json
import os

from microsoft_agents.copilotstudio.client import (
    AgentType,
    ConnectionSettings,
    CopilotClient,
    PowerPlatformCloud,
)

from _common import (
    AGENT_SCHEMA_NAME,
    D2E_SCOPES,
    ENVIRONMENT_ID,
    POLICY_QUESTIONS,
    device_code_token,
    need,
)


def client(agent: str) -> CopilotClient:
    cloud = PowerPlatformCloud(os.environ.get("POWER_PLATFORM_CLOUD", "Prod"))
    settings = ConnectionSettings(
        environment_id=ENVIRONMENT_ID,
        agent_identifier=agent,
        cloud=cloud,
        copilot_agent_type=AgentType.PUBLISHED,
    )
    token = device_code_token(
        D2E_SCOPES
    )  # delegated CopilotStudio.Copilots.Invoke (C8); verify scope string
    return CopilotClient(settings, token)


def citations(activity) -> list[str]:
    """Citations come back on the message activity; the exact carrier differs by channel. Print raw the first time."""
    out = []
    for e in (
        activity.entities or []
    ):  # verify: 'citation' entities with 'citation' list
        d = e.model_dump(exclude_none=True) if hasattr(e, "model_dump") else dict(e)
        if "citation" in d:
            for c in d["citation"]:
                appearance = c.get("appearance", {})
                out.append(
                    appearance.get("url")
                    or appearance.get("name")
                    or json.dumps(c)[:80]
                )
    for a in activity.attachments or []:  # verify: some channels attach a citation card
        if a.content_type and "citation" in str(a.content_type).lower():
            out.append(str(a.name or a.content_type))
    return out


async def ask(agent: str, raw: bool) -> None:
    c = client(agent)
    async for a in c.start_conversation():
        if a.text:
            print(f"[start] {a.text[:120]}")
    for q in POLICY_QUESTIONS:
        print(f"\nQ: {q}")
        async for a in c.ask_question(q):
            if a.type != "message" or not a.text:
                continue
            print(f"A: {a.text.strip()[:600]}")
            cites = citations(a)
            print(f"   citations: {cites or 'none'}")
            if raw:
                print(
                    "   raw entities:",
                    json.dumps(
                        [e.model_dump(exclude_none=True) for e in (a.entities or [])]
                    )[:800],
                )
    print(
        "\nexpected: Q1 and Q2 cite card/refund policy; Q3 is a no-knowledge refusal (ungrounded responses off)."
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--agent",
        default=AGENT_SCHEMA_NAME,
        help="agent schema name; defaults to AGENT_SCHEMA_NAME",
    )
    ap.add_argument(
        "--raw",
        action="store_true",
        help="print raw entities to learn the citation shape",
    )
    args = ap.parse_args()
    need("ENVIRONMENT_ID")
    if not args.agent:
        raise SystemExit("set AGENT_SCHEMA_NAME in .env or pass --agent")
    asyncio.run(ask(args.agent, args.raw))
