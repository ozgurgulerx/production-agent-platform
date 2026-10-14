# production-agent-platform

**Azure-first agentic AI architect for regulated financial services.** A support-operations agent built in stages: RAG and a bounded agent on Azure AI Foundry with MCP tools, OAuth-scoped access, eval gates, tracing, guardrails and a human-review path, plus the architecture and governance packs a design authority expects.

Scenario: the agent answers "what is the refund status for T-1001 and which policy applies?", escalates refunds over 500 GBP to a human, and never shows card or NI numbers. Every stage attaches to the same three MCP tools.

## Stages

Status changes only with a number sourced to a run. Full table with goals and weeks: [`docs/prompts/README.md`](docs/prompts/README.md).

| Stage | What ships | Evidence | Status |
|---|---|---|---|
| S0 Scaffold | uv project, CI, Dockerfile, pre-commit, ADR-0001 | `make lint test` runs | done |
| S1 MCP tools | `support-tickets` MCP server, 3 read-only tools | 3 tools, 6 tests, Inspector verified | planned |
| S2 Bounded agent | Agents SDK agent, guardrails, sessions, tracing | 10/10 scripted tasks | planned |
| S3 RAG + eval gate | hybrid + RRF retrieval, golden set, promptfoo gate | nDCG@10, Recall@20 | planned |
| S4 Orchestration + HITL | durable execution, approval on refunds > 500 GBP, injection suite | injection 10/10 | planned |
| S5 API + OAuth | FastAPI, MCP over Streamable HTTP with OAuth 2.1 | scopes per tool | planned |
| S6 Observability | tracing, cost per 1k, p50/p95 | production-evidence.md | planned |
| S7 Azure + Foundry | Foundry Agent Service, landing-zone shape | runs on Foundry | planned |
| S8 Packs | governance and architecture packs | A11 / A12 | planned |
| S9 Release | release manifest, system card, v1.0 | v1.0 tagged | planned |
| S10 Bedrock note | Foundry vs Bedrock mapping | comparison | planned |

## Architecture

Placeholder until S2. See [`docs/adr/`](docs/adr/) for decisions so far.

## Run

```bash
uv sync
make lint test      # ruff, mypy --strict, pytest
make run-mcp        # MCP server over stdio
make inspector      # MCP Inspector (needs Node >= 22)
docker build -t production-agent-platform . && docker run -i --rm production-agent-platform
```

S1 tool bodies are not written yet, so the MCP tests are marked `xfail` until they are.

## Related

- [`python-reps`](https://github.com/ozgurgulerx/python-reps): the daily timed exercises that feed this platform; they share the tickets/policies dataset.

## Timeline

- [`CHANGELOG.md`](CHANGELOG.md): what shipped, newest first.
- [`docs/log/`](docs/log/): weekly engineering notes with numbers.
- [`docs/prompts/`](docs/prompts/): the stage SPECs and Claude Code prompts.
