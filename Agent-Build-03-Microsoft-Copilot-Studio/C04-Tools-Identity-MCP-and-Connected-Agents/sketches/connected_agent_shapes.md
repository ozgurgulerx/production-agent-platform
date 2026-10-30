# Connected-agent shapes (reading map B3–B7)

What each kind needs before the "Connected agents" dialog accepts it. Dates are page dates from the reading map.

| Kind | You provide | Auth choices | Preconditions | Status |
|---|---|---|---|---|
| Copilot Studio agent | pick from the same environment | the agent's own end-user auth | published; not itself a parent of connected agents | GA |
| Child agent | name, instructions, its own tools and knowledge | inherits | 128 tools of its own | GA |
| Foundry agent | project endpoint, agent id | Entra | **Activity protocol endpoint enabled** on the Foundry agent (REST/Python only); new-portal agent; else HTTP 400 | preview (B4, 2026-08-26) |
| A2A remote agent | agent card URL (`/.well-known/agent-card.json` or the platform's card path) | none, API key, OAuth2 | card reachable over HTTPS; JSON-RPC transport | GA Apr 2026 (B3) |
| Microsoft 365 Agents SDK agent | Activity endpoint `https://host/api/messages` | none, API key, OAuth2 | Activity protocol 1.x; the host validates inbound JWTs itself | preview (B5, 2026-10-14) |

## This agent as a target for others (GitHub harness only, preview, B6)

| Channel | Scope the caller needs | Who can call |
|---|---|---|
| MCP client | `MCS.InvokeAsMCP` (delegated) | any MCP client with an Entra token: Foundry `MCPTool` with an Entra connection, VS Code, AgentCore Gateway with an OAuth credential provider |
| A2A client | `MCS.InvokeAsA2A` (delegated) | Foundry A2A tool (incoming v1.0 GA on the Foundry side, B7), the AWS track's A2A client, any a2a-sdk client |

Early-release environments only at the time of crawl. The published card and MCP endpoint URLs are shown in the channel pane after publish.

## Minimal A2A agent card the dialog accepts (shape)

```json
{
  "name": "ticket-refund-specialist",
  "description": "Refund decisions for UK card tickets, 250 GBP cap",
  "url": "https://<host>/a2a",
  "version": "1.0.0",
  "capabilities": {"streaming": false},
  "skills": [{"id": "refund", "name": "Issue refund", "description": "Refund a ticket within policy"}],
  "securitySchemes": {"bearer": {"type": "http", "scheme": "bearer"}}
}
```
