"""Proves: a policy engine is a plain container (name, optional CMK) and exists independently of any gateway.
Writes POLICY_ENGINE_ID to the track-root .env. --cleanup deletes it."""
import sys
import time

from _common import ENGINE_ID, control, write_env

NAME = "ticket-policy-engine"


def main() -> None:
    c = control()
    if "--cleanup" in sys.argv:
        if ENGINE_ID:
            c.delete_policy_engine(policyEngineId=ENGINE_ID)
            print("deleted", ENGINE_ID)
        return
    existing = [e for e in c.list_policy_engines().get("policyEngines", []) if e.get("name") == NAME]
    if existing:
        eng = c.get_policy_engine(policyEngineId=existing[0]["policyEngineId"])
    else:
        eng = c.create_policy_engine(name=NAME, description="Cedar rules for TicketTools", tags={"owner": "b09"})
        while eng.get("status") not in ("ACTIVE", "FAILED"):
            time.sleep(5)
            eng = c.get_policy_engine(policyEngineId=eng["policyEngineId"])
    print("engine:", eng["policyEngineId"], eng["status"], eng["policyEngineArn"])
    write_env("POLICY_ENGINE_ID", eng["policyEngineId"])
    write_env("POLICY_ENGINE_ARN", eng["policyEngineArn"])


if __name__ == "__main__":
    main()
