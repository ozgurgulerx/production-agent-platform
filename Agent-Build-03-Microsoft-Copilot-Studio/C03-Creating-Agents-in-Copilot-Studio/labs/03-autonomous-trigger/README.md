# 03 — Autonomous: a Dataverse row starts the agent

Way 4. Nobody types the first message. A row in a `Ticket` table triggers the agent, which summarises the ticket, sets a priority and, for a refund over 250 GBP, pauses an agent flow on a request-information step.

## Steps
1. Dataverse: create a table `Ticket` (columns `TicketId`, `Customer`, `Country`, `AmountGBP`, `Description`, `Priority`, `Summary`) in the same solution as the agent.
2. Agent → Overview → **Triggers** → Add → "When a row is added, modified or deleted" (Dataverse) → table `Ticket`, change type Added. Map `Description` and `AmountGBP` into the trigger message ([`trigger.md`](trigger.md)).
3. Add the agent flow from [`agent_flow_refund_approval.md`](agent_flow_refund_approval.md) as a tool.
4. Settings → Solutions: confirm the flow is solution-aware and sharing is on (B2).
5. Create a row with `AmountGBP = 400` → watch Overview → **Activity**; the flow pauses on the approval card.
6. Read the run from code: `python activity_read.py`.

## Facts that bite
- Triggers run with **maker credentials** only (B2); the audit shows the maker. Pair an agent user for Dataverse roles if needed (E4).
- Every trigger payload is billed as an agent action (5 credits, K6).
- The run appears under event-trigger sessions in Monitor (H1) and in `conversationtranscripts` (G4), not under conversational sessions.

## Proof checklist
- [ ] Row created → Activity page shows a run within a minute
- [ ] `Summary` and `Priority` columns filled by the agent
- [ ] 400 GBP row → approval card in Teams; run paused
- [ ] `activity_read.py` prints the run with its outcome
