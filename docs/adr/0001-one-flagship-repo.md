# ADR-0001: One flagship repo, with the daily reps in a separate repo

- Status: accepted
- Date: 2026-10-14

## Context
The contract AI architect lane needs one system a reviewer can walk from HLD to running code to evidence. The earlier blueprint proposed three flagship repos (retrieval, eval control plane, release platform), each a 35 to 65 hour build. On a 20-week plan with a 45-minute Python ceiling, all three would be thin. Timed live-coding exercises sitting in the flagship root (`R0-tickets-basics/`) make the production repo look like a scratchpad.

## Decision
- `production-agent-platform` is the only flagship. Retrieval benchmark, eval release gate and release manifest become stages S3, S4 and S9 of this repo. The Bedrock variant is stage S10, not a repo.
- Timed exercises live in a separate `python-reps` repo. The two share the tickets/policies dataset on purpose.
- The first MCP server (`R1-tickets-mcp/`) moves to `src/pap/tools/` as stage S1.

## Consequences
- One repo carries the A3, A12 and A11 evidence; stage status lives in the README table.
- A reviewer sees no learner exercises in the production repo.
- Cost: a second repo to maintain, and a dataset duplicated across both.

## Revisit when
- A stage outgrows the repo (separate release cadence or team), or
- the plan changes lane away from contract AI architect work.
