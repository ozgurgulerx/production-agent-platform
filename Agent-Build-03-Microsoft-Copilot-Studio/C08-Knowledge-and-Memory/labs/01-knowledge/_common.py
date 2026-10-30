"""Shared helpers for the C08 lab: device-code sign-in (no secrets), Graph and Power Platform API calls, .env writer.

The .env lives at the track root and is found by path, never by walking up (a stray .env exists above the repo).
Tokens are cached in .msal_cache.json next to this file; that file is gitignored.
"""

import json
import os
import sys
from pathlib import Path

import httpx
import msal
from dotenv import load_dotenv, set_key

_TRACK_ROOT = (
    Path(__file__).resolve().parents[3]
)  # track root, where .env lives (never walk up past it)
ENV_PATH = str(_TRACK_ROOT / ".env")
load_dotenv(ENV_PATH)
HERE = Path(__file__).resolve().parent

TENANT_ID = os.environ.get("TENANT_ID", "")
CLIENT_ID = os.environ.get("CLIENT_ID", "")
ENVIRONMENT_ID = os.environ.get("ENVIRONMENT_ID", "")
AGENT_SCHEMA_NAME = os.environ.get("AGENT_SCHEMA_NAME", "")
SHAREPOINT_SITE_URL = os.environ.get("SHAREPOINT_SITE_URL", "")
POWER_PLATFORM_API = os.environ.get(
    "POWER_PLATFORM_API", "https://api.powerplatform.com"
)

GRAPH = "https://graph.microsoft.com/v1.0"
GRAPH_SCOPES = ["https://graph.microsoft.com/.default"]
PP_API_SCOPES = [
    "https://api.powerplatform.com/.default"
]  # CopilotStudio.Copilots.Invoke is delegated under this audience
D2E_SCOPES = [
    "https://api.powerplatform.com/CopilotStudio.Copilots.Invoke"
]  # verify: audience for Direct-to-Engine (C8)

POLICY_QUESTIONS = [
    "Can I refund £300 to a customer's new card?",
    "Do customers still need a travel notice?",
    "What is the capital of Peru?",  # not in the documents: the correct answer is a refusal
]


def need(*names: str) -> None:
    missing = [n for n in names if not os.environ.get(n)]
    if missing:
        sys.exit(
            f"missing in .env: {', '.join(missing)} (see labs-setup/00-setup/README.md)"
        )


def _app() -> msal.PublicClientApplication:
    need("TENANT_ID", "CLIENT_ID")
    cache = msal.SerializableTokenCache()
    cache_file = HERE / ".msal_cache.json"
    if cache_file.exists():
        cache.deserialize(cache_file.read_text())
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        token_cache=cache,
    )
    app._lab_cache_file = cache_file  # type: ignore[attr-defined]
    return app


def device_code_token(scopes: list[str]) -> str:
    """Interactive once per scope set; silent from the local cache afterwards. Never a client secret."""
    app = _app()
    accounts = app.get_accounts()
    result = app.acquire_token_silent(scopes, account=accounts[0]) if accounts else None
    if not result:
        flow = app.initiate_device_flow(scopes=scopes)
        if "user_code" not in flow:
            sys.exit(f"device flow failed: {json.dumps(flow)[:300]}")
        print(flow["message"])  # go to the URL, enter the code
        result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        sys.exit(f"token error: {result.get('error_description', result)}")
    app._lab_cache_file.write_text(app.token_cache.serialize())  # type: ignore[attr-defined]
    return result["access_token"]


def graph(method: str, path: str, token: str | None = None, **kwargs) -> httpx.Response:
    """One Graph v1.0 call. `path` starts with '/'. Raises on 4xx/5xx with the Graph error body."""
    token = token or device_code_token(GRAPH_SCOPES)
    headers = {"Authorization": f"Bearer {token}", **kwargs.pop("headers", {})}
    r = httpx.request(method, f"{GRAPH}{path}", headers=headers, timeout=60, **kwargs)
    if r.status_code >= 400:
        sys.exit(f"Graph {method} {path} -> {r.status_code}: {r.text[:400]}")
    return r


def pp_api(
    method: str, path: str, token: str | None = None, **kwargs
) -> httpx.Response:
    """One Power Platform API call (api.powerplatform.com). Used by C05/C09; here for symmetry."""
    token = token or device_code_token(PP_API_SCOPES)
    headers = {"Authorization": f"Bearer {token}", **kwargs.pop("headers", {})}
    r = httpx.request(
        method, f"{POWER_PLATFORM_API}{path}", headers=headers, timeout=60, **kwargs
    )
    if r.status_code >= 400:
        sys.exit(
            f"Power Platform API {method} {path} -> {r.status_code}: {r.text[:400]}"
        )
    return r


def write_env(key: str, value: str) -> None:
    """Upsert KEY=value in the track-root .env so the next script finds it."""
    set_key(ENV_PATH, key, value)
    os.environ[key] = value
    print(f"  .env  {key}={value}")
