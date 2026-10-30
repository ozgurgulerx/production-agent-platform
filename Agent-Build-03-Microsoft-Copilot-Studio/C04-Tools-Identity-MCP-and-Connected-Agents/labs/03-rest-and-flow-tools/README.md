# 03 — REST tool, approval flow, Dataverse MCP, prompt tool

**Start with the failure.** Import a tidy OpenAPI **3.0** file as a REST tool: rejected. REST API tools take OpenAPI **v2** only (D8). Convert, import, and it works. Then ask for a 400 GBP refund: the tool returns `ESCALATE` and nothing happens, because a tool cannot wait for a human; a flow can.

## Goal
Expose the ticket API as a REST tool, put a human approval in front of refunds above 250 with an agent flow, know what the Dataverse MCP server gives you for free, and see where a prompt tool fits.

## You will end with
- `TICKET_API_BASE` in `.env`; the REST tool answering `get_ticket` through the API-key connection
- an agent flow `Refund approval` that pauses on request-information for > 250 and resumes with the supervisor's answer
- a note on the Dataverse MCP tools your agent could call against its own environment, and the billing line
- one prompt tool that classifies ticket tone

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
cd 03-rest-and-flow-tools
uvicorn ticket_api.app:app --port 8001 &                # local check of the API behind openapi-v2.json
curl -s -H 'X-API-Key: dev' localhost:8001/tickets/1042
# deploy the same app to Container Apps as in lab 02 (az containerapp up --source ticket_api --target-port 8001), then set TICKET_API_BASE in .env
```
Then follow `agent_flow_refund_approval.md`, `dataverse_mcp.md`, `prompt_tool.md`.

## Facts that matter (reading map)
- D8: REST API tool (preview): None / API key / OAuth 2.0 with "which M365 org" and "which client app" restrictions; OpenAPI v2 required.
- A7, B2: agent flows (Standard) / workflows (GitHub harness): async responses beyond 2 minutes, request-information for human input, agent node, Copilot node.
- D6, D7: Dataverse MCP server `https://{org}.crm.dynamics.com/api/mcp`, 15 tools; the Copilot Studio connector lists 11; billed for non-Copilot-Studio clients since 15 Dec 2025.
- K4: prompt tools can use a BYO Foundry chat-completions deployment (GA); GPT-5 family and Responses endpoints not supported.

## Proof (checklist)
- [ ] the OpenAPI 3 import failed and the v2 import succeeded (keep the message)
- [ ] REST tool `get_ticket` returns ticket 1042 in the test pane; the connection asked the user for the API key
- [ ] "Refund 400 pounds on 1042" triggers the flow, a Teams approval card reaches the supervisor, the agent resumes with the decision
- [ ] the Dataverse MCP tool list is visible in the agent (or the note explains why it is not enabled in this environment)
- [ ] the prompt tool classifies "I was charged twice, this is the third time" as `angry`

## Next
`../04-connected-agents/` — Foundry, A2A and SDK agents as connected agents.
