"""Shared helpers for the C09 labs: device-code token (no secrets), Power Platform API, Graph, ARM/Resource Graph, .env writer."""
import json
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
ENVIRONMENT_ID = os.environ.get("ENVIRONMENT_ID", "")
AGENT_ID = os.environ.get("AGENT_ID", "")
PP_API = os.environ.get("POWER_PLATFORM_API", "https://api.powerplatform.com").rstrip("/")
HERE = Path(__file__).resolve().parent
CACHE = HERE / ".msal_cache.json"          # gitignored; delete it to sign in again

PP_SCOPE = "https://api.powerplatform.com/.default"
GRAPH_SCOPE = "https://graph.microsoft.com/.default"
ARM_SCOPE = "https://management.azure.com/.default"
BAP_SCOPE = "https://service.powerapps.com/.default"   # Power Platform admin (BAP) API used by DLP admin calls; verify


def need(*names: str) -> None:
    missing = [n for n in names if not os.environ.get(n)]
    if missing:
        sys.exit(f"missing in .env: {', '.join(missing)} (run the earlier lab or fill .env)")


def _app() -> msal.PublicClientApplication:
    need("TENANT_ID", "CLIENT_ID")
    cache = msal.SerializableTokenCache()
    if CACHE.exists():
        cache.deserialize(CACHE.read_text())
    app = msal.PublicClientApplication(CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}", token_cache=cache)
    app._lab_cache = cache  # noqa: SLF001
    return app


def device_code_token(scope: str) -> str:
    """Delegated token for one resource via device code. Silent from cache when possible. Never a client secret."""
    app = _app()
    accounts = app.get_accounts()
    result = app.acquire_token_silent([scope], account=accounts[0]) if accounts else None
    if not result:
        flow = app.initiate_device_flow(scopes=[scope])
        if "user_code" not in flow:
            sys.exit(f"device flow failed: {flow}")
        print(flow["message"])
        result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        sys.exit(f"token error: {result.get('error_description', result)}")
    if app._lab_cache.has_state_changed:  # noqa: SLF001
        CACHE.write_text(app._lab_cache.serialize())  # noqa: SLF001
    return result["access_token"]


def _client(scope: str, base: str) -> httpx.Client:
    return httpx.Client(base_url=base, headers={"Authorization": f"Bearer {device_code_token(scope)}"}, timeout=60)


def pp_api() -> httpx.Client:
    return _client(PP_SCOPE, PP_API)


def graph() -> httpx.Client:
    return _client(GRAPH_SCOPE, "https://graph.microsoft.com/v1.0")


def arm() -> httpx.Client:
    return _client(ARM_SCOPE, "https://management.azure.com")


def bap() -> httpx.Client:
    return _client(BAP_SCOPE, "https://api.bap.microsoft.com")


def write_env(key: str, value: str) -> None:
    set_key(ENV_PATH, key, value)
    os.environ[key] = value
    print(f"  .env  {key}={value}")


def show(label: str, resp: httpx.Response) -> dict:
    try:
        body = resp.json()
    except json.JSONDecodeError:
        body = {"text": resp.text[:400]}
    print(f"{label:<40} HTTP {resp.status_code}  {json.dumps(body)[:200]}")
    return body if isinstance(body, dict) else {"value": body}
