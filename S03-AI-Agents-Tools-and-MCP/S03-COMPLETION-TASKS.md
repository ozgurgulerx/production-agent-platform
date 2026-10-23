# S03 completion tasks (21 Oct 2026)

Goal: S03.01–06 known cold, with two known soft spots (hands-on evidence, platform detail) closed by S05 and S03.03b. Tick in order within each group. Times are estimates. Merges the three reviews of 21 Oct; the coverage review's proposed S03.07–09 chapters are folded in here, not added.

## A. Do now (before S03.03b)

- [ ] **Record protocol revisions per stage.** S03.02 lockfile pins `mcp 2.3.0`; S03.03 pins `mcp 1.26.0` (declares 2025-11-25). Check which protocol 2.3.0 declares, state both in the S03 README and in S03.05's scope section. (~30 min)
- [ ] **Run MCP Conformance against the S03.03 server.** Its target version settles the revision question; add a "conformance-tested" line. (~1–2 h)
- [ ] **Write the one-page MCP explainer** (new section in S03 README): JSON-RPC 2.0, host/client/server, tools/resources/prompts, stdio vs Streamable HTTP, capability negotiation, what 2026-07-28 changes, plus one annotated successful call trace and one failed one (which layer failed: transport, JSON-RPC, protocol error, tool `isError`). The "explain MCP in two minutes" opener. (~1 h)
- [ ] **Write the comparison and "when not to use MCP" section** (S03.04 or S03 README): MCP vs function calling vs OpenAPI/plugins vs A2A; cases where MCP is the wrong choice (single client and backend, latency-critical, batch); server boundaries by credentials, ownership and blast radius (should HR, tickets and payments share a server?). (~30 min)
- [ ] **Fix the S03 README index:** it stops at S03.04; add S03.05 and S03.06. (5 min)

## B. Consistency fixes (one editing session, ~1 h)

- [ ] **S03.05:** add a "minimum viable build" line (steps 1, 2, 3 keyword arm, 5 projection arm, 6); merge the two further-reading lists; align the interview line with cost-per-successful-task; verify the `posts/2026-07-28/` link resolves; confirm "S03.04 section 10" exists in the committed S03.04.
- [ ] **S03.06:** restore the attack × defence matrix as the stated deliverable (six attacks: description poisoning, shadowing, rug pull, result injection, elicitation phishing, sampling abuse; defences as columns); add MCP-Scan, Promptfoo red-team and Docker MCP Gateway to sections 10–11; pick 2025-11-25 as the base spec and note 07-28 deltas; rename "IntentGrant (from the notes)" to task grant; replace the internal-notes source line with public references; add an elicitation paragraph in section 7.
- [ ] **S03.02 / S03.03:** end-to-end call narration (user request → every message → backend effect; call-id vs operation-key; sequential vs parallel dependencies; bounded loop and stopping conditions).
- [ ] **S03.03:** identity lifecycle section (token refresh and re-authentication, consent expiry, JWKS rotation, user deprovisioned mid-task: which component stops what, tenant isolation); deeper agent identity stays in S08.
- [ ] **S03.03:** transports and lifecycle paragraph; spec-revision note; one line on sampling deprecation in 07-28.
- [ ] **S03.04:** spec-revision note; link section 10 observability to W3C trace context.

## C. Comprehensiveness additions

S03.05 (~1.5 h):
- [ ] Parallel tool calls: column in the A/B/C table, line in the metrics.
- [ ] Catalogue refresh cost: `tools/list` frequency, `listChanged`, client caching of lists; paragraph in strategy A.
- [ ] Two-tier descriptions (short in catalogue, `describe_tool`/`detail` on demand).
- [ ] Unloading discovered tools over long sessions, with a "loaded definitions at step n" metric.
- [ ] Delegation as context partitioning: one paragraph in "Three independent decisions".
- [ ] Model routing (cheap model for discovery): one line in B.
- [ ] Streaming / progress notifications: one row in the large-data table.
- [ ] One resource and one prompt in the large-data step.

