"""Find the ticket agent's Entra Agent ID in Microsoft Graph and print what publish attached to it.

Proves: the identity is a service principal (not an app registration you own), created under the Microsoft
blueprint, with delegated grants / app roles that mirror the published first-party connectors and nothing for
MCP or custom connectors (reading map E1). Writes AGENT_ENTRA_OBJECT_ID to .env.
"""
import argparse
import os

from _common import graph, need, show, write_env

BLUEPRINT_APP_ID = "25664c89-cea5-4ab6-b924-a54fd8a19ae0"


def find_sp(name: str | None, object_id: str | None) -> dict:
    if object_id:
        return graph("GET", f"/v1.0/servicePrincipals/{object_id}?$select=id,appId,displayName,createdDateTime,servicePrincipalType,tags")
    r = graph("GET", f"/v1.0/servicePrincipals?$filter=displayName eq '{name}'"
                     "&$select=id,appId,displayName,createdDateTime,servicePrincipalType,tags")
    hits = r.get("value", [])
    if not hits:
        raise SystemExit(f"no service principal named {name!r}; publish the agent once, or pass --object-id")
    if len(hits) > 1:
        print(f"  {len(hits)} principals share the name; using the newest")
        hits.sort(key=lambda s: s.get("createdDateTime", ""), reverse=True)
    return hits[0]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default=os.environ.get("AGENT_DISPLAY_NAME", "Ticket agent"))
    ap.add_argument("--object-id", default=os.environ.get("AGENT_ENTRA_OBJECT_ID") or None)
    a = ap.parse_args()
    need("TENANT_ID", "CLIENT_ID")

    bp = graph("GET", f"/v1.0/servicePrincipals?$filter=appId eq '{BLUEPRINT_APP_ID}'&$select=id,displayName").get("value", [])
    show("blueprint", bp[0] if bp else "not present yet (appears with the first agent)")

    sp = find_sp(a.name, a.object_id)
    show("agent principal", {k: sp.get(k) for k in ("id", "appId", "displayName", "createdDateTime", "servicePrincipalType")})
    write_env("AGENT_ENTRA_OBJECT_ID", sp["id"])

    try:   # verify: relationship name on the beta surface
        sponsors = graph("GET", f"/beta/servicePrincipals/{sp['id']}/sponsors?$select=displayName,userPrincipalName").get("value", [])
        show("sponsors", [s.get("userPrincipalName") or s.get("displayName") for s in sponsors])
    except SystemExit as e:
        print("  sponsors: not readable on this surface", str(e)[:80])

    grants = graph("GET", f"/v1.0/servicePrincipals/{sp['id']}/oauth2PermissionGrants").get("value", [])
    for g in grants:
        res = graph("GET", f"/v1.0/servicePrincipals/{g['resourceId']}?$select=displayName")
        show(f"grant → {res.get('displayName', g['resourceId'])[:20]}", g.get("scope"))
    roles = graph("GET", f"/v1.0/servicePrincipals/{sp['id']}/appRoleAssignments").get("value", [])
    for r in roles:
        show("app role", {"resource": r.get("resourceDisplayName"), "roleId": r.get("appRoleId")})
    if not grants and not roles:
        print("  no grants yet: scopes are attached at publish, and only for first-party / certified connectors (E1)")
    print("\nexpected: SharePoint / Dataverse style connector scopes present; nothing for the MCP or custom connector.")


if __name__ == "__main__":
    main()
