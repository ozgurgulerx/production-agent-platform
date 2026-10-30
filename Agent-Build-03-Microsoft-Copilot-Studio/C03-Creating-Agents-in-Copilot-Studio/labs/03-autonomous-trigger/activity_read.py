"""Read the last day's event-trigger runs of the ticket agent from Dataverse ConversationTranscript rows.

Proves: autonomous runs are transcripts like any conversation (G4): the trigger payload is the first activity, the
outcome sits in SessionInfo, and the default retention is 30 days. Column names marked verify against your org.
"""
import json
from datetime import datetime, timedelta, timezone

from _common import dataverse, need, show
import os

need("ENVIRONMENT_URL", "AGENT_ID")
since = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
bot_id = os.environ["AGENT_ID"]
# conversationtranscripts: _bot_conversationtranscriptid_value links to the bot; `content` holds the activity JSON (G4)  # verify
path = ("conversationtranscripts?$select=conversationtranscriptid,name,conversationstarttime,content"
        f"&$filter=_bot_conversationtranscriptid_value eq {bot_id} and conversationstarttime ge {since}"
        "&$orderby=conversationstarttime desc&$top=10")
r = dataverse("GET", path)
r.raise_for_status()
rows = r.json().get("value", [])
print(f"{len(rows)} transcript(s) since {since}")
for row in rows:
    content = json.loads(row.get("content") or "{}")
    activities = content.get("activities", [])
    first = next((a for a in activities if a.get("type") == "message"), {})
    session = next((a.get("value") for a in activities if a.get("valueType") == "SessionInfo"), {})  # verify valueType
    trigger = next((a for a in activities if a.get("valueType", "").endswith("TriggerEvent")), None)  # verify
    show(row["conversationstarttime"], {"outcome": session.get("outcome"), "trigger": bool(trigger),
                                        "first": (first.get("text") or "")[:80], "activities": len(activities)})
print("\nIf outcome is missing: the session is still running or SessionInfo has a different valueType in your org.")
