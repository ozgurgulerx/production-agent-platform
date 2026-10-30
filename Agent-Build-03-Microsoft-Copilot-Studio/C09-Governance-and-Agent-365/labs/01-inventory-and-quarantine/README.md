# 01 — Inventory and quarantine

The first deliverable of any Copilot Studio review is the list. This lab prints every agent the admin can see with the three risk fields first, then quarantines the ticket agent and releases it.

## Start with the failure
Ask a maker for the list of agents in the tenant. You get a screenshot of their own maker portal. Ask which agents run tools on maker credentials. Nobody knows. That is the gap the inventory closes (E7).

## Prerequisites
`labs-setup/` done; `.env` has `TENANT_ID`, `CLIENT_ID`, `ENVIRONMENT_ID`, `AGENT_ID` (C03 lab 01). The app registration needs delegated `CopilotStudio.AdminActions.Invoke` on the Power Platform API and `https://management.azure.com/user_impersonation` for Resource Graph. You need a Power Platform admin, AI admin or Global admin role for quarantine.

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
python inventory.py --raw          # first row verbatim, to learn the property names; then without --raw
python quarantine.py --on          # channels go dark, maker test pane still answers
python quarantine.py --off         # revert
```

## What each script proves
- **inventory.py** The same agents appear in Azure Resource Graph as `microsoft.copilotstudio/agents` and in the Power Platform API; authentication mode, tenant-wide share and maker-credential tools are fields. Property names are marked `# verify`; use `--raw` once and fix the constants.
- **quarantine.py** One POST stops every channel; the maker pane keeps working; `isQuarantined` flips (inventory refresh about 20 minutes).

## Proof checklist
- [ ] `inventory.py` lists the ticket agent with `authenticationMode`, sharing scope and tool credential providers
- [ ] at least one other agent in the tenant shows a flag (NO-AUTH, TENANT-WIDE or MAKER-CREDS), or you can say why none does
- [ ] after `--on`, a Teams or web-chat message to the ticket agent fails and the maker test pane still answers
- [ ] after `--off`, the channel answers again; `isQuarantined` is false
- [ ] you can name the three fields you check first without looking
