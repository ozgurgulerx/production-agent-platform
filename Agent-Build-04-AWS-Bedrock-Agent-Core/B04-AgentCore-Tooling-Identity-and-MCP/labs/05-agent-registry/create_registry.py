"""Create `ticket-registry` (IAM-authorised, manual approval) and write TICKET_REGISTRY_ID.

Proves: a registry is an authorised catalogue with an approval gate, separate from the Gateway.
Run: python create_registry.py [--cleanup]
"""

import argparse
import time

from _common import control, need, write_env


def main(cleanup: bool) -> None:
    cp = control()
    if cleanup:
        rid = need("TICKET_REGISTRY_ID")
        for rec in cp.list_registry_records(registryId=rid).get("registryRecords", []):
            cp.delete_registry_record(registryId=rid, recordId=rec["recordId"])          # verify: key name
        cp.delete_registry(registryId=rid); print("deleted", rid); return
    r = cp.create_registry(name="ticket-registry", description="Ticket tools and agents for the UK card team",
                           authorizerType="AWS_IAM", approvalConfiguration={"autoApproval": False})
    rid = r["registryArn"].split("/")[-1]
    while (st := cp.get_registry(registryId=rid)["status"]) in ("CREATING",):
        print("  status", st); time.sleep(5)
    print("status", st, r["registryArn"])
    write_env("TICKET_REGISTRY_ID", rid)
    write_env("TICKET_REGISTRY_ARN", r["registryArn"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--cleanup", action="store_true"); main(p.parse_args().cleanup)
