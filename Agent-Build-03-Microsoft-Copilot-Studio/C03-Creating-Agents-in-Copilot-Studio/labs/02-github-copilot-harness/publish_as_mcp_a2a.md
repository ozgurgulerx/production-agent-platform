# Publish the agent as an MCP server or an A2A agent (preview, B6)

Only the GitHub Copilot harness has these two "client" channels today, and only in early-release environments.

- **MCP client channel**: the agent is exposed as an MCP server. Callers need a delegated token with scope `MCS.InvokeAsMCP`.
- **A2A client channel**: the agent is exposed as an A2A agent with an agent card. Callers need `MCS.InvokeAsA2A`.

Foundry side (B7): the A2A tool accepts A2A v1.0 over JSON-RPC with Entra only, so a Foundry prompt agent can call this agent as a tool. AgentCore side: a Strands agent with an A2A client can call it the same way (B03 lab 03 client pattern).

Checklist: environment is early-release; channel enabled; a Foundry agent with the A2A tool pointed at the card URL answers a ticket question through it. Record the card URL in `.env` as `CS_A2A_CARD_URL` for C04 lab 04.
