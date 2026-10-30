# 04 — A Microsoft 365 Agents SDK agent, connected to Copilot Studio

Way 6, the connected direction. Your own loop in Python on the Activity protocol (`/api/messages`), run anywhere, then added to the ticket agent as a **connected agent** (B5). The calling direction (Direct-to-Engine) is in lab 01.

```
04-agents-sdk-connected/
├── sdk_agent/app.py              aiohttp host, AgentApplication, ticket answers, 250 GBP refusal
├── sdk_agent/requirements.txt
├── sdk_agent/README.md           run locally, dev tunnel, Azure Bot registration, FIC auth (no secrets)
├── register_as_connected_agent.md
└── call_from_copilot_studio.md
```

## Steps
1. `cd sdk_agent && ../../../../labs-setup/.venv/bin/python app.py` → listens on 3978.
2. Test locally with the Agents Playground or `curl` (see `sdk_agent/README.md`).
3. Expose with a dev tunnel; register an Azure Bot with the tunnel URL + `/api/messages`; use **federated identity credentials or managed identity**, never a client secret.
4. Copilot Studio → Ticket Agent → Agents → **Add** → Microsoft 365 Agents SDK agent → endpoint, auth (B5).
5. Ask the Ticket Agent something only the SDK agent knows ("what is the SLA for P1 tickets?") and watch the activity trace delegate.

## Proof checklist
- [ ] `GET /api/messages` returns 405 and a POSTed message activity returns a reply locally
- [ ] Azure Bot registration points at the tunnel; Web Chat test in Azure answers
- [ ] Connected agent added; activity trace shows the delegation
- [ ] A 400 GBP refund asked through Copilot Studio is refused by the SDK agent's own rule
