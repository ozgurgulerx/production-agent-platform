# Publish the ticket agent as an A2A agent, call it from Foundry (reading map B6, B7; preview)

Only a **GitHub-harness** agent in an early-release environment can be published as an MCP server or an A2A agent today. Use the C03 lab 02 agent.

1. Channels → **A2A client** (preview) → enable. Copy the agent card URL. The caller needs an Entra token with the delegated scope `MCS.InvokeAsA2A` (for the MCP client channel, `MCS.InvokeAsMCP`).
2. On Foundry (F04 lab 06 pattern): create a `remote-a2a` connection with Entra auth to the card URL, add `A2ATool` to a prompt agent, ask a ticket question. Foundry's incoming A2A is v1.0 GA; outgoing to this card uses the same JSON-RPC transport (B7).
3. The call appears in Copilot Studio's activity trace with the Foundry agent's identity as the caller.

Record the card JSON and the Foundry response; this closes the loop started in `add_foundry_connected_agent.md`.
