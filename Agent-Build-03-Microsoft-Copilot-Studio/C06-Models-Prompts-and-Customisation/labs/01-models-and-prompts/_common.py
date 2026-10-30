"""Shared helpers for the C06 lab: device-code sign-in (no secrets), Dataverse Web API client, .env writer.

The .env lives at the track root; it is found by path, never by walking up.
"""
import os
import sys
from pathlib import Path

import httpx
import msal
from dotenv import load_dotenv, set_key

_TRACK_ROOT = Path(__file__).resolve().parents[3]   # track root, where .env lives (never walk up past it)
ENV_PATH = str(_TRACK_ROOT / ".env")
load_dotenv(ENV_PATH)

TENANT_ID = os.environ.get("TENANT_ID", "")
CLIENT_ID = os.environ.get("CLIENT_ID", "")
ENVIRONMENT_URL = os.environ.get("ENVIRONMENT_URL", "").rstrip("/")
AGENT_ID = os.environ.get("AGENT_ID", "")
AGENT_SCHEMA_NAME = os.environ.get("AGENT_SCHEMA_NAME", "")

_cache = msal.SerializableTokenCache()


def need(*names: str) -> None:
    missing = [n for n in names if not os.environ.get(n)]
    if missing:
        sys.exit(f"missing in .env: {', '.join(missing)} (see labs-setup/00-setup/README.md)")


def device_code_token(scopes: list[str]) -> str:
    """Interactive device-code sign-in through the public-client app registration. Cached per process."""
    need("TENANT_ID", "CLIENT_ID")
    app = msal.PublicClientApplication(CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}",
                                       token_cache=_cache)
    accounts = app.get_accounts()
    result = app.acquire_token_silent(scopes, account=accounts[0]) if accounts else None
    if not result:
        flow = app.initiate_device_flow(scopes=scopes)
        if "user_code" not in flow:
            sys.exit(f"device flow failed: {flow}")
        print(flow["message"])
        result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        sys.exit(f"sign-in failed: {result.get('error_description')}")
    return result["access_token"]


def dataverse() -> httpx.Client:
    """Dataverse Web API client for the environment (delegated user_impersonation)."""
    need("ENVIRONMENT_URL")
    token = device_code_token([f"{ENVIRONMENT_URL}/user_impersonation"])
    return httpx.Client(base_url=f"{ENVIRONMENT_URL}/api/data/v9.2",
                        headers={"Authorization": f"Bearer {token}", "Accept": "application/json",
                                 "OData-MaxVersion": "4.0", "OData-Version": "4.0"}, timeout=60)


def write_env(key: str, value: str) -> None:
    """Upsert KEY=value in the track-root .env so the next lab can read it."""
    set_key(ENV_PATH, key, value)
    os.environ[key] = value
    print(f"  .env  {key}={value}")
