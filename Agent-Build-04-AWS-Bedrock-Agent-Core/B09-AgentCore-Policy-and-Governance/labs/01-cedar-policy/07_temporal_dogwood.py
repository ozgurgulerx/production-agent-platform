"""Proves (once the syntax is verified): a session-aware Dogwood policy caps a user at N refunds per 24 hours.
Research (2026-10-25): Dogwood = temporal policies, max 20 per engine, 24-hour window (F1). The statement grammar was
not fetched, so this script only submits a candidate and prints the validation outcome. # verify"""
import sys

from _common import ENGINE_ID, control, gateway_arn, need

need("POLICY_ENGINE_ID", "TICKET_GATEWAY_ID")

CANDIDATE = """
// # verify: Dogwood grammar. Intended meaning: at most 3 issue_refund calls per principal per 24h.
limit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"TicketTools___issue_refund",
  resource == AgentCore::Gateway::"<GATEWAY_ARN>"
) to 3 per 24h;
"""


def main() -> None:
    c = control()
    stmt = CANDIDATE.replace("<GATEWAY_ARN>", gateway_arn())
    if "--submit" not in sys.argv:
        print(stmt)
        print("dry run. Pass --submit to send it; expect INVALID until the grammar is corrected from the docs.")
        return
    try:
        r = c.create_policy(policyEngineId=ENGINE_ID, name="refund-rate-3-per-day",
                            definition={"policy": {"statement": stmt}},       # 'policy' slot, not 'cedar'  # verify
                            validationMode="FAIL_ON_ANY_FINDINGS", enforcementMode="LOG_ONLY")
        print("created", r["policyId"], r["status"], r.get("statusReasons"))
    except c.exceptions.ValidationException as e:
        print("validation:", e)


if __name__ == "__main__":
    main()
