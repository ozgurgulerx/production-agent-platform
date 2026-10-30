"""Read the ticket agent's row from Dataverse and print the fields that carry its model configuration.

Proves: the model is a property of the agent row (`bot` table), not a deployment; and Dataverse is the system of
record behind the portal. Field names that hold the model choice are inside the configuration JSON; the key is
printed by scanning for "model" so it works across schema versions (# verify the exact key in your tenant).
"""
import json, os, sys
from pathlib import Path
import httpx, msal
from dotenv import load_dotenv

_TRACK_ROOT = Path(__file__).resolve().parents[2]   # track root, where .env lives
load_dotenv(_TRACK_ROOT / ".env")
TENANT, CLIENT, ENV_URL = os.environ["TENANT_ID"], os.environ["CLIENT_ID"], os.environ["ENVIRONMENT_URL"].rstrip("/")
SCHEMA = os.environ.get("AGENT_SCHEMA_NAME") or sys.exit("AGENT_SCHEMA_NAME missing in .env (C03 lab 01 writes it)")
CACHE = Path(__file__).with_name(".msal_cache.json")

def token(scopes):
    cache = msal.SerializableTokenCache()
    if CACHE.exists():
        cache.deserialize(CACHE.read_text())
    app = msal.PublicClientApplication(CLIENT, authority=f"https://login.microsoftonline.com/{TENANT}", token_cache=cache)
    acc = app.get_accounts()
    r = app.acquire_token_silent(scopes, account=acc[0]) if acc else None
    if not r:
        flow = app.initiate_device_flow(scopes=scopes); print(flow["message"], file=sys.stderr)
        r = app.acquire_token_by_device_flow(flow)
    CACHE.write_text(cache.serialize())
    return r["access_token"]

h = {"Authorization": f"Bearer {token([f'{ENV_URL}/.default'])}", "Accept": "application/json"}
q = f"{ENV_URL}/api/data/v9.2/bots?$select=botid,name,schemaname,configuration,publishedon&$filter=schemaname eq '{SCHEMA}'"
rows = httpx.get(q, headers=h, timeout=30).raise_for_status().json()["value"]
if not rows:
    sys.exit(f"no bot with schemaname {SCHEMA}")
bot = rows[0]
print("agent:", bot["name"], bot["botid"], "published:", bot.get("publishedon"))
cfg = json.loads(bot.get("configuration") or "{}")


def flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out.update(flatten(v, f"{prefix}{k}."))
        else:
            out[f"{prefix}{k}"] = v
    return out


hits = {k: v for k, v in flatten(cfg).items() if "model" in k.lower()}
print("model-related configuration keys:" if hits else "no 'model' key in configuration JSON (default = GPT Chat Latest; # verify)")
for k, v in hits.items():
    print(f"  {k} = {v}")
