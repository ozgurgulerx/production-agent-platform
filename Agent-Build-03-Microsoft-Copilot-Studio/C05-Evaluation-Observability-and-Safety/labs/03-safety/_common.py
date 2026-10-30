"""Shared helpers for the C05 labs: device-code token, Power Platform API and Dataverse calls, .env writer. No secrets."""
import json
import os
import sys
from pathlib import Path

import httpx
import msal
from dotenv import load_dotenv, set_key

_TRACK_ROOT = Path(__file__).resolve().parents[3]   # track root, where .env lives (never walk up past it)
ENV_PATH = _TRACK_ROOT / ".env"
load_dotenv(ENV_PATH)

TENANT_ID = os.environ.get("TENANT_ID", "")
CLIENT_ID = os.environ.get("CLIENT_ID", "")
ENVIRONMENT_ID = os.environ.get("ENVIRONMENT_ID", "")
ENVIRONMENT_URL = os.environ.get("ENVIRONMENT_URL", "").rstrip("/")
AGENT_ID = os.environ.get("AGENT_ID", "")
PP_API = os.environ.get("POWER_PLATFORM_API", "https://api.powerplatform.com").rstrip("/")
API_VERSION = "2024-10-01"
CACHE = Path(__file__).resolve().parent / ".msal_cache.json"      # gitignored


def need(*names: str) -> None:
    missing = [n for n in names if not os.environ.get(n)]
    if missing:
        sys.exit(f"missing in .env: {', '.join(missing)} (see labs-setup/00-setup and the earlier labs)")


def device_code_token(scopes: list[str]) -> str:
    """Delegated token via device code on the public-client app. Cached between runs; no client secret anywhere."""
    need("TENANT_ID", "CLIENT_ID")
    cache = msal.SerializableTokenCache()
    if CACHE.exists():
        cache.deserialize(CACHE.read_text())
    app = msal.PublicClientApplication(CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}", token_cache=cache)
    result = None
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(scopes, account=accounts[0])
    if not result:
        flow = app.initiate_device_flow(scopes=scopes)
        print(flow["message"])
        result = app.acquire_token_by_device_flow(flow)
    if cache.has_state_changed:
        CACHE.write_text(cache.serialize())
    if "access_token" not in result:
        sys.exit(f"token failed: {result.get('error_description')}")
    return result["access_token"]


def pp_api(method: str, path: str, json_body: dict | None = None) -> dict:
    """Call the Power Platform API (copilotstudio namespace). `path` starts with /copilotstudio/..."""
    token = device_code_token([f"{PP_API}/.default"])
    sep = "&" if "?" in path else "?"
    url = f"{PP_API}{path}{sep}api-version={API_VERSION}" if "api-version" not in path else f"{PP_API}{path}"
    r = httpx.request(method, url, json=json_body, timeout=60,
                      headers={"Authorization": f"Bearer {token}", "Accept": "application/json"})
    if r.status_code >= 400:
        sys.exit(f"{method} {url} -> {r.status_code}\n{r.text[:800]}")
    return r.json() if r.content else {}


def dataverse(method: str, path: str, json_body: dict | None = None) -> dict:
    """Dataverse Web API call. `path` starts with /api/data/v9.2/..."""
    need("ENVIRONMENT_URL")
    token = device_code_token([f"{ENVIRONMENT_URL}/user_impersonation"])
    r = httpx.request(method, f"{ENVIRONMENT_URL}{path}", json=json_body, timeout=60,
                      headers={"Authorization": f"Bearer {token}", "Accept": "application/json",
                               "OData-MaxVersion": "4.0", "OData-Version": "4.0", "Prefer": "odata.include-annotations=*"})
    if r.status_code >= 400:
        sys.exit(f"{method} {path} -> {r.status_code}\n{r.text[:800]}")
    return r.json() if r.content else {}


def write_env(key: str, value: str) -> None:
    """Persist an id into the track-root .env so the next script finds it."""
    set_key(str(ENV_PATH), key, value)
    os.environ[key] = value
    print(f"  .env  {key}={value}")


def show(obj: dict, limit: int = 600) -> None:
    print(json.dumps(obj, indent=1, ensure_ascii=False)[:limit])
