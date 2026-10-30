# 01 — The agent's identity, and who a tool runs as

**Start with the failure.** Open Entra → App registrations and look for the ticket agent. It is not there. It is under Enterprise applications (service principals), created by a blueprint you do not own, and you cannot add a secret to it. If your runbook says "register an app for the bot", it is a 2024 runbook.

## Goal
See the agent's Entra Agent ID in Graph and in the inventory, read the connector scopes that publish attached, then flip one tool to maker credentials and watch the security scan react.

## You will end with
- the service principal id in `.env` (`AGENT_ENTRA_OBJECT_ID`), its `createdDateTime`, the sponsor, and the list of connector scopes
- the inventory row for the agent: `authenticationMode`, channels, `connectionProvider` per tool
- a screenshot of the security scan warning after switching a tool to maker credentials, and the reverted state

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
cd 01-identity
python inspect_agent_identity.py      # Graph: find the SP by display name (or by AGENT_ENTRA_OBJECT_ID), grants, app roles
python inventory_entry.py             # Power Platform API inventory, filtered to AGENT_ID
```
Then follow `maker_vs_user_credentials.md` in the portal, and read `conditional_access.md` and `end_user_auth_modes.md`.

## Facts that matter (reading map)
- E1: identity auto-created since May 2026; blueprint `25664c89-cea5-4ab6-b924-a54fd8a19ae0`; Standard harness at creation, GitHub harness at first publish; owner = sponsor; no BYO app registration; only the blueprint mints tokens.
- E1: scopes attached on publish only for first-party and certified connectors; MCP, custom connectors and REST tools get none.
- E1: Conditional Access on the identity is enforced only in Teams today.
- D1, E6, E7: end-user credentials by default; maker credentials flagged by the scan and visible as `connectionProvider: Maker`.
- E5: three end-user auth modes; "No authentication" disables end-user-credential tools.

## Proof (checklist)
- [ ] `inspect_agent_identity.py` prints one service principal whose display name is the agent name and whose `createdDateTime` matches the agent's creation (or first publish)
- [ ] the grants list contains the SharePoint (or other first-party) connector scope and nothing for the MCP connector
- [ ] `inventory_entry.py` shows `authenticationMode` and the tool list with `connectionProvider` values
- [ ] after switching `issue_refund` to maker credentials, the pre-publish security scan shows a warning; after reverting it is clear
- [ ] you can state in one sentence where Conditional Access on the agent applies today

## Next
`../02-mcp-tool/` — the ticket MCP server as a tool, three auth modes.
