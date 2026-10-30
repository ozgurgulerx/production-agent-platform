"""Read the last N hours of ConversationTranscript rows from Dataverse and print outcome and tool calls per conversation.

Proves: the transcript is the conversation-level record (reading map G4): Bot Framework activity JSON with
SessionInfo outcomes and dialog trace; 30-day default retention; test-pane chats carry isDesignMode.
Column names follow the Learn page; the `content` JSON layout is marked verify.
"""
import argparse
import json
from datetime import datetime, timedelta, timezone

from _common import AGENT_ID, dataverse, need

need("ENVIRONMENT_URL")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=int, default=24)
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args()
    since = (datetime.now(timezone.utc) - timedelta(hours=args.hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
    flt = f"createdon ge {since}"
    if AGENT_ID:
        flt += f" and _bot_conversationtranscriptid_value eq {AGENT_ID}"      # verify: lookup column name to the bot
    rows = dataverse("GET", f"/api/data/v9.2/conversationtranscripts?$select=conversationtranscriptid,name,createdon,content"
                            f"&$filter={flt}&$orderby=createdon desc&$top={args.top}").get("value", [])
    print(f"{len(rows)} transcripts since {since}\n")
    for row in rows:
        try:
            activities = json.loads(row.get("content") or "{}").get("activities", [])    # verify: content layout
        except json.JSONDecodeError:
            activities = []
        outcome, tools, design = "?", [], False
        for a in activities:
            v = a.get("value") or {}
            if a.get("valueType") == "SessionInfo" or "outcome" in v:
                outcome = v.get("outcome", outcome)
            if a.get("valueType") == "DialogTraceDetail" or a.get("type") == "trace":
                design = design or bool(v.get("isDesignMode"))
                for step in v.get("actions", []) if isinstance(v, dict) else []:
                    if step.get("actionType") in ("tool", "connector", "mcp"):
                        tools.append(step.get("name", "?"))
        print(f"{row['createdon'][:19]}  {row['conversationtranscriptid'][:8]}  outcome={outcome:<10} "
              f"design={design}  tools={tools or '-'}  activities={len(activities)}")


if __name__ == "__main__":
    main()
