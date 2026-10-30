"""Read the ticket agent's row from the Copilot Studio agent inventory (Power Platform API).

Proves: the inventory exposes entraAgentId, authentication mode, channels, sharing counts and, per tool,
connectionProvider (User | Maker) and connectionIdSharedByMaker (reading map E7). The exact path is from the
inventory page; it is marked verify until run. Fallback: Azure Resource Graph `microsoft.copilotstudio/agents`.
"""
import json
import os
import sys

from _common import AGENT_ID, ENVIRONMENT_ID, need, pp_api, show

# verify: path and api-version from https://learn.microsoft.com/microsoft-copilot-studio/admin-agent-inventory
INVENTORY = "/copilotstudio/environments/{env}/agentinventory?api-version=2024-10-01"
ARG_QUERY = ("resources | where type =~ 'microsoft.copilotstudio/agents' "
             "| where properties.botId =~ '{agent}' | project name, properties")   # fallback, Azure Resource Graph


def main() -> None:
    need("ENVIRONMENT_ID")
    with pp_api() as c:
        r = c.get(INVENTORY.format(env=ENVIRONMENT_ID))
        if r.status_code >= 400:
            print(f"inventory call failed {r.status_code}: {r.text[:300]}\n"
                  f"fallback: run the Azure Resource Graph query below in the portal\n  {ARG_QUERY.format(agent=AGENT_ID)}")
            sys.exit(1)
        rows = r.json().get("value", r.json())
    mine = [a for a in rows if AGENT_ID and AGENT_ID.lower() in json.dumps(a).lower()] or rows[:1]
    for a in mine:
        for key in ("displayName", "entraAgentId", "authenticationMode", "channels", "isQuarantined",
                    "sharedWithCount", "connectorOperations", "tools"):
            if key in a:
                show(key, a[key])
        tools = a.get("tools") or a.get("connectorOperations") or []
        for t in tools:
            show(f"  tool {str(t.get('name', t.get('operationName', '?')))[:20]}",
                 {k: t.get(k) for k in ("connectionProvider", "connectionIdSharedByMaker") if k in t})
    print("\nexpected: connectionProvider=User on every tool; a Maker row is what the security scan warns about.")


if __name__ == "__main__":
    main()
