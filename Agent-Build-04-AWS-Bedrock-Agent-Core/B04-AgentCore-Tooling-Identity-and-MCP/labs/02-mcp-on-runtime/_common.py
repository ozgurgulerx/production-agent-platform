"""Shared helpers for the B04 labs. IAM via SSO profile only; `.env` lives at the track root."""

import os
import re
import uuid
from pathlib import Path

import boto3
from dotenv import load_dotenv

_TRACK_ROOT = Path(__file__).resolve().parents[3]   # track root, where .env lives (never walk up past it)
ENV_PATH = str(_TRACK_ROOT / ".env")
load_dotenv(ENV_PATH)

REGION = os.environ.get("AWS_REGION", "us-east-1")
PROFILE = os.environ.get("AWS_PROFILE") or None
MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "global.anthropic.claude-haiku-5-5")


def session() -> boto3.Session:
    return boto3.Session(profile_name=PROFILE, region_name=REGION)


def control():
    return session().client("bedrock-agentcore-control")


def data():
    return session().client("bedrock-agentcore")


def account_id() -> str:
    return os.environ.get("AWS_ACCOUNT_ID") or session().client("sts").get_caller_identity()["Account"]


def new_session_id() -> str:
    """Runtime session ids must be at least 33 characters."""
    return f"b04-{uuid.uuid4()}-{uuid.uuid4().hex[:8]}"


def write_env(key: str, value: str) -> None:
    """Upsert KEY=value in the track-root .env so the next lab can read it."""
    path = Path(ENV_PATH) if ENV_PATH else Path(__file__).resolve().parents[3] / ".env"
    text = path.read_text() if path.exists() else ""
    line = f"{key}={value}"
    if re.search(rf"^{re.escape(key)}=.*$", text, flags=re.M):
        text = re.sub(rf"^{re.escape(key)}=.*$", line, text, flags=re.M)
    else:
        text = text.rstrip("\n") + ("\n" if text else "") + line + "\n"
    path.write_text(text)
    os.environ[key] = value
    print(f"  .env ← {line}")


def need(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        raise SystemExit(f"{key} is not set in {ENV_PATH or '.env'}; run the lab that writes it first")
    return value


def runtime_invocations_url(runtime_arn: str, qualifier: str = "DEFAULT") -> str:
    from urllib.parse import quote

    return f"https://bedrock-agentcore.{REGION}.amazonaws.com/runtimes/{quote(runtime_arn, safe='')}/invocations?qualifier={qualifier}"
