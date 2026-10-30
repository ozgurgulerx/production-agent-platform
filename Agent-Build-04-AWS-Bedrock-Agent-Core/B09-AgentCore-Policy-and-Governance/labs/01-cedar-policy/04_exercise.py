"""Proves: in LOG_ONLY every call still reaches the target, but the engine records what it would have decided.
Three calls through the gateway with a Cognito bearer: get_ticket (permit), issue_refund 100 (permit),
issue_refund 900 (would deny). Then the decision log is read.
Log group name is not verified; override with --log-group <name>."""
import sys
import time

from _common import GATEWAY_ID, call_tool, cognito_token, need, session, show

need("TICKET_GATEWAY_URL", "POLICY_ENGINE_ID")
DEFAULT_LOG_GROUP = f"/aws/bedrock-agentcore/gateways/{GATEWAY_ID}/policy"   # verify


def exercise(token: str) -> None:
    show("get_ticket T-2041", call_tool(token, "get_ticket", {"ticket_id": "T-2041"}))
    show("issue_refund 100", call_tool(token, "issue_refund",
                                       {"ticket_id": "T-2041", "amount_gbp": 100, "reason": "duplicate charge"}))
    show("issue_refund 900 (over cap)", call_tool(token, "issue_refund",
                                                  {"ticket_id": "T-2041", "amount_gbp": 900, "reason": "customer upset"}))


def read_decisions(log_group: str, since_s: int = 300) -> None:
    logs = session().client("logs")
    try:
        r = logs.filter_log_events(logGroupName=log_group, startTime=int((time.time() - since_s) * 1000), limit=20)
    except logs.exceptions.ResourceNotFoundException:
        print(f"\nno log group {log_group}; find the decision log group in the console and pass --log-group")
        return
    print(f"\ndecisions in {log_group}:")
    for e in r.get("events", []):
        print("  ", e["message"][:200])


def main() -> None:
    token = cognito_token()
    exercise(token)
    lg = sys.argv[sys.argv.index("--log-group") + 1] if "--log-group" in sys.argv else DEFAULT_LOG_GROUP
    time.sleep(10)
    read_decisions(lg)
    print("\nexpected in LOG_ONLY: all three ok on the wire; the 900 call logged as would-deny.")


if __name__ == "__main__":
    main()
