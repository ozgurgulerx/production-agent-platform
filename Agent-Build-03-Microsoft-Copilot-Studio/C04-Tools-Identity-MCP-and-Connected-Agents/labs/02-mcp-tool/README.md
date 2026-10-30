# 02 — The ticket MCP server as a Copilot Studio tool

**Start with the failure.** Paste the server's old `/sse` URL into the MCP wizard: it is rejected, because Copilot Studio dropped SSE in Aug 2025 and accepts Streamable HTTP only (D3). Next, point the wizard at a server that exposes 130 tools: the agent is over the 128-tool limit (D1). Last, add the real server, leave "Allow all" off, and ask for a refund: the planner cannot see `issue_refund` because its toggle is off (D4). Three failures, all about the contract, none about your code.

## Goal
Host the four-tool ticket server on HTTPS (Container Apps), add it to the ticket agent three times with three auth modes, add it once more as a custom connector from an OpenAPI 2.0 file, and prove the per-tool allow-list.

## You will end with
- `TICKET_MCP_URL` in `.env`, `smoke_mcp.py` listing exactly four tools
- the agent answering a ticket question through the MCP tool, visible in the activity trace
- three connections (None, API key, OAuth manual) and a note of what each stored
- the custom connector imported from `custom_connector/openapi.yaml`
- an allow-list transcript: refund refused with `issue_refund` off, performed with it on

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
cd 02-mcp-tool
python mcp_server/main.py &                       # local smoke on :8000/mcp; Ctrl-C after
TICKET_MCP_URL=http://localhost:8000/mcp python smoke_mcp.py
bash mcp_server/deploy_container_apps.sh          # az containerapp up → HTTPS FQDN; writes TICKET_MCP_URL
python smoke_mcp.py                               # same four tools over HTTPS
```
Then `add_via_wizard.md` (three passes), `custom_connector/README.md`, `allow_list.md`.

## Facts that matter (reading map)
- D3: wizard auth None / API key (user supplies at run time) / OAuth 2.0 dynamic discovery, dynamic, manual; Streamable HTTP only; remote only.
- D2, D4: tools and resources, not prompts; dynamic refresh; "Allow all" or per-tool toggles with new tools off; generative orchestration required.
- D1: 128 tools per agent, 25–30 recommended, each child agent its own 128.
- F1: MCP rides on connectors, so a DLP policy that blocks the connector removes the tools and disables publish.
- D5: the GitHub harness adds the server from a gallery or a URL, negotiates the tool list on add, and shows an activity trace per call.

## Proof (checklist)
- [ ] the `/sse` URL was rejected by the wizard (keep the message)
- [ ] `smoke_mcp.py` prints `tools: ['get_ticket', 'list_tickets', 'get_policy', 'issue_refund']` against `TICKET_MCP_URL`
- [ ] the agent answers "what is ticket 1042 about?" via the MCP tool; the activity map shows the tool call
- [ ] API-key pass: the connection prompted the user for the key (not stored by the maker)
- [ ] OAuth manual pass: a sign-in card appeared once; the second question did not prompt
- [ ] with `issue_refund` toggled off the agent declines to refund; toggled on, `issue_refund` returns `REFUNDED` for 1042 and `ESCALATE` for 400 GBP

## Next
`../03-rest-and-flow-tools/` — the same API as a REST tool, and the approval flow above 250.
