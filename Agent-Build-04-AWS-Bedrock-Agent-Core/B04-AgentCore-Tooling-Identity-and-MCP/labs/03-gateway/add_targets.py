"""Add two MCP targets to the Gateway: the Lambda (inline toolSchema, GATEWAY_IAM_ROLE) and the OpenAPI document
(S3, API_KEY credential provider from lab 04 row 01 if present). Polls each to READY.

Proves: different backends, one tool list; outbound credential is per target.
Run: python add_targets.py [--cleanup]
"""

import argparse
import os
import time
from pathlib import Path

from _common import control, need, session, write_env

TOOLS = [
    {"name": "get_ticket", "description": "Return one support ticket by id.",
     "inputSchema": {"type": "object", "properties": {"ticket_id": {"type": "string"}}, "required": ["ticket_id"]}},
    {"name": "list_tickets", "description": "List tickets by status (open|closed).",
     "inputSchema": {"type": "object", "properties": {"status": {"type": "string"}}}},
    {"name": "get_policy", "description": "Return a named policy text; default refund.",
     "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}}}},
    {"name": "issue_refund", "description": "Refund amount GBP against a ticket; above 250 escalates.",
     "inputSchema": {"type": "object", "properties": {"ticket_id": {"type": "string"}, "amount": {"type": "number"},
                                                      "reason": {"type": "string"}}, "required": ["ticket_id", "amount"]}},
]


def wait(cp, gid, tid):
    while (st := cp.get_gateway_target(gatewayIdentifier=gid, targetId=tid)["status"]) in ("CREATING", "UPDATING", "SYNCHRONIZING"):
        print("   ", tid, st); time.sleep(5)
    print("   ", tid, st, cp.get_gateway_target(gatewayIdentifier=gid, targetId=tid).get("statusReasons", ""))


def main(cleanup: bool) -> None:
    cp, gid = control(), need("TICKET_GATEWAY_ID")
    if cleanup:
        for t in cp.list_gateway_targets(gatewayIdentifier=gid).get("items", []):
            cp.delete_gateway_target(gatewayIdentifier=gid, targetId=t["targetId"]); print("deleted", t["name"])
        return
    r = cp.create_gateway_target(
        gatewayIdentifier=gid, name="tickets-lambda",
        targetConfiguration={"mcp": {"lambda": {"lambdaArn": need("TICKET_TOOLS_LAMBDA_ARN"), "toolSchema": {"inlinePayload": TOOLS}}}},
        credentialProviderConfigurations=[{"credentialProviderType": "GATEWAY_IAM_ROLE"}],
    )
    wait(cp, gid, r["targetId"]); write_env("TICKETS_LAMBDA_TARGET_ID", r["targetId"])

    key = "openapi/tickets.yaml"
    session().client("s3").put_object(Bucket=need("CODE_BUCKET"), Key=key, Body=(Path(__file__).parent / key).read_bytes())
    provider_arn = os.environ.get("TICKETS_API_KEY_PROVIDER_ARN")
    creds = ([{"credentialProviderType": "API_KEY", "credentialProvider": {"apiKeyCredentialProvider": {
                "providerArn": provider_arn, "credentialLocation": "HEADER", "credentialParameterName": "x-api-key"}}}]
             if provider_arn else [{"credentialProviderType": "GATEWAY_IAM_ROLE"}])   # placeholder until lab 04 row 01
    r = cp.create_gateway_target(
        gatewayIdentifier=gid, name="tickets-api",
        targetConfiguration={"mcp": {"openApiSchema": {"s3": {"uri": f"s3://{need('CODE_BUCKET')}/{key}"}}}},
        credentialProviderConfigurations=creds,
    )
    wait(cp, gid, r["targetId"]); write_env("TICKETS_API_TARGET_ID", r["targetId"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--cleanup", action="store_true"); main(p.parse_args().cleanup)
