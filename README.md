# production-agent-platform

Azure-first agentic AI platform for regulated financial services — RAG + MCP tools + bounded agents, with evals, tracing, guardrails, cost and latency evidence. Built stage by stage; every stage ships tagged, tested and measured. Amazon Bedrock twin at architecture level.

<!-- Badges go live with the first ci.yml (Stage 3b PR). A stale badge is worse than none. -->

## What it does

A support-operations assistant over a ticket and policy corpus. A user asks "what is the refund status for T-1001 and which policy applies?"; the agent calls ticket and policy tools over MCP, retrieves policy text with ACL trimming, stays inside a step budget and a tool allowlist, returns a typed answer that quotes the policy it relied on, and leaves a trace. Every answer is scored by an eval suite in CI; every release carries its numbers.

## Architecture (target)

```
user ──► FastAPI (auth, rate limit, timeouts)
            │
            ▼
      Agents SDK runner ── guardrails (in/out) ── structured output
            │  max_turns, tool allowlist, tracing
            ├──► MCP server (stdio): list_tickets · get_ticket · get_policy     ◄── Stage 3a, now
            └──► RAG: Azure AI Search hybrid (BM25 + vector) → RRF → reranker → ACL filter
                                                      ▲
                                      Azure OpenAI (chat, embeddings) via APIM gateway
      traces ──► Langfuse / OTel GenAI      evals ──► promptfoo + LLM judge, CI gate
```

Drawn diagrams, landing-zone shape and the Bedrock twin arrive in `docs/architecture/` with Stage 4.

## Stages

| Stage | What ships | Where | Tag | Tests | Key numbers |
|---|---|---|---|---|---|
| 3a | `support-tickets` MCP server: 3 read-only tools over 8 tickets and 5 policies, Inspector-verified | [R1-tickets-mcp](R1-tickets-mcp/) · [SPEC](R1-tickets-mcp/SPEC.md) | `stage3a-v0.1` (pending) | 6 (spec §6) | tool round-trip p95: not yet measured |
| 3b | Bounded agent loop over the same tools: allowlist, step budget, structured output, tracing, 10 scripted tasks | — | — | — | — |
| 2 | RAG over the policy corpus: hybrid retrieval, RRF, reranker, ACL trimming, golden set of 50 | — | — | — | — |
| 3c | Orchestration: handoffs, durable execution, human approval, injection suite | — | — | — | — |
| 4 | Production evidence: cost per 1k requests, p50/p95, fallback path, release manifest | — | — | — | — |
| 5 | Azure AI Foundry rebuild + Bedrock comparison | — | — | — | — |

Numbers in this table are copied from CI runs and `docs/production-evidence.md`, never typed from memory. "Not yet measured" is the honest state until a run exists.

## Quickstart (Stage 3a)

```bash
cd R1-tickets-mcp
uv sync
uv run pytest -q                                   # 6 tests, in-memory MCP client
npx @modelcontextprotocol/inspector uv run python -m stage3a.server   # call the tools by hand
```

Conventions from here on: `uv` for environments, `ruff` + `mypy --strict` + `pytest` on every PR once `ci.yml` lands (Stage 3b), secrets only in `.env` (see `.env.example`), small commits on a branch, every stage behind a PR.

## Evidence

Each link is created by the stage that produces it; until then it does not exist and is not listed as if it did.

- `docs/production-evidence.md` — eval scores, judge agreement, cost per 1k, p50/p95, fallback and human-review path, release manifest; every number linked to the run that produced it (Stage 4).
- `docs/evals/` — promptfoo results per tag, judge calibration against hand labels (Stage 2).
- `docs/security/` — threat model, OWASP LLM Top 10 mapping, injection suite with the exploit shown before each control (Stage 3c).
- `docs/governance/` — EU AI Act classification, NIST AI RMF mapping, DPIA, system card (governance pack).
- Demo recordings per major tag.

## Decisions

[docs/adr/](docs/adr/) — one architecture decision record per decision a reviewer would challenge: transport, tool surface, retrieval stack, judge independence, Foundry vs Bedrock.

## Engineering log

- [CHANGELOG.md](CHANGELOG.md) — one line per shipped thing, newest first; versions are git tags.
- [docs/log/](docs/log/) — weekly engineering notes: shipped, measured, broke-and-fixed, decided.
- [docs/reading/](docs/reading/) — one-page notes on the reference documents this platform is built from (OpenAI Agents SDK, Anthropic building-effective-agents and context engineering, MCP spec and authorization, Azure AI Foundry, Amazon Bedrock), each written from memory after the read and checked against the source.

## Drills

`R0-tickets-basics/` and its successors are timed Python exercises (25–45 min, tests given, no AI while the timer runs) over the same ticket data. They are kept in the repo as the record of the coding discipline behind the stages, not as part of the platform.

## Repo layout

```
R1-tickets-mcp/      Stage 3a — MCP server (src/stage3a, tests, data, SPEC.md)
R0-tickets-basics/   timed Python drill, rung 0
docs/                adr/ · log/ · reading/  (architecture/, evals/, security/, governance/ arrive with their stages)
CHANGELOG.md         release history
package.json         MCP Inspector pin
```

## Author

Ozgur Guler — Azure-first agentic AI architect for regulated financial services; ex-Microsoft AI solutions engineer, ex-AWS solutions architect, ex-Cisco / J.P. Morgan low-latency systems. London from March 2027.
