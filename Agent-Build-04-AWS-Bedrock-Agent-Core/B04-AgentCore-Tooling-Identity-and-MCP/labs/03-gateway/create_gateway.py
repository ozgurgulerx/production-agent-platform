"""Create `ticket-gateway`: MCP protocol, semantic search on, Cognito JWT inbound, the lab role outbound.
Writes TICKET_GATEWAY_ID and TICKET_GATEWAY_URL.

Proves: a Gateway is one MCP server with one inbound check; search must be chosen at creation.
Run: python create_gateway.py [--cleanup]
"""

import argparse
import time

from _common import control, need, write_env


def main(cleanup: bool) -> None:
    cp = control()
    if cleanup:
        gid = need("TICKET_GATEWAY_ID")
        for t in cp.list_gateway_targets(gatewayIdentifier=gid).get("items", []):
            cp.delete_gateway_target(gatewayIdentifier=gid, targetId=t["targetId"])
        cp.delete_gateway(gatewayIdentifier=gid); print("deleted", gid); return
    r = cp.create_gateway(
        name="ticket-gateway",
        description="Ticket tools for the UK card team",
        roleArn=need("AGENTCORE_GATEWAY_ROLE_ARN"),
        protocolType="MCP",
        protocolConfiguration={"mcp": {"searchType": "SEMANTIC",                                   # creation-time only
                                       "instructions": "Tools for reading tickets and issuing refunds.",
                                       "streamingConfiguration": {"enableResponseStreaming": True}}},
        authorizerType="CUSTOM_JWT",
        authorizerConfiguration={"customJWTAuthorizer": {"discoveryUrl": need("COGNITO_DISCOVERY_URL"),
                                                         "allowedClients": [need("COGNITO_CLIENT_ID")]}},
        exceptionLevel="DEBUG",                                                                    # verbose errors while learning
    )
    gid = r["gatewayId"]
    while (st := cp.get_gateway(gatewayIdentifier=gid)["status"]) in ("CREATING", "UPDATING"):
        print("  status", st); time.sleep(5)
    print("status", st, "| workload identity:", cp.get_gateway(gatewayIdentifier=gid).get("workloadIdentityDetails"))
    write_env("TICKET_GATEWAY_ID", gid)
    write_env("TICKET_GATEWAY_URL", r["gatewayUrl"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--cleanup", action="store_true"); main(p.parse_args().cleanup)
