"""Device-code sign-in through the public-client app, then Dataverse WhoAmI and a Power Platform API token.

Proves: the app registration, consent and environment URL are right, and no secret is needed anywhere.
"""
import json, os, sys
from pathlib import Path
import httpx, msal
from dotenv import load_dotenv

_TRACK_ROOT = Path(__file__).resolve().parents[3]   # track root, where .env lives
load_dotenv(_TRACK_ROOT / ".env")
TENANT, CLIENT, ENV_URL = os.environ["TENANT_ID"], os.environ["CLIENT_ID"], os.environ["ENVIRONMENT_URL"].rstrip("/")
CACHE = Path(__file__).with_name(".msal_cache.json")

def token(scopes):
    cache = msal.SerializableTokenCache()
    if CACHE.exists():
        cache.deserialize(CACHE.read_text())
    app = msal.PublicClientApplication(CLIENT, authority=f"https://login.microsoftonline.com/{TENANT}", token_cache=cache)
    accounts = app.get_accounts()
    result = app.acquire_token_silent(scopes, account=accounts[0]) if accounts else None
    if not result:
        flow = app.initiate_device_flow(scopes=scopes)
        print(flow["message"], file=sys.stderr)
        result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        sys.exit(f"token failed: {result.get('error_description')}")
    CACHE.write_text(cache.serialize())
    return result["access_token"]

who = httpx.get(f"{ENV_URL}/api/data/v9.2/WhoAmI", headers={"Authorization": f"Bearer {token([f'{ENV_URL}/.default'])}"}, timeout=30)
who.raise_for_status()
print("  Dataverse WhoAmI:", json.dumps(who.json()))
token(["https://api.powerplatform.com/.default"])
print("  Power Platform API token acquired")
