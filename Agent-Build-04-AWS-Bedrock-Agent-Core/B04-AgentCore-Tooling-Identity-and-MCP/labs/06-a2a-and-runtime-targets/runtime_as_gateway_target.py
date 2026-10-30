"""Register the B03 ticket-agent Runtime as an HTTP `agentcoreRuntime` target on the lab 03 Gateway with
CALLER_IAM_CREDENTIALS, then call it at https://<gwId>.gateway.bedrock-agentcore.<region>.amazonaws.com/<target>/invocations.

Proves: an agent becomes a tool for other agents without being an MCP server; the downstream Runtime sees the caller's
IAM identity, not the Gateway's. Run: python runtime_as_gateway_target.py [--cleanup]
"""

import argparse
import json
import time

import httpx
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

from _common import REGION, control, need, new_session_id, session, write_env

TARGET = "ticket-agent"


def sigv4_post(url: str, body: dict) -> httpx.Response:
    creds = session().get_credentials().get_frozen_credentials()
    req = AWSRequest(method="POST", url=url, data=json.dumps(body), headers={"Content-Type": "application/json",
                     "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id": new_session_id()})
    SigV4Auth(creds, "bedrock-agentcore", REGION).add_auth(req)          # verify: signing service name for gateway URLs
    return httpx.post(url, content=req.body, headers=dict(req.headers), timeout=120)


def main(cleanup: bool) -> None:
    cp, gid = control(), need("TICKET_GATEWAY_ID")
    if cleanup:
        cp.delete_gateway_target(gatewayIdentifier=gid, targetId=need("TICKET_AGENT_TARGET_ID")); print("deleted"); return
    r = cp.create_gateway_target(
        gatewayIdentifier=gid, name=TARGET,
        targetConfiguration={"http": {"agentcoreRuntime": {"arn": need("TICKET_AGENT_RUNTIME_ARN"), "qualifier": "DEFAULT"}}},
        credentialProviderConfigurations=[{"credentialProviderType": "CALLER_IAM_CREDENTIALS"}],   # or JWT_PASSTHROUGH
    )
    tid = r["targetId"]
    while (st := cp.get_gateway_target(gatewayIdentifier=gid, targetId=tid)["status"]) in ("CREATING", "UPDATING"):
        print("  status", st); time.sleep(5)
    print("status", st); write_env("TICKET_AGENT_TARGET_ID", tid)

    url = f"https://{gid}.gateway.bedrock-agentcore.{REGION}.amazonaws.com/{TARGET}/invocations"
    resp = sigv4_post(url, {"prompt": "What is the status of ticket 1042?"})
    print(resp.status_code, resp.text[:600])


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--cleanup", action="store_true"); main(p.parse_args().cleanup)
