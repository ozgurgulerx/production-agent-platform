# Agent flow: human approval above 250 GBP (reading map A7, B2)

The MCP and REST tools return `ESCALATE` above 250 and stop. A tool cannot wait for a person; an **agent flow** (Standard harness; "workflow" in the GitHub harness) can, with a **request-information** step.

## Build (Copilot Studio → Flows → New agent flow)
1. Trigger: **When an agent calls the flow**. Inputs: `ticket_id` (text), `amount` (number), `reason` (text).
2. Condition: `amount > 250`.
   - Yes: **Request information** (Teams approval card to the supervisor group) → wait → branch on `Approve` / `Reject`.
   - No: HTTP action `POST {TICKET_API_BASE}/tickets/{ticket_id}/refund` with the API-key connection, or the Dataverse row update if you keep tickets in Dataverse.
3. **Respond to the agent**: `decision` (text), `result` (text). Mark the flow as able to respond asynchronously so the agent is not held to the 2-minute limit (A7, May 2026).
4. Save, then in the agent: Tools → Add a tool → Flows → `Refund approval`. Description: "Use for any refund; it handles approval above 250 GBP."

## Test
"Refund 400 pounds on ticket 1042 for a duplicate charge" → the agent calls the flow → the supervisor gets the card → after Approve the agent reports `REFUNDED`; after Reject it reports the rejection. Below 250 the flow refunds directly.

## Credits
Agent-flow actions bill at 13 credits per 100 actions; the agent action (tool call) is 5 (K6). Note it on the proof.

## GitHub harness note
The same shape is a **workflow** with an **agent node**; triggers in the new harness are preview (A9).
