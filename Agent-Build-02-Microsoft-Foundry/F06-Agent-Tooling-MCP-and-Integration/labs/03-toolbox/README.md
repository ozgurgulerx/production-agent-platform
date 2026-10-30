# 08 — Connector-backed MCP servers behind one toolbox

## Goal
Bundle several MCP servers (your ServiceNow and Salesforce Logic Apps servers, or the public stand-ins) plus web search and tool search into a **toolbox**: one versioned MCP endpoint with credentials injected from project connections. The agent attaches the toolbox as a single `mcp` tool.

## Run
```bash
source ../.venv/bin/activate
python toolbox_demo.py                                    # public servers
SERVICENOW_MCP_URL=... SERVICENOW_CONNECTION_NAME=sn-conn SALESFORCE_MCP_URL=... SALESFORCE_CONNECTION_NAME=sf-conn python toolbox_demo.py
```
Equivalent azd: declare `host: azure.ai.toolbox` with `tools:` in `azure.yaml` (see F03 `labs/02-hosted-agents` and the upstream `04-foundry-toolbox` sample), or `azd ai toolbox create ticket-tools --from-file toolbox.yaml`.

## What the toolbox does and does not do
Does: one endpoint (`/toolboxes/{name}/mcp` serves the promoted default version, `/versions/{v}/mcp` a pinned one), credential injection from connections, immutable versions you promote without touching agents, guardrails (`rai_policy_name`), tool search (`tool_search` + `call_tool` meta-tools, GA Sept 2026), skills (preview).
Does not: run your tool code, rate-limit or IP-restrict (APIM does), or enforce `require_approval` (the consuming agent does). Hosted-agent toolboxes are GA; prompt-agent toolboxes are public preview.

## Proof (checklist)
- [ ] `toolbox ticket-tools v1` created and the agent's `mcp_list_tools` shows the meta-tools
- [ ] answer cites a tool result from one of the servers
- [ ] v2 created; the agent still works without redeploy; promote v2 in the portal and re-run

## Next
`../04-mcp-auth-apim/` — who the server sees: the six auth types, and APIM in front.
