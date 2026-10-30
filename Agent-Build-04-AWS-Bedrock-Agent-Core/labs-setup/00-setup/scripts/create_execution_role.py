"""Create the Runtime execution role the labs assume and write its ARN to the track-root .env.

Proves: the role trusts bedrock-agentcore.amazonaws.com only from this account (aws:SourceAccount /
aws:SourceArn), and grants ECR pull, logs, X-Ray, Bedrock invoke and workload-identity token calls.
B09 lab 03 prints the least-privilege diff. Run with --cleanup to delete it.
"""
import argparse, json, os, sys
from pathlib import Path
import boto3
from dotenv import load_dotenv, set_key

_TRACK_ROOT = Path(__file__).resolve().parents[3]   # track root, where .env lives (never walk up past it)
ENV = str(_TRACK_ROOT / ".env")
load_dotenv(ENV)
ROLE = "agentcore-ticket-runtime-role"
sess = boto3.Session(profile_name=os.getenv("AWS_PROFILE") or None, region_name=os.getenv("AWS_REGION", "us-east-1"))
iam, sts = sess.client("iam"), sess.client("sts")
account = sts.get_caller_identity()["Account"]
region = sess.region_name

trust = {"Version": "2012-10-17", "Statement": [{
    "Effect": "Allow", "Principal": {"Service": "bedrock-agentcore.amazonaws.com"},
    "Action": "sts:AssumeRole",
    "Condition": {"StringEquals": {"aws:SourceAccount": account},
                  "ArnLike": {"aws:SourceArn": f"arn:aws:bedrock-agentcore:{region}:{account}:*"}}}]}
policy = {"Version": "2012-10-17", "Statement": [
    {"Sid": "ECR", "Effect": "Allow", "Action": ["ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer", "ecr:GetAuthorizationToken"], "Resource": "*"},
    {"Sid": "Logs", "Effect": "Allow", "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents", "logs:DescribeLogGroups", "logs:DescribeLogStreams"], "Resource": f"arn:aws:logs:{region}:{account}:log-group:/aws/bedrock-agentcore/*"},
    {"Sid": "Traces", "Effect": "Allow", "Action": ["xray:PutTraceSegments", "xray:PutTelemetryRecords", "xray:GetSamplingRules", "xray:GetSamplingTargets", "cloudwatch:PutMetricData"], "Resource": "*"},
    {"Sid": "Models", "Effect": "Allow", "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream", "bedrock:ApplyGuardrail"], "Resource": "*"},
    {"Sid": "WorkloadIdentity", "Effect": "Allow", "Action": ["bedrock-agentcore:GetWorkloadAccessToken", "bedrock-agentcore:GetWorkloadAccessTokenForJWT", "bedrock-agentcore:GetResourceOauth2Token", "bedrock-agentcore:GetResourceApiKey"], "Resource": f"arn:aws:bedrock-agentcore:{region}:{account}:workload-identity-directory/default*"},
    {"Sid": "Memory", "Effect": "Allow", "Action": ["bedrock-agentcore:CreateEvent", "bedrock-agentcore:ListEvents", "bedrock-agentcore:RetrieveMemoryRecords", "bedrock-agentcore:ListMemoryRecords", "bedrock-agentcore:GetMemoryRecord"], "Resource": f"arn:aws:bedrock-agentcore:{region}:{account}:memory/*"},
    {"Sid": "Code", "Effect": "Allow", "Action": ["s3:GetObject"], "Resource": f"arn:aws:s3:::{os.getenv('CODE_BUCKET', '*')}/*"},
]}

def create():
    try:
        arn = iam.create_role(RoleName=ROLE, AssumeRolePolicyDocument=json.dumps(trust),
                              Description="Execution role for the ticket-agent labs")["Role"]["Arn"]
    except iam.exceptions.EntityAlreadyExistsException:
        arn = iam.get_role(RoleName=ROLE)["Role"]["Arn"]
        iam.update_assume_role_policy(RoleName=ROLE, PolicyDocument=json.dumps(trust))
    iam.put_role_policy(RoleName=ROLE, PolicyName="agentcore-ticket-runtime", PolicyDocument=json.dumps(policy))
    set_key(ENV, "AGENTCORE_RUNTIME_ROLE_ARN", arn)
    set_key(ENV, "AWS_ACCOUNT_ID", account)
    print("role", arn, "\nwritten to", ENV)

def cleanup():
    iam.delete_role_policy(RoleName=ROLE, PolicyName="agentcore-ticket-runtime")
    iam.delete_role(RoleName=ROLE); print("deleted", ROLE)

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--cleanup", action="store_true")
    cleanup() if p.parse_args().cleanup else create()
