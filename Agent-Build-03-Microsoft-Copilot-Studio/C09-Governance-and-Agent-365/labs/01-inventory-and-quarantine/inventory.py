"""List every Copilot Studio agent the admin can see, with the three risk fields first (E7).

Proves: the inventory exists outside the maker portal; authentication mode, tenant-wide sharing and
maker-credential tools are readable fields, not opinions. Two sources, same data: Azure Resource Graph
(type microsoft.copilotstudio/agents) and the Power Platform API inventory. Read-only; nothing to revert.
"""
import argparse
import json

from _common import ENVIRONMENT_ID, AGENT_ID, arm, pp_api, show

RISK_FIELDS = ("authenticationMode", "entireTenant", "sharedWithCount", "isQuarantined", "entraAgentId", "channels")
ARG_QUERY = """
resources
| where type =~ 'microsoft.copilotstudio/agents'
| project name, id, environmentId = tostring(properties.environmentId), props = properties
"""   # verify: property names once the first row prints (print(json.dumps(row)) below)


def via_resource_graph() -> list[dict]:
    with arm() as c:
        r = c.post("/providers/Microsoft.ResourceGraph/resources", params={"api-version": "2022-10-01"},
                   json={"query": ARG_QUERY, "options": {"resultFormat": "objectArray"}})
        body = show("resource graph", r)
    return body.get("data", [])


def via_power_platform_api() -> list[dict]:
    with pp_api() as c:
        r = c.get(f"/copilotstudio/environments/{ENVIRONMENT_ID}/bots", params={"api-version": "2022-03-01-preview"})  # verify path (C6)
        body = show("power platform api", r)
    return body.get("value", [])


def print_row(row: dict) -> None:
    props = row.get("props") or row.get("properties") or row
    tools = props.get("tools") or props.get("actions") or []
    maker_tools = [t.get("name") for t in tools if str(t.get("connectionProvider", "")).lower() == "maker"]
    flags = []
    if str(props.get("authenticationMode", "")).lower() in ("none", "noauth", ""):
        flags.append("NO-AUTH")
    if props.get("entireTenant"):
        flags.append("TENANT-WIDE")
    if maker_tools:
        flags.append(f"MAKER-CREDS:{','.join(maker_tools)}")
    mark = " <== ticket agent" if AGENT_ID and AGENT_ID in json.dumps(row) else ""
    print(f"- {row.get('name') or props.get('displayName')}: {', '.join(flags) or 'ok'}  "
          f"{ {k: props.get(k) for k in RISK_FIELDS if k in props} }{mark}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["arg", "ppapi", "both"], default="both")
    ap.add_argument("--raw", action="store_true", help="print the first row verbatim to learn the property names")
    args = ap.parse_args()
    rows = []
    if args.source in ("arg", "both"):
        rows += via_resource_graph()
    if args.source in ("ppapi", "both"):
        rows += via_power_platform_api()
    if args.raw and rows:
        print(json.dumps(rows[0], indent=1)[:3000])
    print(f"\n{len(rows)} agents. Three fields first: authentication mode, tenant-wide share, maker-credential tools.")
    for row in rows:
        print_row(row)
