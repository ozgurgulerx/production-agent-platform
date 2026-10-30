# Way 1 — Prompt agent in the portal

The portal is the fastest path and the one most teams start with. It is also the one that hides the most, so this page shows what each click does on the wire.

1. Foundry portal → your project → **Build** → **Agents** → **Create agent**. Interaction mode **Text** (Voice is way 3 and cannot be changed later).
2. Name `ticket-agent-portal`, model `gpt-5-mini`, instructions:
   > You are the support-ticket assistant for a UK bank's card team. Answer briefly. When you do not have a tool for something, say so instead of guessing.
3. **Save**. Saving creates **version 1**. Every later Save creates a new immutable version; the name can never change.
4. **Try in playground** → ask "My card was charged twice." The playground is calling `POST {project_endpoint}/agents/ticket-agent-portal/endpoint/protocols/openai/responses?api-version=v1`.
5. **Code** tab → the SDK equivalent is exactly `02-prompt-agent-sdk.py`.

What the Save button sent (REST, `api-version=v1`):
```http
POST https://<resource>.services.ai.azure.com/api/projects/<project>/agents?api-version=v1
Authorization: Bearer <token for https://ai.azure.com/.default>
{"name": "ticket-agent-portal", "definition": {"kind": "prompt", "model": "gpt-5-mini", "instructions": "..."}}
```
And what the playground sends per turn:
```http
POST .../agents/ticket-agent-portal/endpoint/protocols/openai/responses?api-version=v1
{"input": "My card was charged twice.", "conversation": "<conversation id>"}
```

Proof: screenshot of the agent's **Versions** tab showing v1, and the playground answer. Then run `python 06-invoke-everything.py` with `AGENT_NAMES=ticket-agent-portal` to prove the same agent answers from code.

Gotcha: the portal's default "create a new version on every save" is fine; the same pattern in a startup hook of an app is how teams hit the 1,000-version cap.
