"""Shared bits for the observability lab. IAM/SSO only; `.env` at the track root."""
import os
from pathlib import Path
import boto3
from dotenv import load_dotenv

_TRACK_ROOT = Path(__file__).resolve().parents[3]   # track root, where .env lives (never walk up past it)
load_dotenv(str(_TRACK_ROOT / ".env"))
REGION = os.environ.get("AWS_REGION", "us-east-1")
PROFILE = os.environ.get("AWS_PROFILE") or None
MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "global.anthropic.claude-haiku-5-5")
RUNTIME_ARN = os.environ.get("TICKET_AGENT_RUNTIME_ARN", "")


def session() -> boto3.Session:
    return boto3.Session(profile_name=PROFILE, region_name=REGION)


def agent_id_from_arn(arn: str) -> str:
    """arn:aws:bedrock-agentcore:<region>:<acct>:runtime/<agent_id> -> <agent_id>"""
    return arn.rsplit("/", 1)[-1]


def runtime_log_group(arn: str = RUNTIME_ARN, endpoint: str = "DEFAULT") -> str:
    return f"/aws/bedrock-agentcore/runtimes/{agent_id_from_arn(arn)}-{endpoint}"
