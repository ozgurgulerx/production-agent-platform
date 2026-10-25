# S05.04: Agent Task Evals

Status: **Planned** (scope only; build target 1 November 2026).

End-to-end task suites over the support-ticket catalogue, scored by end state and cost per successful task. The suite is the capstone sequence, each step an eval case with a deterministic check:

1. Trace a read-only request end to end.
2. User-scoped authentication, two tenants.
3. A consequential action with bound confirmation.
4. The response is lost after the backend commits.
5. Worker restart and reconciliation.
6. Hostile metadata or ticket content.
7. Expired credentials, revoked access, a changed tool schema.
8. Quota exhaustion and a latency regression.
9. Inspect traces and backend state; justify recovery and the release decision.

The release-decision rule is written before any run: what result ships, holds, or reverts a tool-design or context-strategy change ("selection improved but cost per success rose" must have an answer). Metrics come from S05.02; the context-strategy comparison from S03.05 runs on this suite.

[Back to S05](../README.md)
