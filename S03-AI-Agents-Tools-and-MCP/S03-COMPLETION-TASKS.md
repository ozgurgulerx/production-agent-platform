# S03 completion tasks (21 Oct 2026)

Goal: S03.01–06 known cold, with two known soft spots (hands-on evidence, platform detail) closed by S04 and S03.03b. Tick in order within each group. Times are estimates. Merges the three reviews of 21 Oct; the coverage review's proposed S03.07–09 chapters are folded in here, not added.

## Status after the documentation update

Reviewed against the local repository on **21 October 2026**. Checked boxes mean the specified documentation exists, not that a build, security control, conformance suite or recall exercise passed. The remaining work is hands-on evidence and learning; keep S03.04–06 concept expansion frozen unless implementation reveals a concrete gap. No implementation, dependency or CI changes were made for this update.

Evidence index: [S03 overview](README.md), [S03.02 narration](S03.02-Functions-to-MCP-Tools/README.md#narrate-one-complete-agent-call), [S03.03 identity lifecycle](S03.03-MCP-OAuth2.1/README.md#identity-lifecycle-who-stops-what), [operations one-pager](S03.04-MCP-Tool-Design/README.md#operations-one-pager-from-a-call-to-a-recoverable-service), [S03.05](S03.05-MCP-Context-Efficiency/README.md), [S03.06](S03.06-Client-as-Trust-Boundary/README.md).

## A. Before S03.03b

- [x] **Record protocol support per stage.** S03.02 pins `mcp 2.3.0`, whose installed registry supports 2026-07-28 and earlier handshake revisions; S03.03 pins `mcp 1.26.0` (latest 2025-11-25). Both are stated in the S03 overview and S03.05 scope. Actual interpreter and on-wire revision remain evidence to record for each run; a lockfile does not establish the shared environment.
- [ ] **Run revision-matched MCP Conformance against S03.03.** Pin suite version/commit and requirement set; confirm applicable server-role scenarios, transport and test authentication. Record executed checks, skips, failures and redacted wire evidence. State a scoped result only after execution; do not infer the exercised revision from the suite label or add a blanket badge. See S03.03's priority TODO. Harness adaptation may be needed; no run or CI integration is claimed.
- [x] **Write the one-page MCP explainer** (new section in S03 README): JSON-RPC 2.0, host/client/server, tools/resources/prompts, stdio vs Streamable HTTP, capability negotiation, what 2026-07-28 changes, plus one annotated successful call trace and one failed one (which layer failed: transport, JSON-RPC, protocol error, tool `isError`). The "explain MCP in two minutes" opener. (~1 h)
- [x] **Write the comparison and "when not to use MCP" section** (S03.04 or S03 README): MCP vs function calling vs OpenAPI/plugins vs A2A; cases where MCP is the wrong choice (single client and backend, latency-critical, batch); server boundaries by credentials, ownership and blast radius (should HR, tickets and payments share a server?). (~30 min)
- [x] **Fix the S03 README index:** S03.05 and S03.06 are linked and labelled as design material. The completion checklist is linked too.

## B. Consistency fixes — documented

- [x] **S03.05:** add a "minimum viable build" line (steps 1, 2, 3 keyword arm, 5 projection arm, 6); distinguish the recall drill from the reference index (overlap retained intentionally); align the interview line with cost-per-successful-task; verify the `posts/2026-07-28/` link resolves; confirm "S03.04 section 10" exists in the committed S03.04.
- [x] **S03.06:** restore the attack × defence matrix as the stated deliverable (six attacks: description poisoning, shadowing, rug pull, result injection, elicitation phishing, sampling abuse; defences as columns); add MCP-Scan, Promptfoo red-team and Docker MCP Gateway to sections 10–11; pick 2025-11-25 as the base spec and note 07-28 deltas; rename "IntentGrant (from the notes)" to task grant; replace the internal-notes source line with public references; add an elicitation paragraph in section 7.
- [x] **S03.02 / S03.03:** end-to-end call narration (user request → every message → backend effect; call-id vs operation-key; sequential vs parallel dependencies; bounded loop and stopping conditions).
- [x] **S03.03:** identity lifecycle section (token refresh and re-authentication, consent expiry, JWKS rotation, user deprovisioned mid-task: which component stops what, tenant isolation); deeper agent identity stays in S08.
- [x] **S03.03:** transports and lifecycle paragraph; spec-revision note; one line on sampling deprecation in 07-28.
- [x] **S03.04:** spec-revision note; link section 10 observability to W3C trace context.

## C. Coverage additions — documented

S03.05 — documentation completed, experiments unrun:

- [x] Parallel tool calls: comparison-table row and metrics; matched concurrency is an experimental control.
- [x] Catalogue refresh cost: `tools/list` frequency, `listChanged`, client caching of lists; paragraph in strategy A.
- [x] Two-tier descriptions (short in catalogue, `describe_tool`/`detail` on demand).
- [x] Unloading discovered tools over long sessions, with a "loaded definitions at step n" metric.
- [x] Delegation as context partitioning: one paragraph in "Three independent decisions".
- [x] Model routing (cheap model for discovery): one line in B.
- [x] Progress notifications: large-data row explicitly separates status updates from partial-result streaming.
- [x] One resource and one prompt specified as optional contracts in the large-data step; not implemented or added to the minimum build.

S03.06 — documentation completed, controls/attacks unrun:

- [x] Explicit threat model up front: attackers, goals, trusted base.
- [x] Supply chain and installation: registries, `npx`/`uvx`, pinning, signatures, container isolation, review before enabling.
- [x] Final-output exfiltration: markdown image links, link unfurling; row in section 8.
- [x] Six-attack matrix (see B) including elicitation phishing and sampling abuse.
- [x] Resource exhaustion as a named attack.
- [x] Platform mapping table: Foundry (agent identity, MCP tool config, approval), AgentCore (Gateway, authenticated policy inputs, Cedar), Agents SDK (guardrails, `tool_filter`, approval callbacks).
- [x] Standards paragraph: OWASP LLM Top 10, OWASP agentic guidance, MCP security best practices, MITRE ATLAS.
- [x] Third-party data handling line (remote servers leave your retention/residency boundary).
- [x] Detection layer paragraph: injection classifiers, call-pattern anomalies, canaries.
- [x] Adversarial benchmarks: AgentDojo, InjecAgent, plus the scanners.

## D. Build (the soft spots)

- [ ] **S04 evals stage, target 1 Nov, with the capstone as the scenario set** (from the coverage review; replaces a separate S03.09). Each step is an eval case with a deterministic check: (1) trace a read-only request; (2) user-scoped auth, two tenants; (3) consequential action with bound confirmation; (4) response lost after backend commit; (5) worker restart and reconciliation; (6) hostile metadata or ticket content; (7) expired credentials, revoked access, changed schema; (8) quota exhaustion and latency regression; (9) inspect traces and backend state, justify recovery and the release decision. Harness: tool-selection accuracy, discovery recall, held-out questions, end-state checks, repeated runs. Add conformance to CI only after a compatible local run is established. MCPJam is already noted in S03.04 as the off-the-shelf alternative; no integration is required.
- [ ] **S03.03b Foundry/Entra build.** The S03.06 platform mapping is documented; platform setup and observed enforcement remain outstanding. The earlier half-day estimate is tentative.
- [ ] **S03.06 build at demo depth:** malicious `fx-rates` server, scanners and bounded Docker MCP Gateway step. Exercise the six named attack paths where supported plus output exfiltration/resource exhaustion against the combined controls, with benign cases. Matrix cells stay `NR` until run; record unsupported paths and N/A controls explicitly. Separate detection, proposed calls, blocked calls and backend effects.
- [ ] **S03.05:** minimum viable build only, after S04: steps 1–2, keyword arm of 3, projection arm of 5, cache comparison in 6, and the results/decision note in 7. The other arms, resource/prompt implementation and 30-step history experiment remain optional.
- [x] **Operations one-pager documented** in S03.04 §10 and linked from S03.06 §12: deployment, versioning, W3C trace context, latency decomposition, replica races, retries, shutdown, incident response and regression capture.
- [ ] **Produce operations evidence:** demonstrate restart recovery, duplicate-intent handling across workers, bounded shutdown and a captured regression. The existing process-local refund ledger does not establish these properties.

## E. Learn by heart (retrieval, not re-reading)

- [ ] Answer the S03.04 section 11 and S03.06 section 12 questions out loud, no notes; log misses in the quiz sheet.
- [ ] Two-minute spoken answers: "What is MCP?", "How would you expose our systems to an agent safely?", "When would you not use MCP?"
- [ ] Draw the S03.03 responsibility table and the S03.06 enforcement diagram from memory.
- [ ] Diagnostic follow-ups, one each: SDK call hangs (which layer); stream breaks after a refund committed; user loses access mid-export; two replicas retry the same operation; latency doubled, error rate flat.
- [ ] Create basic Anki cards for observed recall misses; no cards or quiz results are claimed yet.

Rejected: new chapters S03.07 protocol mechanics, S03.08 production systems, S03.09 interview cases (folded into A, B, D above).

Deferred, not planned: registries (official registry, Glama, Smithery), LiteLLM gateway, Prefect Horizon, Cloudflare, mcpo, mcp-remote, deeper gateway stage, multi-server composition beyond S03.06, reference runtime and vector-index material from the codex reports, formal information-flow proofs, full IAM design (S08).
