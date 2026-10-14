# Stage prompts

Each stage has a SPEC (`SN-*.md`) and a Claude Code prompt (see [`prompts.md`](prompts.md)). Paste the prompt at the repo root after `git checkout -b sN/<name>`. Status changes only with a number sourced to a run.

| Stage | Week | Ships | Evidence line | Goals | Status |
|---|---|---|---|---|---|
| S0 Scaffold | wk1 | pyproject, CI, Dockerfile, pre-commit, README stage table, ADR-0001, CLAUDE.md, data/ | CI green; `make test` runs | M.12 | done |
| S1 MCP tools | wk1 | support-tickets MCP server (3 tools, 6 tests, Inspector screenshots) | 3 tools, 6 tests, Inspector verified | G1.1 | planned |
| S2 Bounded agent | wk1-2 | Agents SDK agent: step budget, allowlist, structured output, guardrails, sessions, tracing; 10 scripted tasks | 10/10 scripted tasks; trace screenshot | G1.1, G2.5 | planned |
| S3 RAG + eval gate | wk2 | Policy RAG: chunking, hybrid + RRF, reranker, ACL trimming; golden set 50; promptfoo CI gate; judge calibrated vs 30 labels; GraphRAG cost | nDCG@10, Recall@20, judge agreement, graph-build cost | G2.1, G2.2 | planned |
| S4 Orchestration + HITL + injection | wk4 | Orchestrator-workers, evaluator-optimiser; durable execution; human approval > 500 GBP; 10 injection tests; LangGraph twin | injection 10/10; kill-and-resume demo | G4.1, G4.2 | planned |
| S5 API + OAuth | wk6, wk8 | FastAPI hardened; MCP over Streamable HTTP with OAuth 2.1 (Entra), scope per tool, audit log | OAuth scopes per tool; OWASP API Top 10 checklist | M.11 | planned |
| S6 Observability + numbers | wk2, wk9 | Tracing (one chosen, ADR), OTel GenAI attributes; cost/1k, p50/p95, tokens per task; fallback path | cost/1k, p95, fallback path | G2.12, M.10 | planned |
| S7 Azure + Foundry | wk7, wk11 | Foundry Agent Service rebuild of S2; A1 landing-zone shape; PTU vs pay-go note | runs on Foundry; landing-zone diagram | M.5, A1 | planned |
| S8 Packs | wk4, wk5, wk11 | docs/governance/ (A11) and docs/architecture/ (A12) complete; review-board deck | A11 done; A12 v1/final | G4.3, M.6 | planned |
| S9 Release | wk10-12 | release-manifest.yaml, system card, demo video, tagged v1.0 | v1.0 tagged; demo linked | M.10, A5 | planned |
| S10 Bedrock note | wk13 | Foundry vs Bedrock mapping; adapter if time | platform comparison | X.2 | planned |
