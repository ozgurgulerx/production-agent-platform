"""Proves: a resource-based policy on the Runtime (Mar 2026) lets a partner account invoke it with its own identity;
CloudTrail then shows the real principal. PutResourcePolicy(resourceArn, policy) with the shape verified in boto3.
Usage: python resource_policy_runtime.py --partner 210987654321 [--apply] [--cleanup]"""
import json
import sys

from _common import control, need

need("TICKET_AGENT_RUNTIME_ARN")
import os
RUNTIME_ARN = os.environ["TICKET_AGENT_RUNTIME_ARN"]


def policy(partner: str) -> dict:
    return {"Version": "2012-10-17", "Statement": [{
        "Sid": "PartnerInvoke", "Effect": "Allow",
        "Principal": {"AWS": f"arn:aws:iam::{partner}:role/partner-ticket-caller"},
        "Action": ["bedrock-agentcore:InvokeAgentRuntime"],
        "Resource": [RUNTIME_ARN, f"{RUNTIME_ARN}/runtime-endpoint/DEFAULT"],   # verify endpoint ARN form
        "Condition": {"StringEquals": {"bedrock-agentcore:RuntimeAuthorizerType": "AWS_IAM"}}}]}   # verify key


def main() -> None:
    c = control()
    if "--cleanup" in sys.argv:
        c.delete_resource_policy(resourceArn=RUNTIME_ARN); print("deleted resource policy"); return
    partner = sys.argv[sys.argv.index("--partner") + 1] if "--partner" in sys.argv else "210987654321"
    doc = policy(partner)
    print(json.dumps(doc, indent=1))
    if "--apply" in sys.argv:
        r = c.put_resource_policy(resourceArn=RUNTIME_ARN, policy=json.dumps(doc))
        print("applied:", r.get("policy", "")[:200])
        print("read back:", c.get_resource_policy(resourceArn=RUNTIME_ARN).get("policy", "")[:200])


if __name__ == "__main__":
    main()
