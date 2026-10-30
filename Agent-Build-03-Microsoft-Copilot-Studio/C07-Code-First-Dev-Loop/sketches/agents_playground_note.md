# Agents Playground, in one page

The Microsoft 365 Agents Playground is the local test client that ships with the Agents Toolkit for VS Code (A10; current Toolkit release details not re-verified, reading map "unverified" list). It sends Bot Framework / Activity-protocol messages to a URL you give it and renders the replies, with no Entra token and no tenant.

- Point it at `http://localhost:3978/api/messages` while `python app.py` from C03 lab 04 is running.
- It exercises `AgentApplication` handlers (`@app.message`, `@app.conversation_update`), Adaptive Cards and typing indicators. It does **not** exercise `MsalConnectionManager`, because it sends no token; the first authenticated call comes from Copilot Studio through the tunnel (B5).
- It does not exercise MCP. If the thing you built is a tool, host it as an MCP server and test it with an MCP client (C04 lab 02).
- When you add the agent to Copilot Studio as a connected agent, choose the auth mode (none / API key / OAuth2) to match `app.py`; the Playground's success tells you nothing about that step.

Shape of the aiohttp host (signatures from `microsoft-agents-hosting-aiohttp` 1.9.0, verified in the venv 25 Oct 2026):

```python
from aiohttp import web
from microsoft_agents.hosting.aiohttp import CloudAdapter, start_agent_process
from microsoft_agents.hosting.core import AgentApplication, MemoryStorage, TurnContext, TurnState
from microsoft_agents.authentication.msal import MsalConnectionManager

connections = MsalConnectionManager(connections_configurations=...)   # from env / config, no secrets in code
adapter = CloudAdapter(connection_manager=connections)
app = AgentApplication[TurnState](storage=MemoryStorage(), adapter=adapter)   # verify kwargs vs ApplicationOptions

@app.message("/ticket")
async def ticket(context: TurnContext, state: TurnState):
    await context.send_activity("Ticket T-1001 is open; refunds above 250 GBP need approval.")

async def messages(request: web.Request):
    return await start_agent_process(request, app, adapter)

web_app = web.Application(); web_app.router.add_post("/api/messages", messages)
web.run_app(web_app, port=3978)
```
