"""Expose the knowledge base to agents as MCP tools on the B04 gateway.

Proves: the agent never learns a knowledge-base id or a Retrieve API; it sees two tools on the same gateway as
the ticket tools, `Retrieve` and `AgenticRetrieveStream` (J2), behind the same JWT authoriser and the same
Cedar policy engine (B09). Writes TICKET_KB_TARGET_ID.

The Managed KB target is a Gateway *connector* (CreateGatewayTarget targetConfiguration.mcp.connector) whose
connectorId names the Bedrock knowledge-base integration; the id string below is read from .env so the
verified value from the console can be dropped in.          # verify: connector id and `configurations` keys (D1, J2)
Run:  python add_gateway_target.py [--cleanup]
"""
import os
import sys
import time

from _common import control, need, write_env

TARGET = "TicketPolicies"
GATEWAY = need("TICKET_GATEWAY_ID")
KB_ID = need("TICKET_KB_ID")
CONNECTOR_ID = os.environ.get("KB_CONNECTOR_ID", "bedrock-knowledge-base")   # verify: exact connector id in your region


def create(cp):
    for t in cp.list_gateway_targets(gatewayIdentifier=GATEWAY, maxResults=100)["items"]:
        if t["name"] == TARGET:
            return t
    t = cp.create_gateway_target(
        gatewayIdentifier=GATEWAY, name=TARGET,
        description="Managed knowledge base of UK card policies; tools Retrieve and AgenticRetrieveStream",
        targetConfiguration={"mcp": {"connector": {
            "source": {"connectorId": CONNECTOR_ID},
            "enabled": ["Retrieve", "AgenticRetrieveStream"],                                  # verify: tool names as listed
            "configurations": [{"knowledgeBaseId": KB_ID}],                                     # verify: configuration key
        }}},
        credentialProviderConfigurations=[{"credentialProviderType": "GATEWAY_IAM_ROLE"}],  # the gateway role calls Bedrock
    )
    while (t := cp.get_gateway_target(gatewayIdentifier=GATEWAY, targetId=t["targetId"]))["status"] != "READY":
        if t["status"] == "FAILED":
            raise SystemExit(t.get("statusReasons"))
        print("  target:", t["status"]); time.sleep(5)
    return t


if __name__ == "__main__":
    cp = control()
    if "--cleanup" in sys.argv:
        for t in cp.list_gateway_targets(gatewayIdentifier=GATEWAY, maxResults=100)["items"]:
            if t["name"] == TARGET:
                cp.delete_gateway_target(gatewayIdentifier=GATEWAY, targetId=t["targetId"]); print("[cleanup] target deleted")
        raise SystemExit(0)
    t = create(cp)
    write_env("TICKET_KB_TARGET_ID", t["targetId"])
    print("gateway role needs bedrock:Retrieve and bedrock:AgenticRetrieveStream on", KB_ID, "(add to AGENTCORE_GATEWAY_ROLE_ARN)")
    print("tool names on the gateway:", f"{TARGET}___Retrieve", f"{TARGET}___AgenticRetrieveStream")
