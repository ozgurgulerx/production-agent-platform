# C09 labs — govern reach: inventory, DLP, Agent 365

Runnable proofs for the C09 chapter. Setup is shared: [`../../labs-setup/`](../../labs-setup/) (venv, `.env` at the track root, device-code app registration). These labs assume the ticket agent from C03 lab 01 (`AGENT_ID`, `ENVIRONMENT_ID`) and the MCP tool from C04 lab 02 (`TICKET_MCP_URL`). The user has tenant admin; lab 02 changes a DLP policy and reverts it in the same session. Nothing here has run yet; every proof checklist is unticked.

```
labs/
├── 01-inventory-and-quarantine/   list every agent with the three risk fields → quarantine the ticket agent → release
├── 02-dlp-and-environment-rules/  block the HTTP virtual connector → publish disables → unblock; ACP pre-approval; group rules; credit caps
└── 03-agent-365-and-purview/      registry block / reassign, Tooling Gateway with APIM, BYO MCP approval, Purview audit pull, CMK, firewall, Defender
```

| Lab | Chapter section | Changes in the tenant | Revert | Time |
|---|---|---|---|---|
| 01 | §2 | quarantines one agent | `quarantine.py --off` | 30 min |
| 02 | §3, §4, §8 | one DLP policy edit, one environment-group rule | documented in each README | 1 session |
| 03 | §7, §8 | registry block on one agent (optional) | unblock in the same page | 1 session |

```bash
source ../../labs-setup/.venv/bin/activate
cd 01-inventory-and-quarantine && python inventory.py
```

Scopes: the public-client app registration from `labs-setup/00-setup` needs the delegated Power Platform API scopes `CopilotStudio.Copilots.Invoke` and `CopilotStudio.AdminActions.Invoke`, Azure Resource Graph via `https://management.azure.com/.default`, and Microsoft Graph `AuditLog.Read.All` for lab 03. Admin consent once.
