# Workflow: refund approval (A7)

Workflows (the renamed agent flows on this harness) are the deterministic side. Build in the agent's Workflows tab:

1. **Trigger**: "When an agent calls the workflow" with inputs `ticket_id`, `amount_gbp`, `reason`.
2. **Condition**: `amount_gbp <= 250`.
   - yes → **Agent node**: call `Ticket Agent (GH)` with "issue refund {amount_gbp} on {ticket_id}" → return the result.
   - no → **Request information**: approval card to the `cards-uk-leads` Teams channel with ticket, amount, reason. The run pauses (async beyond the two-minute limit, A2 May 2026).
3. **Prompt node** (optional, Deep model): draft the customer message from the outcome.
4. **Return**: `{status, message}` to the agent.

Add the workflow as a tool on the agent with the description "Use for any refund request". Credits: workflow actions are billed per 100 (K6).

Standard-harness equivalent: an agent flow with the same nodes, see `../03-autonomous-trigger/agent_flow_refund_approval.md`.
