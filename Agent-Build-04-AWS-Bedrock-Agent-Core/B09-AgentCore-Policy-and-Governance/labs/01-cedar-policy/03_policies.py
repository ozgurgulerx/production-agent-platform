"""Proves: one Cedar statement per policy; creation is validated (FAIL_ON_ANY_FINDINGS); each policy carries its own
enforcementMode. Creates read_all (ACTIVE) and refund_cap (ACTIVE) from policies/*.cedar, then lists the engine."""
import sys
import time
from pathlib import Path

from _common import ENGINE_ID, HERE, control, gateway_arn, need

need("POLICY_ENGINE_ID", "TICKET_GATEWAY_ID")
POLICIES = {"read-all": "read_all.cedar", "refund-cap-250": "refund_cap.cedar"}


def statement(name: str, arn: str) -> str:
    return (HERE / "policies" / name).read_text().replace("<GATEWAY_ARN>", arn)


def main() -> None:
    c = control()
    if "--cleanup" in sys.argv:
        for p in c.list_policies(policyEngineId=ENGINE_ID).get("policies", []):
            c.delete_policy(policyEngineId=ENGINE_ID, policyId=p["policyId"])
            print("deleted", p["name"])
        return
    arn = gateway_arn()
    have = {p["name"]: p for p in c.list_policies(policyEngineId=ENGINE_ID).get("policies", [])}
    for name, file in POLICIES.items():
        if name in have:
            print("exists", name, have[name]["status"])
            continue
        r = c.create_policy(policyEngineId=ENGINE_ID, name=name,
                            definition={"cedar": {"statement": statement(file, arn)}},
                            validationMode="FAIL_ON_ANY_FINDINGS", enforcementMode="ACTIVE")
        while r.get("status") in ("CREATING", None):
            time.sleep(3)
            r = c.get_policy(policyEngineId=ENGINE_ID, policyId=r["policyId"])
        print("created", name, r["status"], r.get("statusReasons"))
    print("\nengine", ENGINE_ID)
    for p in c.list_policies(policyEngineId=ENGINE_ID).get("policies", []):
        print(f"  {p['name']:<18} {p.get('enforcementMode', ''):<9} {p['status']}")


if __name__ == "__main__":
    main()
