"""Read the ticket agent's `bot` row from Dataverse and print the fields that carry model and generative settings.

Proves: the "model" is agent configuration stored in Dataverse (the `bot` table), not a deployment you own; the
same row is what `pac copilot clone` turns into YAML. Column names for the model setting are marked verify.
"""
import json
import sys

from _common import AGENT_ID, AGENT_SCHEMA_NAME, dataverse, need

MODEL_HINTS = ("model", "gpt", "claude", "reason", "generative", "orchestrat")   # substrings to surface, verify exact keys


def find_bot(dv):
    if AGENT_ID:
        return dv.get(f"/bots({AGENT_ID})").raise_for_status().json()
    need("AGENT_SCHEMA_NAME")
    r = dv.get("/bots", params={"$filter": f"schemaname eq '{AGENT_SCHEMA_NAME}'", "$top": "1"}).raise_for_status().json()
    if not r["value"]:
        sys.exit(f"no bot with schemaname {AGENT_SCHEMA_NAME}")
    return r["value"][0]


def walk(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]")
    else:
        yield path, obj


def main() -> None:
    dv = dataverse()
    bot = find_bot(dv)
    print(f"bot {bot.get('name')}  schema {bot.get('schemaname')}  id {bot.get('botid')}")
    print(f"published: {bot.get('publishedon')}  language {bot.get('language')}")
    cfg_raw = bot.get("configuration")                      # verify: JSON string column holding agent settings
    if not cfg_raw:
        print("no `configuration` column on this row; print all columns and look for the model setting:")
        print(json.dumps({k: v for k, v in bot.items() if not k.startswith("@")}, indent=1)[:3000])
        return
    cfg = json.loads(cfg_raw) if isinstance(cfg_raw, str) else cfg_raw
    hits = [(p, v) for p, v in walk(cfg) if any(h in p.lower() for h in MODEL_HINTS)]
    print(f"\n{len(hits)} configuration fields that look model-related:")
    for p, v in hits:
        print(f"  {p} = {v}")
    print("\nThe primary model you see in Settings > Generative AI should appear above; if it does not, the setting is"
          " stored on a botcomponent row (verify) and `pac copilot clone` is the reliable way to read it.")


if __name__ == "__main__":
    main()
