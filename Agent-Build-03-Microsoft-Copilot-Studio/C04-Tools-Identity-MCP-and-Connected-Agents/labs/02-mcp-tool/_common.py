"""Shared helpers for the C04 labs: device-code sign-in (no secrets), Power Platform API, Dataverse, Graph, .env writer.

Every lab folder carries an identical copy so it stays self-contained. Tokens are cached in `.msal_cache.json`
next to the script (gitignored). Scopes: Power Platform API `https://api.powerplatform.com/.default`,
Dataverse `{ENVIRONMENT_URL}/.default`, Graph `https://graph.microsoft.com/.default`.
"""
import json
import os
import re
import sys
from pathlib import Path

import httpx
import msal
from dotenv import load_dotenv

_TRACK_ROOT = Path(__file__).resolve().parents[3]   # track root, where .env lives (never walk up past it)
ENV_PATH = _TRACK_ROOT / ".env"
load_dotenv(ENV_PATH)
HERE = Path(__file__).resolve().parent

TENANT_ID = os.environ.get("TENANT_ID", "")
CLIENT_ID = os.environ.get("CLIENT_ID", "")
ENVIRONMENT_ID = os.environ.get("ENVIRONMENT_ID", "")
ENVIRONMENT_URL = os.environ.get("ENVIRONMENT_URL", "").rstrip("/")
PP_API = os.environ.get("POWER_PLATFORM_API", "https://api.powerplatform.com").rstrip("/")
AGENT_SCHEMA_NAME = os.environ.get("AGENT_SCHEMA_NAME", "")
AGENT_ID = os.environ.get("AGENT_ID", "")

PP_SCOPE = [f"{PP_API}/.default"]
GRAPH_SCOPE = ["https://graph.microsoft.com/.default"]
DATAVERSE_SCOPE = [f"{ENVIRONMENT_URL}/.default"] if ENVIRONMENT_URL else []
D2E_SCOPE = [f"{PP_API}/CopilotStudio.Copilots.Invoke"]


def need(*names: str) -> None:
    missing = [n for n in names if not os.environ.get(n)]
    if missing:
        sys.exit(f"missing in .env: {', '.join(missing)} (see labs-setup/00-setup and the earlier labs)")


def _app() -> msal.PublicClientApplication:
    need("TENANT_ID", "CLIENT_ID")
    cache = msal.SerializableTokenCache()
    cache_file = HERE / ".msal_cache.json"
    if cache_file.exists():
        cache.deserialize(cache_file.read_text())
    app = msal.PublicClientApplication(CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}", token_cache=cache)
    app._lab_cache_file, app._lab_cache = cache_file, cache   # type: ignore[attr-defined]
    return app


def device_code_token(scopes: list[str]) -> str:
    """Interactive once per scope set; silent from the cache afterwards. Never a client secret."""
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
    if app._lab_cache.has_state_changed:   # type: ignore[attr-defined]
        app._lab_cache_file.write_text(app._lab_cache.serialize())   # type: ignore[attr-defined]
    return result["access_token"]


def _client(scopes: list[str], base: str) -> httpx.Client:
    return httpx.Client(base_url=base, headers={"Authorization": f"Bearer {device_code_token(scopes)}",
                                                "Accept": "application/json"}, timeout=60)


def pp_api() -> httpx.Client:
    """Power Platform API (copilotstudio namespace, evaluation, quarantine, inventory)."""
    return _client(PP_SCOPE, PP_API)


def dataverse() -> httpx.Client:
    """Dataverse Web API v9.2 for the environment in .env (bot, botcomponent, conversationtranscript)."""
    need("ENVIRONMENT_URL")
    c = _client(DATAVERSE_SCOPE, f"{ENVIRONMENT_URL}/api/data/v9.2")
    c.headers.update({"OData-MaxVersion": "4.0", "OData-Version": "4.0"})
    return c


def graph(method: str, path: str, **kwargs) -> dict:
    """One Microsoft Graph call; path starts with /v1.0 or /beta."""
    with _client(GRAPH_SCOPE, "https://graph.microsoft.com") as c:
        r = c.request(method, path, **kwargs)
        if r.status_code >= 400:
            sys.exit(f"graph {method} {path} -> {r.status_code} {r.text[:400]}")
        return r.json() if r.content else {}


def write_env(key: str, value: str) -> None:
    """Upsert KEY=value in the track-root .env so the next lab can read it."""
    text = ENV_PATH.read_text() if ENV_PATH.exists() else ""
    line = f"{key}={value}"
    if re.search(rf"^{re.escape(key)}=.*$", text, flags=re.M):
        text = re.sub(rf"^{re.escape(key)}=.*$", line, text, flags=re.M)
    else:
        text = text.rstrip("\n") + f"\n{line}\n"
    ENV_PATH.write_text(text)
    os.environ[key] = value
    print(f"  .env  {key}={value}")


def show(label: str, obj) -> None:
    print(f"{label:<28} {json.dumps(obj, default=str)[:220]}")
