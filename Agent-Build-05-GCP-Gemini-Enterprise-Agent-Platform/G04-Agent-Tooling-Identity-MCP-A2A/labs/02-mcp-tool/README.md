# 02 — `McpToolset` to a ticketing MCP server, with the refund-policy callback

## Goal
Give `ticket-agent` the ticketing tools through `McpToolset` (map D3), prove a tool call round-trips under `adk web`, narrow what the model sees with `tool_filter`, and refuse "refund outside policy" in a `before_tool_callback` (map B4) rather than in the prompt. The MCP server is MCP Toolbox for Databases run locally over stdio against a local Postgres; lab 03 moves the same `tools.yaml` to Cloud Run.

## Steps
```bash
source ../../../labs-setup/.venv/bin/activate
set -a; source ../../../.env; set +a
brew install mcp-toolbox                                    # 1.15.0 (map D6)
toolbox --version

# 1. A local Postgres with the tickets table (any Postgres you have; Docker shown).
docker run -d --name tickets-pg -e POSTGRES_PASSWORD=tickets -e POSTGRES_DB=tickets -p 5432:5432 postgres:16
psql postgresql://postgres:tickets@localhost:5432/tickets -f ../03-mcp-toolbox/schema.sql
export TICKETS_DB_HOST=localhost TICKETS_DB_PORT=5432 TICKETS_DB_NAME=tickets TICKETS_DB_USER=postgres TICKETS_DB_PASSWORD=tickets

# 2. Run the Toolbox once in the foreground to see the tools load, then stop it; ticket_agent/agent.py starts it over stdio.
toolbox --config ../03-mcp-toolbox/tools.yaml --ui              # --ui is the 1.15.0 flag (map D6); Ctrl-C after it lists tools

# 3. Run the agent. ticket_agent/agent.py builds McpToolset(StdioConnectionParams(toolbox --stdio --config ...)) at import time (map D3).
adk web --port 8000      # from this lab folder; pick ticket_agent in the dropdown
# ask: "What is the status of ticket 1002?"  -> lookup_ticket call visible in the Events tab
# ask: "Refund ticket 1002 in full"           -> the callback answers, no tool runs

# 4. Second client, same server: Gemini CLI (map H6). Add to ~/.gemini/settings.json:
#   {"mcpServers": {"tickets": {"command": "toolbox", "args": ["--stdio", "--config", "<abs>/03-mcp-toolbox/tools.yaml"]}}}
gemini   # then /mcp  -> lists lookup_ticket, my_open_tickets
```

## What to write
- `ticket_agent/agent.py`: the `tool_filter` list and the `refuse_refund_outside_policy` callback body. The callback receives the tool, its args and the context; return a dict to short-circuit the call, `None` to allow it (map B4). Policy: refunds are allowed only when `amount <= 50` and the ticket was opened within 30 days; anything else returns `{"status": "refused", "reason": ...}` and the agent explains.
- `test_02_mcp_tool.py`: unit tests for the callback with a fake tool call; one integration test (skipped without the Toolbox) that the toolset lists exactly the filtered tools.

## Expected output
`adk web` Events show a `lookup_ticket` function call with `{"ticket_id": 1002}` and a response row from the table. The refund request produces no tool call; the final text quotes the policy. Gemini CLI `/mcp` lists the two tools. If the toolset shows zero tools, the Toolbox process did not start: `McpToolset` must be constructed synchronously at module level, and there is no auto-reconnect after a session restore (map D3).

## Proof checklist
- [ ] `toolbox --config ... --ui` lists `lookup_ticket` and `my_open_tickets`
- [ ] `adk web` Events tab shows one `lookup_ticket` call and its result
- [ ] "Refund ticket 1002 in full" produces no tool call and the callback's reason appears in the answer
- [ ] `tool_filter` removes `my_open_tickets` when you set it to `["lookup_ticket"]` and the tool list shrinks
- [ ] Gemini CLI `/mcp` lists the same tools from the same `tools.yaml`
- [ ] `pytest test_02_mcp_tool.py` runs the callback tests (integration test skipped is fine)

## Cleanup
`docker rm -f tickets-pg`. Keep `tools.yaml` and `schema.sql` in lab 03; they deploy unchanged.

## Next
`../03-mcp-toolbox/` — the same server on Cloud Run with Google auth; produces `TICKET_MCP_URL`.
