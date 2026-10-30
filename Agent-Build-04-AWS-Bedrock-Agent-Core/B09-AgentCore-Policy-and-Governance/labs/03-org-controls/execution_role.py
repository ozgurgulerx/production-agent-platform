"""Proves: a least-privilege Runtime execution role has a trust policy bound to this account (aws:SourceAccount)
and this runtime's ARN pattern (aws:SourceArn), a model allow-list, and no BedrockAgentCoreFullAccess.
Default: print both documents. --apply creates the role; --cleanup deletes it."""
import json
import os
import sys

from _common import REGION, session

ACCOUNT = os.environ.get("AWS_ACCOUNT_ID", "<account>")
ROLE = "ticket-agent-runtime-role"
MODELS = ["anthropic.claude-haiku-5-5*", "anthropic.claude-sonnet-5-5*", "amazon.nova-2-lite-v1:0"]

TRUST = {"Version": "2012-10-17", "Statement": [{
    "Effect": "Allow", "Principal": {"Service": "bedrock-agentcore.amazonaws.com"}, "Action": "sts:AssumeRole",
    "Condition": {"StringEquals": {"aws:SourceAccount": ACCOUNT},
                  "ArnLike": {"aws:SourceArn": f"arn:aws:bedrock-agentcore:{REGION}:{ACCOUNT}:*"}}}]}

PERMISSIONS = {"Version": "2012-10-17", "Statement": [
    {"Sid": "Image", "Effect": "Allow", "Action": ["ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer"],
     "Resource": f"arn:aws:ecr:{REGION}:{ACCOUNT}:repository/ticket-agent*"},
    {"Sid": "ImageAuth", "Effect": "Allow", "Action": ["ecr:GetAuthorizationToken"], "Resource": "*"},
    {"Sid": "Logs", "Effect": "Allow",
     "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents", "logs:DescribeLogGroups",
                "logs:DescribeLogStreams"],
     "Resource": f"arn:aws:logs:{REGION}:{ACCOUNT}:log-group:/aws/bedrock-agentcore/runtimes/*"},
    {"Sid": "Traces", "Effect": "Allow",
     "Action": ["xray:PutTraceSegments", "xray:PutTelemetryRecords", "cloudwatch:PutMetricData"], "Resource": "*"},
    {"Sid": "Models", "Effect": "Allow",
     "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream", "bedrock:Converse",
                "bedrock:ConverseStream"],
     "Resource": [f"arn:aws:bedrock:*::foundation-model/{m}" for m in MODELS]
                 + [f"arn:aws:bedrock:*:{ACCOUNT}:inference-profile/global.{m}" for m in MODELS]},
    {"Sid": "WorkloadIdentity", "Effect": "Allow",
     "Action": ["bedrock-agentcore:GetWorkloadAccessToken", "bedrock-agentcore:GetWorkloadAccessTokenForJWT"],
     "Resource": f"arn:aws:bedrock-agentcore:{REGION}:{ACCOUNT}:workload-identity-directory/default*"},
    {"Sid": "NeverMintUserTokens", "Effect": "Deny",
     "Action": ["bedrock-agentcore:GetWorkloadAccessTokenForUserId"], "Resource": "*"},
]}


def main() -> None:
    iam = session().client("iam")
    if "--cleanup" in sys.argv:
        iam.delete_role_policy(RoleName=ROLE, PolicyName="runtime-permissions"); iam.delete_role(RoleName=ROLE)
        print("deleted", ROLE); return
    if "--apply" in sys.argv:
        r = iam.create_role(RoleName=ROLE, AssumeRolePolicyDocument=json.dumps(TRUST), Tags=[{"Key": "owner", "Value": "b09"}])
        iam.put_role_policy(RoleName=ROLE, PolicyName="runtime-permissions", PolicyDocument=json.dumps(PERMISSIONS))
        print("created", r["Role"]["Arn"]); return
    print("# trust policy\n", json.dumps(TRUST, indent=1)); print("\n# permissions\n", json.dumps(PERMISSIONS, indent=1))
    print("\ngrep targets: 'BedrockAgentCoreFullAccess' attached? trust without SourceArn? InvokeModel on '*'?")


if __name__ == "__main__":
    main()
