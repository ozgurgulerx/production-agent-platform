"""Shared bits for the guardrails lab. IAM/SSO only; `.env` at the track root (walks up)."""
import os
import re
from pathlib import Path

import boto3
from dotenv import load_dotenv

_TRACK_ROOT = Path(__file__).resolve().parents[3]   # track root, where .env lives (never walk up past it)
ENV_PATH = str(_TRACK_ROOT / ".env")
load_dotenv(ENV_PATH)
REGION = os.environ.get("AWS_REGION", "us-east-1")
PROFILE = os.environ.get("AWS_PROFILE") or None
MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "global.anthropic.claude-haiku-5-5")
GUARDRAIL_ID = os.environ.get("GUARDRAIL_ID", "")
GUARDRAIL_VERSION = os.environ.get("GUARDRAIL_VERSION", "DRAFT")


def session() -> boto3.Session:
    return boto3.Session(profile_name=PROFILE, region_name=REGION)


def bedrock():
    return session().client("bedrock")


def runtime():
    return session().client("bedrock-runtime")


def write_env(key: str, value: str) -> None:
    p = Path(ENV_PATH)
    text = p.read_text() if p.exists() else ""
    line = f"{key}={value}"
    text = re.sub(rf"^{key}=.*$", line, text, flags=re.M) if re.search(rf"^{key}=", text, flags=re.M) else text.rstrip("\n") + f"\n{line}\n"
    p.write_text(text)
    print(f".env <- {line}")


def require_guardrail() -> tuple[str, str]:
    if not GUARDRAIL_ID:
        raise SystemExit("run create_guardrail.py first (writes GUARDRAIL_ID / GUARDRAIL_VERSION to .env)")
    return GUARDRAIL_ID, GUARDRAIL_VERSION
