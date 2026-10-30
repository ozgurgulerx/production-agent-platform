"""Shared helpers for the B09 labs: session from SSO profile, clients, .env writer, gateway MCP call, Cognito token."""
import json
import os
import sys
import uuid
from pathlib import Path

import boto3
import httpx
from dotenv import load_dotenv, set_key

_TRACK_ROOT = Path(__file__).resolve().parents[3]   # track root, where .env lives (never walk up past it)
ENV_PATH = str(_TRACK_ROOT / ".env")
load_dotenv(ENV_PATH)

REGION = os.environ.get("AWS_REGION", "us-east-1")
PROFILE = os.environ.get("AWS_PROFILE") or None
GATEWAY_ID = os.environ.get("TICKET_GATEWAY_ID", "")
GATEWAY_URL = os.environ.get("TICKET_GATEWAY_URL", "")
ENGINE_ID = os.environ.get("POLICY_ENGINE_ID", "")
HERE = Path(__file__).resolve().parent


def session() -> boto3.Session:
    return boto3.Session(profile_name=PROFILE, region_name=REGION)


def control():
    return session().client("bedrock-agentcore-control")


def data():
    return session().client("bedrock-agentcore")


def write_env(key: str, value: str) -> None:
    """Persist a resource id into the track-root .env so the next script finds it."""
    set_key(ENV_PATH or str(Path.cwd() / ".env"), key, value)
    os.environ[key] = value
    print(f"  .env  {key}={value}")


def need(*names: str) -> None:
    missing = [n for n in names if not os.environ.get(n)]
    if missing:
        sys.exit(f"missing in .env: {', '.join(missing)} (run the earlier lab first)")


def gateway_arn() -> str:
    return control().get_gateway(gatewayIdentifier=GATEWAY_ID)["gatewayArn"]


def cognito_token() -> str:
    """Bearer for the gateway's JWT authorizer. USER_PASSWORD_AUTH with the test user from B04 lab 01."""
    import getpass

    need("COGNITO_CLIENT_ID", "COGNITO_TEST_USERNAME")
    idp = session().client("cognito-idp")
    pw = os.environ.get("COGNITO_TEST_PASSWORD") or getpass.getpass("Cognito test user password: ")
    r = idp.initiate_auth(
        ClientId=os.environ["COGNITO_CLIENT_ID"],
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": os.environ["COGNITO_TEST_USERNAME"], "PASSWORD": pw},
    )
    return r["AuthenticationResult"]["AccessToken"]


def call_tool(token: str, name: str, arguments: dict) -> dict:
    """One MCP tools/call through the gateway (stateless streamable HTTP). Returns the JSON-RPC body."""
    body = {"jsonrpc": "2.0", "id": str(uuid.uuid4()), "method": "tools/call",
            "params": {"name": f"TicketTools___{name}", "arguments": arguments}}
    r = httpx.post(GATEWAY_URL, json=body, timeout=60,
                   headers={"Authorization": f"Bearer {token}", "Accept": "application/json, text/event-stream"})
    try:
        return {"status": r.status_code, **r.json()}
    except json.JSONDecodeError:
        return {"status": r.status_code, "text": r.text[:500]}


def show(label: str, result: dict) -> None:
    verdict = "DENIED" if result.get("error") or result.get("status", 200) >= 400 else "ok"
    print(f"{label:<34} {verdict:<7} {json.dumps(result)[:160]}")
