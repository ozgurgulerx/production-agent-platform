# Add a Microsoft 365 Agents SDK agent (reading map B5, preview)

The C03 lab 04 agent runs on `aiohttp` with `AgentApplication` and listens at `https://<host>/api/messages`.

1. Agents → Add → **Microsoft 365 Agents SDK agent**. Endpoint: the `/api/messages` URL. Auth: **None** for a local tunnel demo; **OAuth2** (the SDK host validates inbound Entra JWTs through `MsalConnectionManager`) for anything shared.
2. Description for routing. Test with a question the SDK agent owns.
3. The trace shows an Activity exchange, not a tool call; the SDK agent can itself call Copilot Studio back through Direct-to-Engine (lab 05), which is how you build a bridge between tenants.
