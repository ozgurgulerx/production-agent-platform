# Agent flow: refund approval with a human step (Standard harness)

Agent flows are the Standard-harness name for workflows (A7).

1. Trigger: **When an agent calls the flow** with `ticket_id` (text), `amount_gbp` (number), `reason` (text).
2. Condition `amount_gbp <= 250`:
   - yes → **Call the ticket MCP tool / HTTP** `issue_refund` → respond `{status: issued}`.
   - no → **Request information** (human-in-the-loop): approval card to `cards-uk-leads`; the flow waits. Responses beyond two minutes are asynchronous (A2, May 2026).
3. On approve → `issue_refund` with an `approved_by` field; on reject → respond `{status: rejected, reason}`.
4. **Respond to the agent** with status and a customer-facing sentence.

Add as a tool with the description "Use for any refund request; the flow decides approval". Credits: flow actions 13 per 100 (K6).