S03.06 (~2 h):
- [ ] Explicit threat model up front: attackers, goals, trusted base.
- [ ] Supply chain and installation: registries, `npx`/`uvx`, pinning, signatures, container isolation, review before enabling.
- [ ] Final-output exfiltration: markdown image links, link unfurling; row in section 8.
- [ ] Six-attack matrix (see B) including elicitation phishing and sampling abuse.
- [ ] Resource exhaustion as a named attack.
- [ ] Platform mapping table: Foundry (agent identity, MCP tool config, approval), AgentCore (Gateway, Identity, Cedar), Agents SDK (guardrails, `tool_filter`, approval callbacks).
- [ ] Standards paragraph: OWASP LLM Top 10, OWASP agentic guidance, MCP security best practices, MITRE ATLAS.
- [ ] Third-party data handling line (remote servers leave your retention/residency boundary).
- [ ] Detection layer paragraph: injection classifiers, call-pattern anomalies, canaries.
- [ ] Adversarial benchmarks: AgentDojo, InjecAgent, plus the scanners.

## D. Build (the soft spots)

- [ ] **S05 evals stage, target 1 Nov, with the capstone as the scenario set** (from the coverage review; replaces a separate S03.09). Each step is an eval case with a deterministic check: (1) trace a read-only request; (2) user-scoped auth, two tenants; (3) consequential action with bound confirmation; (4) response lost after backend commit; (5) worker restart and reconciliation; (6) hostile metadata or ticket content; (7) expired credentials, revoked access, changed schema; (8) quota exhaustion and latency regression; (9) inspect traces and backend state, justify recovery and the release decision. Harness: tool-selection accuracy, discovery recall, held-out questions, end-state checks, repeated runs. Conformance in CI. Note MCPJam as the off-the-shelf alternative; do not build on it.
- [ ] **S03.03b Foundry/Entra** (half day) and a platform paragraph in S03.06.
- [ ] **S03.06 build at demo depth:** malicious `fx-rates` server, scanners, Docker MCP Gateway step, matrix with pass/fail evidence.
- [ ] **S03.05:** minimum viable build only, after S05.
- [ ] **Operations one-pager** (S03.04 §10 + S03.06 §12 merged): deployment, versioning, observability and latency decomposition, replica races and retry budgets, graceful shutdown, incident response and regression capture.

## E. Learn by heart, then integrated exercises

Order decided 21 Oct: cram the chapters first, then do the four integrated exercises in `S03-EXERCISE-PLAN.md` (X1 system → tool set → contract; X2 scale; X3 trust boundary; X4 eval design, which becomes the S05 spec). Per-chapter exercises are skipped for now and kept as reference.

- [ ] Cram per `S03-MCP-cram-plan.xlsx`; retrieval drills; misses to cards. (10–12 h)
- [ ] X1–X4 in order, one per sitting, dated files under `exercises/`. (about 9 h)
- [ ] Closed-book redo of failed self-checks; transfer test on an unseen domain; commit. (2 h)


- [ ] Answer the S03.04 section 11 and S03.06 section 12 questions out loud, no notes; log misses in the quiz sheet.
- [ ] Two-minute spoken answers: "What is MCP?", "How would you expose our systems to an agent safely?", "When would you not use MCP?"
- [ ] Draw the S03.03 responsibility table and the S03.06 enforcement diagram from memory.
- [ ] Diagnostic follow-ups, one each: SDK call hangs (which layer); stream breaks after a refund committed; user loses access mid-export; two replicas retry the same operation; latency doubled, error rate flat.
- [ ] Anki cards for every miss, via the anki-card skill.

Rejected: new chapters S03.07 protocol mechanics, S03.08 production systems, S03.09 interview cases (folded into A, B, D above).

Deferred, not planned: registries (official registry, Glama, Smithery), LiteLLM gateway, Prefect Horizon, Cloudflare, mcpo, mcp-remote, deeper gateway stage, multi-server composition beyond S03.06, reference runtime and vector-index material from the codex reports, formal information-flow proofs, full IAM design (S08).
