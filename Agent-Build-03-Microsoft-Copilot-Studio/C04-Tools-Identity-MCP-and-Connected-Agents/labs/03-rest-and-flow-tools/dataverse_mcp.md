# Dataverse MCP server (reading map D6, D7)

Every environment has an MCP endpoint at `https://{org}.crm.dynamics.com/api/mcp`. The server exposes 15 tools (search_data, read_query, create / update / delete record, create / update / delete table, skills, file upload); the Copilot Studio connector surfaces 11 of them (D7, preview). Auth is the user's Dataverse rights: the agent sees what the signed-in user can see, which is why end-user credentials matter here.

## Add it
Tools → Add a tool → Model Context Protocol → **Dataverse MCP server** (prebuilt). Pick the environment (usually the same one). Turn "Allow all" off and enable `search_data`, `read_query` only for the ticket agent.

## Try it
If the tickets live in a Dataverse table (`cr1ab_ticket`), ask "which open tickets mention a duplicate charge?" and watch `search_data` in the activity map.

## Billing
For clients other than Copilot Studio (VS Code, Claude Code, your own MCP client) the server is billed since 15 Dec 2025; `search_data` is priced like tenant graph grounding (10 credits). Inside Copilot Studio the normal tool-call rates apply (K6).

## Why it matters for the comparison
It is the counterpart of the AWS AgentCore "AWS MCP Server" and the Azure MCP Server: the platform's own data plane, offered as MCP, governed by the same connector DLP.
