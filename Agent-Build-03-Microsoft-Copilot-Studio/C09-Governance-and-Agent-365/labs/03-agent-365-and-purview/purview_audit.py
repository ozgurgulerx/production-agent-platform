"""Pull the last day of Copilot Studio audit events from Purview through Microsoft Graph (F6, F7).

Proves: BotPublish (a maker action) and CopilotInteraction (a user turn) land in the same unified audit log,
so the publish that introduced a tool and the first refund attempt through it are one query apart.
Read-only; nothing to revert. Needs AuditLog.Read.All (delegated) and a Purview-licensed admin.
"""
import argparse
import time
from datetime import datetime, timedelta, timezone

from _common import graph, show

OPERATIONS = ["BotPublish", "BotCreate", "BotShare", "BotAuthUpdate", "CopilotInteraction"]
QUERY_PATH = "/security/auditLog/queries"   # Graph audit log query API (beta on some tenants: /beta/...); verify


def run_query(hours: int) -> list[dict]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    body = {"displayName": f"copilot-studio-last-{hours}h", "filterStartDateTime": start.isoformat(),
            "filterEndDateTime": end.isoformat(), "operationFilters": OPERATIONS,
            "serviceFilters": ["PowerPlatform", "CopilotStudio", "Copilot"]}   # verify service names
    with graph() as c:
        c.base_url = "https://graph.microsoft.com/beta"   # verify: v1.0 vs beta for auditLog queries
        r = c.post(QUERY_PATH, json=body)
        q = show("create audit query", r)
        qid = q.get("id")
        if not qid:
            return []
        while True:
            s = c.get(f"{QUERY_PATH}/{qid}").json()
            if s.get("status") in ("succeeded", "failed", "cancelled"):
                break
            print("  status:", s.get("status")); time.sleep(10)
        recs = c.get(f"{QUERY_PATH}/{qid}/records").json()
    return recs.get("value", [])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--hours", type=int, default=24)
    rows = run_query(ap.parse_args().hours)
    print(f"\n{len(rows)} records")
    for r in rows[:50]:
        audit = r.get("auditData", {})
        print(f"- {r.get('createdDateTime')}  {r.get('operation'):<20} {r.get('userPrincipalName','?'):<30} "
              f"{str(audit.get('BotName') or audit.get('AppIdentity') or '')[:40]}")
    print("\nexpected: your BotPublish from C03 lab 01 and CopilotInteraction rows for each test turn; "
          "transcript text is only in DSPM for AI, not here (F6).")
