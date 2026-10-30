"""Print the DLP classification of the HTTP virtual connector and the ticket connector for the lab environment (F1).

Proves: MCP and REST tools are governed as connectors; the classification you see here is what disables the
publish button. Read-only. The policy edit itself is done in PPAC (dlp_policy.md) and reverted there;
run this before, during and after to capture the three states.
"""
import argparse

from _common import ENVIRONMENT_ID, bap, need, show

HTTP_CONNECTOR = "shared_webcontents"            # HTTP virtual connector id; verify against Get-DlpPolicy output
NOAUTH_CONNECTOR = "shared_pvabotsnoauth"        # "Chat without Microsoft Entra ID authentication"; verify


def policies_for_environment() -> list[dict]:
    with bap() as c:
        r = c.get("/providers/PowerPlatform.Governance/v2/policies", params={"api-version": "2016-11-01"})  # verify path (DLP admin API)
        body = show("list DLP policies", r)
    out = []
    for p in body.get("value", []):
        envs = [e.get("name") for e in p.get("environments", [])]
        scope = p.get("environmentType")
        if scope == "AllEnvironments" or ENVIRONMENT_ID in envs or (scope == "ExceptEnvironments" and ENVIRONMENT_ID not in envs):
            out.append(p)
    return out


def classification(policy: dict, connector_suffix: str) -> str:
    for group in policy.get("connectorGroups", []):
        for conn in group.get("connectors", []):
            if str(conn.get("id", "")).endswith(connector_suffix):
                return group.get("classification", "?")
    return policy.get("defaultConnectorsClassification", "General (default)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticket-connector", default="shared_tickets-5fcustom", help="custom connector id suffix for the ticket API/MCP connector")
    args = ap.parse_args()
    need("ENVIRONMENT_ID")
    pols = policies_for_environment()
    print(f"\n{len(pols)} DLP policies apply to environment {ENVIRONMENT_ID}")
    for p in pols:
        print(f"- {p.get('displayName')}: HTTP={classification(p, HTTP_CONNECTOR)}  "
              f"no-auth-chat={classification(p, NOAUTH_CONNECTOR)}  ticket={classification(p, args.ticket_connector)}")
        for ep in p.get("connectorConfigurations", {}).get("endpointConfigurations", []):
            if ep.get("connectorId", "").endswith(HTTP_CONNECTOR):
                print("    HTTP endpoint rules:", [(r.get("behavior"), r.get("endpoint")) for r in ep.get("endpointRules", [])])
    print("\nBlocked HTTP + a REST/MCP tool on the agent => publish button disabled in Copilot Studio (F1).")
