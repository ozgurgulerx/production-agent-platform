# F01 capability builds — Architecture and production evidence

## Build contract

Status: **planned; functionality unverified**. Build one capability at a time using the existing module and labs. Record environment/dependency versions, permitted assistance, positive and negative results, and trace/test evidence. The learner writes code and tests; these contracts do not supply hidden implementations. Verify dated API and availability claims before execution.

### Reference architecture and ownership

- [ ] Build: Draw the support-ticket request from authenticated user through gateway, agent, retrieval, tool and stores. For each hop record identity, network path, residency, logs and failure owner. Defend hosted vs self-hosted and document platform/identity/retrieval ADRs.
- [ ] Verify: Inject unavailable retrieval and model throttling in the chosen test environment; explain degraded behavior and recovery without claiming a target as a measurement.

### Well-Architected numerical contract

- [ ] Build: Assign explicit latency, token, cost, availability and recovery targets to the request path. Use actual traces from F08 to reconcile them. Include reliability, security, cost, operations and performance trade-offs.
- [ ] Verify: Present measured workload, sample count and interval; identify the largest budget miss and show how a changed design would be tested.

### Architecture artefacts and fundamentals

- [ ] Build: Produce HLD/LLD, component matrix, ADRs, release/handover runbook and a three-minute A3 walkthrough. Explain subscriptions, management groups, tenants, policy vs RBAC vs locks and regional choices.
- [ ] Verify: Review an intentionally inconsistent permission/network/residency diagram and correct it with evidence. Cross-reference Certs/AI-103 and AZ-305; retained AI-102 wording is historical, not a current exam plan.

## Exact checklist targets

Each ID below is a distinct occurrence in the [full coverage matrix](../reference/production-build-coverage.md). Source wording is retained, including historical names and unfinished placeholders; it is not a fresh API guarantee. Compound items may require several small builds. Mark complete only after recording evidence.

