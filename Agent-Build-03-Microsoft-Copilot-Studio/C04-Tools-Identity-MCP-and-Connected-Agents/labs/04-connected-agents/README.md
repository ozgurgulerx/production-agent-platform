# 04 — Connected agents: Foundry, A2A, Agents SDK, and this agent as A2A for Foundry

**Start with the failure.** Add the Foundry `ticket-agent-prompt` from the F03 lab as a connected agent with its project endpoint and agent id. Copilot Studio returns **400**. Nothing is wrong with the agent: its **Activity protocol endpoint** is off, and the portal has no switch for it (B4). `foundry_agent_enable_activity.py` turns it on; the second attempt succeeds.

## Goal
Connect the three kinds of external agent the dialog accepts, and publish the ticket agent itself as an A2A agent so Foundry can call it back.

## You will end with
- the Foundry agent listed under Connected agents, and a plan that hands a question to it
- the AWS track's A2A refund specialist (or any A2A card) as a remote agent
- the C03 lab 04 Agents SDK agent connected through its Activity endpoint
- (GitHub harness, preview) the ticket agent's A2A card URL, and a Foundry A2A tool calling it

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
cd 04-connected-agents
python foundry_agent_enable_activity.py            # reads the Foundry track .env if present; else FOUNDRY_PROJECT_ENDPOINT / FOUNDRY_AGENT_NAME
```
Then `add_foundry_connected_agent.md`, `a2a_remote_agent.md`, `add_sdk_agent.md`, `expose_as_a2a_for_foundry.md`.

## Facts that matter (reading map)
- B3: kinds: Copilot Studio agents, child agents, Foundry agents, A2A remote agents (GA Apr 2026), Agents SDK agents; split at 30–40 actions; a parent cannot itself be connected.
- B4: Foundry agent needs the Activity protocol endpoint enabled by REST/Python; new-portal agents only; else 400.
- B5: Agents SDK agent via `/api/messages`; auth none / API key / OAuth2.
- B6: GitHub-harness agent published as MCP server or A2A agent (preview, early-release environments); scopes `MCS.InvokeAsMCP` / `MCS.InvokeAsA2A`.
- B7: Foundry incoming A2A v1.0 GA, Entra only, JSON-RPC.

## Proof (checklist)
- [ ] first add of the Foundry agent returned 400 (keep the text); after enabling the Activity endpoint it was accepted
- [ ] a question that needs the Foundry agent shows a hand-off step in the activity map
- [ ] the A2A remote agent's card was fetched and the agent appears with its skills
- [ ] the SDK agent answers through the connected-agent path (trace shows the Activity call)
- [ ] (preview) the ticket agent's A2A card URL resolves and a Foundry `A2ATool` call returns an answer

## Next
`../05-direct-to-engine-apps/` — calling the agent from your own app on behalf of the user.
