# 11 — Agent-to-agent: the A2A tool (v1.0 GA) and Logic Apps as a caller

## Goal
Replace "Connected Agents" (not available in the new Agent Service) with the two supported patterns: an `a2a` tool over a `RemoteA2A` connection for cross-boundary delegation, and in-process Agent Framework workflows (folder 12) for everything else. Then show an external caller (Logic Apps Standard) invoking a Foundry agent with its managed identity.

## Run
```bash
azd ai project set "$FOUNDRY_PROJECT_ENDPOINT"
azd ai connection create specialist-a2a --kind remote-a2a --target "$FOUNDRY_PROJECT_ENDPOINT/agents/ticket-agent-workflow/endpoint/protocols/a2a" --auth-type user-entra-token --audience https://ai.azure.com
source ../.venv/bin/activate && python a2a_demo.py
```
Targets: another Foundry agent (enable incoming A2A on it; audience `https://ai.azure.com`), the self-hosted agent from 02, or any A2A 1.0 server. Toolbox variant: `A2AToolboxTool`. `logic-app/workflow.json` is a Logic Apps Standard workflow that calls the agent's Responses endpoint with managed identity (grant it Foundry User on the project).

## Facts
- `a2a` = protocol 1.0 GA; `a2a_preview` = 0.3. Text only; no streaming when the target is a Foundry agent.
- Auth is on the connection: the same six types as MCP. `send_credentials_for_agent_card` only when the card itself is protected.
- Client user delegation (`AgentOnBehalfOfUser`) is preview and needs the `AgentBlueprint` scheme.

## Proof (checklist)
- [ ] `a2a_demo.py` prints an `a2a_call` item and the specialist's answer
- [ ] Logic App run history shows a 200 from the agent endpoint with the workflow's identity in the agent trace

## Next
F03 `labs/03-multi-agent-workflow/` — the in-process alternative, hosted as one agent.
