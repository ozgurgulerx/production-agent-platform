"""Create the Gateway execution role: trusted by bedrock-agentcore.amazonaws.com (scoped to this account), allowed to
invoke the ticket Lambda, read the OpenAPI document in CODE_BUCKET and fetch tokens from Identity.
Writes AGENTCORE_GATEWAY_ROLE_ARN.

Proves: the Gateway's outbound identity for GATEWAY_IAM_ROLE targets is this role, nothing else.
Run: python gateway_role.py [--cleanup]
"""

import argparse
import json

from _common import REGION, account_id, need, session, write_env

ROLE = "AgentCoreGatewayRole-labs"


def main(cleanup: bool) -> None:
    iam = session().client("iam")
    if cleanup:
        iam.delete_role_policy(RoleName=ROLE, PolicyName="inline"); iam.delete_role(RoleName=ROLE); print("deleted"); return
    acct = account_id()
    trust = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "bedrock-agentcore.amazonaws.com"},
             "Action": "sts:AssumeRole", "Condition": {"StringEquals": {"aws:SourceAccount": acct},
             "ArnLike": {"aws:SourceArn": f"arn:aws:bedrock-agentcore:{REGION}:{acct}:*"}}}]}
    policy = {"Version": "2012-10-17", "Statement": [
        {"Effect": "Allow", "Action": ["lambda:InvokeFunction"], "Resource": f"arn:aws:lambda:{REGION}:{acct}:function:ticket-*"},
        {"Effect": "Allow", "Action": ["s3:GetObject"], "Resource": f"arn:aws:s3:::{need('CODE_BUCKET')}/openapi/*"},
        {"Effect": "Allow", "Action": ["bedrock-agentcore:GetWorkloadAccessToken", "bedrock-agentcore:GetWorkloadAccessTokenForJWT",
                                       "bedrock-agentcore:GetResourceOauth2Token", "bedrock-agentcore:GetResourceApiKey"], "Resource": "*"},
        {"Effect": "Allow", "Action": ["bedrock:InvokeGuardrailChecks"], "Resource": "*"},   # B09 Guardrails-in-Policy
        {"Effect": "Allow", "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], "Resource": "*"},
    ]}
    try:
        arn = iam.create_role(RoleName=ROLE, AssumeRolePolicyDocument=json.dumps(trust))["Role"]["Arn"]
    except iam.exceptions.EntityAlreadyExistsException:
        arn = iam.get_role(RoleName=ROLE)["Role"]["Arn"]
    iam.put_role_policy(RoleName=ROLE, PolicyName="inline", PolicyDocument=json.dumps(policy))
    write_env("AGENTCORE_GATEWAY_ROLE_ARN", arn)


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--cleanup", action="store_true"); main(p.parse_args().cleanup)
