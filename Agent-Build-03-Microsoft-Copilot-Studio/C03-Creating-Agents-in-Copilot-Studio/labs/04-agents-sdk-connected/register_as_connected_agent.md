# Register the SDK agent as a connected agent (B5)

Copilot Studio → Ticket Agent → **Agents** → Add → **Microsoft 365 Agents SDK agent**:
- Endpoint: `https://<tunnel-or-host>/api/messages` (the Activity protocol endpoint).
- Authentication: **None** (local demo only), **API key** (header), or **OAuth 2.0** (recommended; the SDK validates the JWT from the Azure Bot registration).
- Name and description: the orchestrator uses the description to decide when to delegate ("Knows ticket SLAs and raw ticket rows").

Rules that apply (B3): a main agent with connected agents cannot itself be connected elsewhere; split at 30–40 actions. The SDK agent gets no Entra Agent ID connector scopes (E1); its identity is the Azure Bot app or managed identity you registered.

Same thing elsewhere: Foundry hosted agent exposed over A2A; AgentCore Runtime as a Gateway HTTP target.
