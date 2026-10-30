"""Weighted routing between two HTTP targets (e.g. ticket-agent v1 and v2 pinned to two Runtime endpoints): a Gateway
rule with routeToTarget.weightedRoute, 90/10, fallback on connection errors. This is the canary mechanism; Runtime
endpoints themselves have no traffic split.

Shape from CreateGatewayRule (botocore 1.43.118); not run. Run: python gateway_rule_weighted.py [--cleanup]   # verify
"""

import argparse

from _common import control, need, write_env


def main(cleanup: bool) -> None:
    cp, gid = control(), need("TICKET_GATEWAY_ID")
    if cleanup:
        cp.delete_gateway_rule(gatewayIdentifier=gid, ruleId=need("TICKET_CANARY_RULE_ID")); print("deleted"); return
    r = cp.create_gateway_rule(
        gatewayIdentifier=gid, priority=10, description="canary: 90% v1, 10% v2",
        conditions=[{"matchPaths": {"anyOf": ["/ticket-agent/invocations"]}}],                           # verify path form
        actions=[{"routeToTarget": {"weightedRoute": {"trafficSplit": [
            {"name": "v1", "targetName": "ticket-agent", "weight": 90,
             "fallback": {"triggerOn": {"errors": ["CONNECTION_ERROR", "FIRST_BYTE_TIMEOUT"]}, "firstByteTimeoutMilliseconds": 5000,
                          "targetFallback": [{"targetName": "ticket-agent-v2"}]}},
            {"name": "v2", "targetName": "ticket-agent-v2", "weight": 10},
        ]}}}],
    )
    print("rule", r["ruleId"], r.get("status")); write_env("TICKET_CANARY_RULE_ID", r["ruleId"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--cleanup", action="store_true"); main(p.parse_args().cleanup)
