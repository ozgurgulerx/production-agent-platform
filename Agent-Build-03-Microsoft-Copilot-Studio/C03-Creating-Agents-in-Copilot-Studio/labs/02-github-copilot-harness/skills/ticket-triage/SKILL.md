---
name: ticket-triage
description: Classify a support ticket for the UK card team (priority, queue, refund eligibility) before answering the customer.
---

# Ticket triage

Use this skill when a message mentions a ticket id (T-####) or asks what to do with a ticket.

## Steps
1. Call `get_ticket` with the ticket id. If it does not exist, say so and stop.
2. Classify priority: P1 fraud or lost card, P2 duplicate or wrong charge, P3 everything else.
3. Decide the queue: `cards-uk` for UK and EU customers, `escalations` for other countries (card policy).
4. Refund eligibility: eligible if the ticket is a duplicate charge under 250 GBP and within 60 days (refund policy). Above 250 GBP: not eligible by this agent; escalate.
5. Answer in four lines: priority, queue, eligibility with the policy cited, next action.

## Guardrails
- Never issue a refund inside triage; triage only recommends.
- Quote the policy document name you relied on.
