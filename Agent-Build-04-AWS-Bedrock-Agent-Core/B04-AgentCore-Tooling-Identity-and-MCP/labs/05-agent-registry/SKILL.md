---
name: refund-policy
description: How the UK card team decides refunds. Load before using issue_refund.
---
# Refund policy skill
1. Read the ticket (`get_ticket`) and the policy (`get_policy refund`).
2. Duplicate charges are refunded in full; closed tickets are never refunded.
3. Above £250 return ESCALATE with the reason; never call `issue_refund` with amount > 250.
4. Quote the ticket id and the amount in the final answer.
