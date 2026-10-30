# Stateful MCP on Runtime (Mar 2026)

Lab 02 deploys with `stateless_http=True`. Change one line, `FastMCP(..., stateless_http=False)`, and the server keeps its own session state. What changes:

| | Stateless (default) | Stateful |
|---|---|---|
| Session id | platform injects `Mcp-Session-Id` and maps it to a Runtime session | the server issues it on `initialize`; the client must echo it on every request |
| MCP version | works with 2026-07-28 (no `initialize`) | needs 2025-xx versions with `initialize` |
| Elicitation (server asks the user mid-call) | no | yes |
| Sampling (server asks the client's model) | no | yes |
| Progress notifications | no | yes |
| Scaling | any microVM can answer | one microVM per session, same 15 min idle / 8 h lifetime |

Pick stateful only when a tool genuinely needs to ask a question mid-call (`issue_refund` above £250 could elicit "approve?" instead of returning ESCALATE). Everything else stays stateless.
