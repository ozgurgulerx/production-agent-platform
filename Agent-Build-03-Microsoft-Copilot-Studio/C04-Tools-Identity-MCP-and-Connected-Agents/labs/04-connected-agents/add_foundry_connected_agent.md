# Add a Foundry agent as a connected agent (reading map B4, preview)

1. In the ticket agent: Agents → Add → **Foundry agent**. Enter the project endpoint (`https://<resource>.services.ai.azure.com/api/projects/<project>`) and the agent id/name (`ticket-agent-prompt`).
2. Without the Activity endpoint: **400**. Record the message.
3. Run `python foundry_agent_enable_activity.py`, repeat step 1: accepted. Give it a description the planner can route on: "Handles card-replacement questions for UK customers."
4. Auth: the user's Entra identity is forwarded; the Foundry agent's own identity decides what it may read.
5. Test: "Can I get a replacement card sent to Peru?" → activity map shows a hand-off to the Foundry agent and its refusal citing the card policy (F08 knowledge).

Limits: new-portal Foundry agents only; the Copilot Studio agent becomes a parent and can no longer be connected elsewhere (B3). The reverse (Foundry calling this agent) is `expose_as_a2a_for_foundry.md`.