- [ ] **CB001** — Write the implementation yourself; record the code path and dependency versions.
- [ ] **CB002** — Demonstrate the successful flow and a relevant failure/denied-access flow.
- [ ] **CB003** — Capture a reproducible command, trace/test result, and relevant measured latency/cost/quality.
- [ ] **CB004** — Explain the identity, network, data, safety, and rollback boundaries relevant to that build.
- [ ] **CB005** — Mark complete only with evidence; repo files and sample code do not establish proficiency or successful deployment.
- [ ] **CB159** — Every component must have an answer to: identity, network path, data residency (UK South / UK West, EU Data Boundary), what is logged, what is private.
- [ ] **CB160** — Doc anchors: Azure Well-Architected Framework (five pillars, AI workload guidance), Azure OpenAI baseline reference architecture (Architecture Center), Foundry networking / Private Link docs, APIM GenAI gateway policies.
- [ ] **CB161** — Reliability: multi-region model deployments, APIM backend pools and circuit breaker, retry/backoff with jitter, idempotent tool calls, queue-based load levelling, graceful degradation (smaller model, cached answer, human route).
- [ ] **CB162** — Security: identity-first (no keys), least-privilege RBAC roles (Cognitive Services OpenAI User vs Contributor, Search Index Data Reader), private endpoints, CMK, Content Safety, prompt-injection controls, egress control for tools.
- [ ] **CB163** — Cost optimisation: PTU vs pay-as-you-go break-even, prompt caching, semantic caching at APIM, model routing (small-first), token budgets per feature, chargeback via APIM subscriptions.
- [ ] **CB164** — Operational excellence: tracing, eval gates in CI, prompt/version registry, release manifest, rollback of prompt/model/index versions, runbooks.
- [ ] **CB165** — Performance efficiency: streaming, parallel tool calls, async ingestion, index partitioning, embeddings batch sizes, PTU sizing arithmetic.
- [ ] **CB166** — Be able to put a number against each pillar for A3.
- [ ] **CB167** — Draw from memory, in under ten minutes, with these named: Entra ID (user identity, app registrations, managed identities, agent identity), APIM in front of Azure OpenAI / Foundry models (AI gateway: token-rate limits, quota per consumer, semantic caching, model-fallback policy, key-less managed-identity auth, logging to App Insights / Event Hubs), Private Link + private endpoints + DNS zones for every PaaS hop, Key Vault (secrets, CMK), Azure AI Search (hybrid vector + BM25 + semantic ranker, security-trimmed indexes, indexers vs push), Azure OpenAI / Foundry model deployments (Standard vs Provisioned Throughput Units vs Data Zone / Global Standard, content filters), Foundry Agent Service or Agent Framework host on Container Apps / AKS, Cosmos DB (sessions, memory, audit), Storage (documents, eval sets), Document Intelligence (ingestion), Content Safety (prompt shields, groundedness, protected material), Azure Monitor + App Insights + OpenTelemetry (traces with span-level eval scores), Foundry Evaluations, Service Bus / Event Grid for async tool execution, Azure Functions / Durable Functions for long-running or human-approval steps, Defender for Cloud + Purview for data governance.
- [ ] **CB168** — Non-functional budget to state unprompted: p95 latency per hop, tokens per request, cost per 1k requests, availability target, RPO/RPO for memory and audit stores, max blast radius of a prompt-injection event.
- [ ] **CB169** — Every component must have an answer to: identity, network path, data residency (UK South / UK West, EU Data Boundary), what is logged, what is private.
- [ ] **CB170** — Doc anchors: Azure Well-Architected Framework (five pillars, AI workload guidance), Azure OpenAI baseline reference architecture (Architecture Center), Foundry networking / Private Link docs, APIM GenAI gateway policies.
- [ ] **CB171** — Reliability: multi-region model deployments, APIM backend pools and circuit breaker, retry/backoff with jitter, idempotent tool calls, queue-based load levelling, graceful degradation (smaller model, cached answer, human route).
- [ ] **CB172** — Security: identity-first (no keys), least-privilege RBAC roles (Cognitive Services OpenAI User vs Contributor, Search Index Data Reader), private endpoints, CMK, Content Safety, prompt-injection controls, egress control for tools.
- [ ] **CB173** — Cost optimisation: PTU vs pay-as-you-go break-even, prompt caching, semantic caching at APIM, model routing (small-first), token budgets per feature, chargeback via APIM subscriptions.
- [ ] **CB174** — Operational excellence: tracing, eval gates in CI, prompt/version registry, release manifest, rollback of prompt/model/index versions, runbooks.
- [ ] **CB175** — Performance efficiency: streaming, parallel tool calls, async ingestion, index partitioning, embeddings batch sizes, PTU sizing arithmetic.
- [ ] **CB176** — Be able to put a number against each pillar for A3.
- [ ] **CB177** — Three minutes: what is deployed, where, eval scores, p95, cost per 1k, the OAuth/MCP trust boundary, fallback and human-review path, what you would change for a bank. Every number real.
- [ ] **CB178** — HLD / LLD structure, ADR template and three real ADRs from A3 (platform choice, identity model, retrieval design), target and transition states, NFR budget table, threat model (STRIDE + OWASP LLM Top 10 + MITRE ATLAS), rollout/rollback plan, handover pack, design-authority review checklist, cost model. Defend each under challenge. This is A12.
- [ ] **CB221** — AI-102 objectives (week 9) — Foundry, Azure OpenAI, AI Search, Document Intelligence, Language, Vision, Speech, Content Safety, agents; the exam frames the vocabulary SI panels use.
- [ ] **CB222** — AZ-305 objectives (week 16) — identity, governance, data storage, business continuity, compute, networking, migration; the architect tie-breaker.
- [ ] **CB226** — Source B says “RPO/RPO”; Source A says “RPO/RTO”. Keep both source texts and set explicit recovery-point and recovery-time objectives in the build.
- [ ] **CB228** — Verify dated certification names and regulatory applicability before using them as current requirements; this merge makes no new certification or legal assessment.
- [ ] **CB229** — Verify source claims about memory, identity, deployment ownership, managed compute, and Toolbox against the chosen product/API version.

- [ ] **TOP-FUNDAMENTALS** — Architecture 27: resource groups/subscriptions/management groups, RBAC/Policy/locks, regions/zones, ARM/Bicep, tags/cost, Monitor/Log Analytics/App Insights, Key Vault/App Configuration, and Entra tenants.

## Completion evidence

- [ ] Store the artifact path, reproducible command, observed outcome, limitations and next gap in the existing study log.
- [ ] Preserve current labs; link to shared concepts rather than importing another stage’s implementation.
- [ ] Do not label a sample, empty test collection or planned experiment as verified functionality.
