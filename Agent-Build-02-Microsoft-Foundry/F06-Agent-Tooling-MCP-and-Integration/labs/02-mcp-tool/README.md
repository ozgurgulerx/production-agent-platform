# 07 — A remote MCP server as a Foundry tool (Logic Apps Standard as the host)


**Start with the failure.** Before adding the tool, ask the F03 prompt agent "what is the status of ticket 1042?". It answers confidently and wrongly, because it has nothing to look at. Run this lab, ask again, and keep both transcripts in the proof. The contrast is the whole argument for tools.

## Goal
Attach a remote MCP server to a Foundry agent with the current `mcp` tool and drive the approval loop. Logic Apps Standard is the host used in the narrative because it turns connector-backed workflows into MCP tools without code (`https://<app>.azurewebsites.net/api/mcpservers/<name>/mcp`), but **Foundry has no "Logic Apps tool"**: whatever hosts the MCP server (Logic Apps, Functions, Container Apps, APIM) is invisible to the agent.

## You will end with
- `ticket-agent-mcp`, a prompt agent with one `mcp` tool (`server_label`, `server_url`, `require_approval`, optional `project_connection_id`)
- a transcript showing `mcp_list_tools` → `mcp_approval_request` → `mcp_approval_response` → `mcp_call` → answer

## Run
```bash
source ../.venv/bin/activate
python mcp_tool_demo.py                                   # public Learn MCP server, no auth
LOGIC_APP_MCP_URL=https://<app>.azurewebsites.net/api/mcpservers/ticketing/mcp MCP_CONNECTION_NAME=la-ticketing python mcp_tool_demo.py
```
The connection (`azd ai connection create la-ticketing --kind remote-tool --target <url> --auth-type custom-keys --custom-key "x-api-key=<key>"`) holds the credential; the tool only references it. See 09 for the six auth types.

## Facts that matter
- `require_approval` defaults to `always`; each call pauses as an `mcp_approval_request` item that your code answers with `McpApprovalResponse` and `previous_response_id`. `{"never": {"tool_names": [...]}}` whitelists read-only tools.
- A non-streaming tool call has 100 s; long tools need MCP tasks + background mode (preview).
- 128 tools per agent; nested `anyOf` schemas are rejected as "Invalid tool schema".
- Private servers need the Standard setup and Container Apps internal ingress on the delegated subnet.

## Proof (checklist)
- [ ] `approval requested: ticketing.<tool>(...)` printed at least once, then an `mcp_call` with no error
- [ ] the same run against your Logic Apps MCP server with a connection
- [ ] trace in the portal shows the tool span under the response

## Next
`../03-toolbox/` — several servers behind one toolbox.
