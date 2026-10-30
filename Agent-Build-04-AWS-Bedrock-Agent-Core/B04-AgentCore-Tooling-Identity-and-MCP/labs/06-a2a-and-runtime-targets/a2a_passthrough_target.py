"""Add an A2A passthrough target pointing at the B03 A2A specialist Runtime (port 9000 contract), with session
stickiness on the Runtime session header and JWT passthrough, then fetch its agent card through the Gateway path.

Proves: Gateway routes A2A, it does not aggregate it; the card comes from the Runtime. Run: python a2a_passthrough_target.py [--cleanup]
"""

import argparse
import sys
import time
from pathlib import Path

import httpx

from _common import REGION, control, need, runtime_invocations_url, write_env

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01-identity-inbound"))
from tokens import client_credentials_token  # noqa: E402

TARGET = "refund-specialist"


def main(cleanup: bool) -> None:
    cp, gid = control(), need("TICKET_GATEWAY_ID")
    if cleanup:
        cp.delete_gateway_target(gatewayIdentifier=gid, targetId=need("REFUND_A2A_TARGET_ID")); print("deleted"); return
    endpoint = runtime_invocations_url(need("TICKET_A2A_RUNTIME_ARN")).split("?")[0]      # B03 lab 03 writes the ARN
    r = cp.create_gateway_target(
        gatewayIdentifier=gid, name=TARGET,
        targetConfiguration={"http": {"passthrough": {"endpoint": endpoint, "protocolType": "A2A",
                             "stickinessConfiguration": {"identifier": "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id", "timeout": 900}}}},   # verify
        credentialProviderConfigurations=[{"credentialProviderType": "JWT_PASSTHROUGH"}],
    )
    tid = r["targetId"]
    while (st := cp.get_gateway_target(gatewayIdentifier=gid, targetId=tid)["status"]) in ("CREATING", "UPDATING"):
        print("  status", st); time.sleep(5)
    print("status", st); write_env("REFUND_A2A_TARGET_ID", tid)

    card_url = f"https://{gid}.gateway.bedrock-agentcore.{REGION}.amazonaws.com/{TARGET}/invocations/.well-known/agent-card.json"   # verify path
    resp = httpx.get(card_url, headers={"Authorization": f"Bearer {client_credentials_token()}"}, timeout=60)
    print(resp.status_code, resp.text[:800])


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--cleanup", action="store_true"); main(p.parse_args().cleanup)
