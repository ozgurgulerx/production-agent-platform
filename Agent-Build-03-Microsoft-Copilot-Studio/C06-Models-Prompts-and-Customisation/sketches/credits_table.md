# Sketch: Copilot Credits per feature (reading map K6, 2026-08-03)

| Feature | Credits | Unit |
|---|---|---|
| Classic answer (topic without generative AI) | 1 | per answer |
| Generative answer | 2 | per answer |
| Agent action (trigger run, deep reasoning, topic transition, computer-use step) | 5 | per action |
| Tenant graph grounding (semantic search over M365) | 10 | per answer that uses it |
| Agent-flow actions | 13 | per 100 actions |
| AI tools: basic / standard / premium | 1 / 15 / 100 | per 10 responses |
| Premium AI tool on a reasoning model | 10 | per 1,000 tokens |
| Content processing | 8 | per page |
| Voice | 10 / 35 / 75 | per minute, by tier |
| Computer use step (Standard harness, B8) | 5, Opus 4.6: 15 | per step |

Pack: 25,000 credits for USD 200 per month (K7); PAYG through an Azure billing policy (per-credit rate on the pricing page, third-party say USD 0.01, verify). Microsoft 365 Copilot-licensed users in B2E: no charge for these features (agent flows only when called from an agent). Enforcement: prepaid agents disabled at 125 % of the pack, flows blocked at 100 %, per-agent monthly caps in PPAC (C09).

The GitHub Copilot harness bills by usage in credits rather than by these feature rates (A5, K5); the table above is the Standard harness.
