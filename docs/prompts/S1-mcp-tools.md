# Stage 3a — support-tickets MCP server (SPEC)

## 1. What we are building, in one paragraph
A small MCP server called `support-tickets`. An MCP server is a program that exposes a few functions ("tools") over a standard protocol so that an AI model can discover and call them. This one exposes three read-only tools over two JSON files: the support tickets you used in today's Python exercise, and five short refund policies. Tonight nothing calls it except a test and the MCP Inspector (a browser tool for calling a server by hand). Tomorrow an Agents SDK agent will call these same three tools to answer questions like "what is the refund status for T-1001 and which policy applies?".

## 2. Why this exists
- It is the first brick of A3, the agent on Azure that is your production evidence. Every later stage (agent, guardrails, evals, tracing, APIM + OAuth on Azure) attaches to these three tools without changing them.
- It un-suspends the Anki card "Created any MCP tools? Walk me through your server" (reported at Oracle Health and Cymax).
- It is tonight's agent-assisted PR: Claude Code types, you drive and review every line.

## 3. The data
`data/tickets.json` — 8 support tickets, same file as the R0 exercise. Fields: `id`, `customer_id`, `created_at`, `priority`, `status`, `subject`, optional `tags`, optional `amount_disputed`.

`data/policies.json` — 5 refund/dispute/data policies, each `{id, title, text}`. Ids: `POL-REFUND-01` (30-day window), `POL-REFUND-02` (original payment method only), `POL-REFUND-03` (over 500 GBP needs supervisor approval), `POL-DISPUTE-01` (5 working days), `POL-DATA-01` (never show card or NI numbers). These are what the agent will quote when it explains a decision. Both files are provided in this folder.

## 4. The three tools (the contract)
| Tool | Arguments | Returns | On bad input |
|---|---|---|---|
| `list_tickets` | `status`: one of `open`, `pending`, `closed`, or omitted for all; `limit`: integer, default 10, max 50 | list of `{id, priority, status, subject}` in file order, at most `limit` items | `limit` outside 1..50 → `ToolError("limit must be 1..50")` |
| `get_ticket` | `ticket_id`: string | the full ticket dict | unknown id → `ToolError("unknown ticket id; call list_tickets first")` |
| `get_policy` | `policy_id`: string | `{id, title, text}` | unknown id → `ToolError("unknown policy id; ids look like POL-REFUND-01")` |

Rules:
- Each tool is a typed Python function decorated with `@mcp.tool()`; arguments carry type hints, the return is a pydantic model, so the SDK generates `inputSchema` and `outputSchema` and fills `structuredContent`.
- Every tool has a docstring that says when to use it and when not ("Use get_ticket when you already have an id; otherwise list_tickets first").
- Every tool is read-only; mark it `annotations={"readOnlyHint": True}`.
- `ToolError` is the SDK's way to return an error the model can read (`isError: true`) instead of crashing the server. Messages tell the model what to do next and never contain a stack trace.

## 5. The server
- File `src/stage3a/server.py`. `from mcp.server.mcpserver import MCPServer` (SDK 2.x; `FastMCP` is the old name and will not import).
- `mcp = MCPServer("support-tickets")`; data loaded once at startup from `data/`.
- Logging to **stderr only**. Never `print()` — stdout is the protocol channel over stdio and one stray line kills the connection.
- `if __name__ == "__main__": mcp.run()` runs it over stdio.

## 6. The tests (`tests/test_server.py`, written before the server)
Using the SDK in-memory client (`from mcp import Client`), no subprocess, no network:
1. `list_tools` returns exactly `{"list_tickets", "get_ticket", "get_policy"}`.
2. `list_tickets(status="open")` returns 4 items; `list_tickets(limit=2)` returns 2.
3. `get_ticket("T-1001")` → `structured_content["priority"] == "high"`.
4. `get_ticket("nope")` → `is_error` is true and the message contains `list_tickets`.
5. `get_policy("POL-REFUND-03")` → text contains `500`.
6. Calling a tool that does not exist raises `MCPError` with code `-32602`.

## 7. Repo layout
```
stage3a-mcp/
  SPEC.md            this file
  README.md          how to run tests and Inspector; the Inspector screenshots
  pyproject.toml     mcp>=2,<3 ; pydantic ; pytest ; pythonpath = ["src"]
  data/tickets.json  data/policies.json
  src/stage3a/__init__.py  src/stage3a/server.py
  tests/test_server.py
```

## 8. How tonight runs (90 minutes)
1. You (5 min): `git init`, `uv init --python 3.12`, `uv add "mcp>=2,<3" pydantic`, `uv add --dev pytest`. Copy this folder's `SPEC.md` and `data/` in.
2. Claude Code (40 min): open it in the repo, paste: "Read SPEC.md. Plan first. Then write tests/test_server.py from section 6, then src/stage3a/server.py from sections 4–5, then README.md. Run `uv run pytest -q` and show me the output. Do not commit." Approve the plan only if it matches the spec; if it adds tools or files, say no.
3. You (20 min, the review): open `server.py`. For each decorator, each `ToolError` and the `run()` line, say in one sentence what it does; if you cannot, ask Claude Code "explain this line" and read the answer. Run `uv run pytest -q` yourself: 6 passed.
4. You (15 min): `npx @modelcontextprotocol/inspector uv run python -m stage3a.server`; in the browser call `get_ticket` with `T-1001` and with `nope`; screenshot both into `docs/`.
5. You (5 min): `git add -A && git commit -m "stage3a: support-tickets MCP server, 3 tools, 6 tests, Inspector verified"`. Push if the remote exists.

## 9. Done means
Six tests green, two Inspector screenshots, one commit, and you can say the next three sentences from memory: what the server exposes, why errors come back as `isError` not exceptions, and why nothing may print to stdout.

## 10. Not tonight
OAuth, Streamable HTTP, Azure, the agent, evals, tracing. Those are Stage 3b onwards and each one reuses these three tools unchanged.
