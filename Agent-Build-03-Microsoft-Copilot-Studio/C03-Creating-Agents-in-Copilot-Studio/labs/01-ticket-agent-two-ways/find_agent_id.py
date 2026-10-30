"""Find the ticket agent's Dataverse row by schema name and write AGENT_ID to .env.

Proves: an agent is a `bot` row in Dataverse (C6); the schema name from Settings > Advanced > Metadata is the
stable handle that pac, the client library and the evaluation API all use.
"""
from _common import AGENT_SCHEMA_NAME, dataverse, need, show, write_env

need("AGENT_SCHEMA_NAME")
r = dataverse("GET", f"bots?$select=botid,name,schemaname,statecode,publishedon&$filter=schemaname eq '{AGENT_SCHEMA_NAME}'")
r.raise_for_status()
rows = r.json().get("value", [])
if not rows:
    raise SystemExit(f"no bot with schemaname {AGENT_SCHEMA_NAME} in {dataverse.__module__}; create it in the portal first")
bot = rows[0]
show("bot", bot)
write_env("AGENT_ID", bot["botid"])
print("published on:", bot.get("publishedon") or "never (publish before invoking from code)")
