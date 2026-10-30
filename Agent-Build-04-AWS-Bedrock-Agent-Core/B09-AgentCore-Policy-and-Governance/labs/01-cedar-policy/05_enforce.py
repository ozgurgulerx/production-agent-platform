"""Proves: flipping the gateway to ENFORCE turns the logged would-deny into a refusal; the error body names the policy
when exceptionLevel is DEBUG. --cleanup detaches the engine, deletes the policies and the engine (reverse order)."""
import subprocess
import sys
from pathlib import Path

from _common import call_tool, cognito_token, need, show

need("TICKET_GATEWAY_URL", "POLICY_ENGINE_ARN")
HERE = Path(__file__).resolve().parent
PY = sys.executable


def main() -> None:
    if "--cleanup" in sys.argv:
        for script, args in (("02_attach_log_only.py", ["--cleanup"]), ("03_policies.py", ["--cleanup"]),
                             ("01_create_engine.py", ["--cleanup"])):
            subprocess.run([PY, str(HERE / script), *args], check=False)
        return
    subprocess.run([PY, str(HERE / "02_attach_log_only.py"), "--mode", "ENFORCE"], check=True)
    token = cognito_token()
    show("get_ticket T-2041", call_tool(token, "get_ticket", {"ticket_id": "T-2041"}))
    show("issue_refund 100", call_tool(token, "issue_refund",
                                       {"ticket_id": "T-2041", "amount_gbp": 100, "reason": "duplicate charge"}))
    denied = call_tool(token, "issue_refund", {"ticket_id": "T-2041", "amount_gbp": 900, "reason": "customer upset"})
    show("issue_refund 900 (over cap)", denied)
    print("\nexpected: first two ok, third DENIED; the error body should reference refund-cap-250 (DEBUG level).")
    print("not permitted at all (no policy): a tool outside TicketTools is also denied -> deny by default.")


if __name__ == "__main__":
    main()
