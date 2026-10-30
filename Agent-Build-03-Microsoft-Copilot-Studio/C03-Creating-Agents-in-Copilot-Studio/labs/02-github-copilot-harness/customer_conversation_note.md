# Customer Conversation harness (preview, 21 Oct 2026, A6)

Way 5. For contact centres: a **primary agent** greets and routes, **sub-agents** own a job each (refunds, card replacement), every sub-agent has an **escalation path** to a human queue. Voice and chat through Dynamics 365 Contact Center.

The ticket agent in this shape:
- primary: identify customer and intent; hand to a sub-agent.
- sub-agent `refunds`: `get_ticket`, `issue_refund` with the 250 GBP cap; escalation path `cards-uk-leads`.
- sub-agent `card-replacement`: card policy knowledge; escalation for non-UK/EU addresses.

Sub-agents share ALM with the primary (one solution); connected agents do not (A6, B3). No code-first path is documented yet; treat it as portal-only and preview.
