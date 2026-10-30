"""Shared helpers for the B03 scripts: env loading, boto3 session, session ids, .env upserts.

Auth is IAM only: `AWS_PROFILE` (SSO) or the default credential chain. No access keys in files.
The `.env` sits at the track root; every script finds it by walking up from its own folder.
"""
from __future__ import annotations

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
ROLE_ARN = os.environ.get("AGENTCORE_RUNTIME_ROLE_ARN", "")
CODE_BUCKET = os.environ.get("CODE_BUCKET", "")

SUPPORT_INSTRUCTIONS = (
    "You are the support-ticket assistant for a UK bank's card team. "
    "Answer briefly. Use the tools for ticket facts; never invent a ticket. "
    "Refunds above 250 GBP need a human: refuse and say so."
)


def session() -> boto3.Session:
    return boto3.Session(profile_name=PROFILE, region_name=REGION)


def control():
    """Control plane: create/update/delete runtimes, endpoints, harnesses, memories."""
    return session().client("bedrock-agentcore-control")


def data():
    """Data plane: invoke runtimes and harnesses, events, memory records."""
    return session().client("bedrock-agentcore")


def new_session_id() -> str:
    """Runtime session ids must be at least 33 characters (B4). Two UUID4s is 73."""
    return f"ticket-{uuid.uuid4()}-{uuid.uuid4()}"


def write_env(key: str, value: str) -> None:
    """Upsert KEY=value into the track-root .env so later labs can read the resource."""
    path = Path(ENV_PATH) if ENV_PATH else Path(__file__).resolve().parents[4] / ".env"
    text = path.read_text() if path.exists() else ""
    line = f"{key}={value}"
    if re.search(rf"^{re.escape(key)}=.*$", text, flags=re.M):
        text = re.sub(rf"^{re.escape(key)}=.*$", line, text, flags=re.M)
    else:
        text = text.rstrip("\n") + ("\n" if text else "") + line + "\n"
    path.write_text(text)
    os.environ[key] = value
    print(f"[env] {line}")


def require(*names: str) -> None:
    missing = [n for n in names if not os.environ.get(n)]
    if missing:
        raise SystemExit(f"Set {', '.join(missing)} in .env first (see labs-setup/00-setup).")


def read_body(response) -> str:
    """InvokeAgentRuntime returns a StreamingBody; SSE when the agent streams, JSON otherwise."""
    ctype = response.get("contentType", "")
    body = response["response"]
    if "text/event-stream" in ctype:
        out = []
        for raw in body.iter_lines():
            line = raw.decode() if isinstance(raw, bytes) else raw
            if line.startswith("data: "):
                out.append(line[6:])
        return "\n".join(out)
    return body.read().decode()
