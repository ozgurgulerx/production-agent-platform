"""Shared helpers for the C03 scripts: track-root .env, device-code tokens, Power Platform API and Dataverse calls.

Auth is Entra only: a public-client app registration (CLIENT_ID) and device-code sign-in; tokens cached in
`.msal_cache.json` next to this file (gitignored). No client secrets anywhere.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import httpx
import msal
from dotenv import load_dotenv

_TRACK_ROOT = Path(__file__).resolve().parents[3]   # track root, where .env lives (never walk up past it)
ENV_PATH = str(_TRACK_ROOT / ".env")
load_dotenv(ENV_PATH)

TENANT_ID = os.environ.get("TENANT_ID", "")
CLIENT_ID = os.environ.get("CLIENT_ID", "")
ENVIRONMENT_ID = os.environ.get("ENVIRONMENT_ID", "")
ENVIRONMENT_URL = os.environ.get("ENVIRONMENT_URL", "").rstrip("/")
PP_API = os.environ.get("POWER_PLATFORM_API", "https://api.powerplatform.com").rstrip("/")
AGENT_SCHEMA_NAME = os.environ.get("AGENT_SCHEMA_NAME", "")
HERE = Path(__file__).resolve().parent
_CACHE = HERE / ".msal_cache.json"

SUPPORT_INSTRUCTIONS = (HERE / "instructions.md").read_text() if (HERE / "instructions.md").exists() else ""


def need(*names: str) -> None:
    missing = [n for n in names if not os.environ.get(n)]
    if missing:
        sys.exit(f"missing in .env: {', '.join(missing)} (see ../../labs-setup/00-setup/README.md)")


def _app() -> msal.PublicClientApplication:
    need("TENANT_ID", "CLIENT_ID")
    cache = msal.SerializableTokenCache()
    if _CACHE.exists():
        cache.deserialize(_CACHE.read_text())
    app = msal.PublicClientApplication(CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}", token_cache=cache)
    app._lab_cache = cache  # noqa: SLF001  keep a handle to persist after each call
    return app


def device_code_token(scopes: list[str]) -> str:
    """Delegated token via device code; silent from the cache when possible."""
    app = _app()
    accounts = app.get_accounts()
    result = app.acquire_token_silent(scopes, account=accounts[0]) if accounts else None
    if not result:
        flow = app.initiate_device_flow(scopes=scopes)
        if "user_code" not in flow:
            sys.exit(f"device flow failed: {flow}")
        print(flow["message"], flush=True)
        result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        sys.exit(f"token error: {result.get('error_description', result)}")
    if app._lab_cache.has_state_changed:  # noqa: SLF001
        _CACHE.write_text(app._lab_cache.serialize())  # noqa: SLF001
    return result["access_token"]


def pp_api(method: str, path: str, scope: str = "https://api.powerplatform.com/.default", **kw) -> httpx.Response:
    """Power Platform API (copilotstudio namespace and friends). `path` starts with /copilotstudio/... (C6)."""
    token = device_code_token([scope])
    return httpx.request(method, f"{PP_API}{path}", headers={"Authorization": f"Bearer {token}"}, timeout=60, **kw)


def dataverse(method: str, path: str, **kw) -> httpx.Response:
    """Dataverse Web API v9.2 on the environment URL; `path` like 'bots?$select=...'."""
    need("ENVIRONMENT_URL")
    token = device_code_token([f"{ENVIRONMENT_URL}/.default"])
    headers = {"Authorization": f"Bearer {token}", "OData-MaxVersion": "4.0", "OData-Version": "4.0",
               "Accept": "application/json", "Prefer": 'odata.include-annotations="*"'}
    return httpx.request(method, f"{ENVIRONMENT_URL}/api/data/v9.2/{path}", headers=headers, timeout=60, **kw)


def write_env(key: str, value: str) -> None:
    """Upsert KEY=value into the track-root .env so later labs can read it."""
    path = Path(ENV_PATH)
    text = path.read_text() if path.exists() else ""
    line = f"{key}={value}"
    if re.search(rf"^{re.escape(key)}=.*$", text, flags=re.M):
        text = re.sub(rf"^{re.escape(key)}=.*$", line, text, flags=re.M)
    else:
        text = text.rstrip("\n") + ("\n" if text else "") + line + "\n"
    path.write_text(text)
    os.environ[key] = value
    print(f"  .env  {key}={value}")


def show(label: str, obj) -> None:
    print(f"{label:<28} {json.dumps(obj, default=str)[:300]}")
