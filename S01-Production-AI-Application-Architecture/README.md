# S01: Production AI Application Architecture

Status: **Drafted** (structure set 23 October 2026; all eight chapters given a first written pass the same day, consolidated from the earlier production-architecture prep contract, its 22 golden answers, the AI Application Architecture book skeleton and the interview knowledge-base concept notes).

The whole application an agent lives in: the request path, state, control plane, tenancy, cost and deployment. The diagram every later chapter zooms into.

The governing rule for the section: **an LLM application is ordinary deterministic software with one probabilistic component inside it. The model proposes; services own identity, state, authorization and side effects.** Every chapter is one place where that rule has to be made concrete.

## Learning order

| Subsection | What it covers |
| --- | --- |
| [Reference Architecture](S01.01-Reference-Architecture/README.md) | The one diagram: client → gateway → orchestration/harness → model → tools (MCP) → data and backends, with state, policy, evals and observability as cross-cutting planes; what each box owns; where S02–S09 plug in. |
| [Request Path: Sync, Streaming, Async, Background](S01.02-Request-Path/README.md) | One user request end to end; streaming tokens and tool events; async and background runs for long tasks; timeouts, deadlines, cancellation; Foundry background mode and AgentCore runtime sessions. |
| [State, Sessions and Storage](S01.03-State-Sessions-and-Storage/README.md) | Conversation history, task state, artifacts, approvals and long-term memory as separate stores with separate owners; keys, versions, retention; what the model sees versus what the system records. |
| [Control Plane: Routing, Config, Versioning, Release](S01.04-Control-Plane/README.md) | Model routing and fallbacks, prompt and tool-definition versioning, feature flags, canary releases, config as code; evals as the release gate (S05); rollback. |
| [Multi-Tenancy and Identity Propagation](S01.05-Multi-Tenancy-and-Identity-Propagation/README.md) | Tenant isolation at every layer (prompt, tools, data, cache, traces); the user's identity carried to tools (OAuth passthrough, on-behalf-of) versus the agent's own identity; pointers to S03.03 and S08. |
| [Cost and Latency Budgets](S01.06-Cost-and-Latency-Budgets/README.md) | Where time and money go per request (prefill, decode, tools, retrieval); SLOs; prompt caching, batching, model tiers; cost per successful task; links to T-Inference for serving internals. |
| [Deployment Topologies](S01.07-Deployment-Topologies/README.md) | Foundry (Agent Service, Container Apps, Functions, private networking), Bedrock AgentCore (Runtime, Gateway), Vertex, and self-hosted (Kubernetes); where MCP servers run; network boundaries; the same ticket agent on each. |
| [Reliability: Retries, Idempotency, Backpressure](S01.08-Reliability/README.md) | Failure modes of an LLM app (timeouts, partial tool failure, rate limits, lost responses); retry budgets, idempotency keys, circuit breakers, graceful degradation; operation keys and reconciliation from S03.04 generalised. |

## Where the prior work went

The chapters consolidate three earlier bodies of work. Nothing was dropped; each item below names the chapter that now owns it.

| Prior concept (prep contract) | Depth | Now in |
| --- | --- | --- |
| Application anatomy (seven planes; Bind, Ground, Gate, Prove; prototype to regulated pilot) | design | S01.01 |
| Production control architecture (irreversible-action control trace; agent versus deterministic boundary) | design | S01.01 for the boundary, S01.04 for the control matrix, S01.08 for idempotency |
| Python API boundary (tenant-aware async streaming; durable webhook delivery) | prototype | S01.02 for the endpoint, S01.08 for the webhook shape |
| Customer-facing frontend (two-day demo choice; production-pilot redesign) | design | S01.02 |
| Model-provider SDK boundary (tool loop, schema, streaming, retries; four-hour outage) | prototype | S01.02 for the client, S01.08 for the outage |
| Provider and serving topology (direct versus managed access; realtime versus batch) | prototype | S01.07 for placement, S01.02 and S01.06 for batch |
| Inference observability (SLO and alert design; multi-plane incident diagnosis) | design | S01.06 for SLOs, S01.08 for the incident |
| Batch and streaming data path (backfill plus stream; hot partition, late data, replay) | prototype | S01.03 for identity, order, lineage and checkpoints |
| Git, CI and reproducibility (PR workflow; environment and dependency drift) | prototype | S01.04 |
| Production-shaped deployment (build and walkthrough; live degradation and recovery) | prototype | S01.07 for the deliverable, S01.08 for recovery |
| Technical ownership and defence (architecture choices and failure limits; 100-times scale) | prototype | S01.01 for the request-order walk, S01.06 for the 10x and 100x defence |

The earlier six-chapter book skeleton maps as: system boundaries to S01.01, model and runtime to S01.04 and S01.07, orchestration to S01.02 and S04, data and state to S01.03, reliability and operations to S01.06 and S01.08, and the architecture review checklist into S01.01. The knowledge-base concept notes on inference metrics, routing and cost per task feed S01.06; those on tenant isolation, RBAC and ABAC, residency and audit logs feed S01.05; those on agent state, approvals and idempotency feed S01.03 and S01.08. Interview-prep scaffolding (sources, provenance tiers, readiness effects, question identifiers) was deliberately left behind; the questions themselves appear under each chapter's "Interview probes".

## Integration exercises

Six timeboxed design exercises, each combining two or three chapters. Each has a deliverable, three success checks and a failure branch to answer under time pressure. These are design exercises; their presence here is not evidence that any has been completed.

| Exercise | Chapters | Timebox | Deliverable | Failure branch |
| --- | --- | --- | --- | --- |
| Application path | S01.01, S01.02 | 25 min | Annotated sequence diagram plus UI and API contracts for start, chunk, cancel, reconnect, approve and fail; state ownership explicit; disconnect cancels or safely detaches; tenant and approval boundaries enforced outside the model | The browser disconnects while the model is streaming and the server continues expensive work |
| Provider boundary | S01.02, S01.07 | 25 min | Placement decision record, provider-interface sketch and failure-classification table; retries distinguish safe from unknown outcomes; fallback evaluated rather than assumed equivalent | The primary provider rate-limits, then fails after partial output |
| Data path | S01.03, S01.08 | 30 min | Data-flow diagram, checkpoint and idempotency contract, executable replay assertion; batch and stream converge on one schema; replay does not duplicate the durable effect; lineage identifies source and processing version | A retry overlaps a late event during a tenant backfill |
| Production control path | S01.04, S01.06 | 25 min | Requirement-to-control-to-signal matrix and a staged rollout decision; every gate has an owner and threshold; business and technical signals both present; rollback contains irreversible effects | Business KPIs fall while infrastructure health remains green |
| Delivery chain | S01.04, S01.07 | 20 min | Release checklist, minimal CI gate, configuration contract, rollback and recovery narration; artifact reproducible from a clean checkout; secrets and environment inputs validated | The release passes locally but fails after customer-specific configuration is injected |
| Ownership chain | S01.01, S01.07, S01.08 | 20 min | Five-minute code defence in request order, a tested repair and a precise proof and non-proof statement; the repair is causal and regression-tested | An interviewer selects an unfamiliar generated code path and asks for a live repair |

## Scenarios

Fourteen rehearsal scenarios carried from the prep contract, grouped by shape. Prompts reported from real interviews are reconstructions; none is claimed to have been asked verbatim.

**Full builds**

| Scenario | Timebox | Prompt | Primary chapters | Failure branch |
| --- | --- | --- | --- | --- |
| Semantic product search | 6 h plus 10-min walkthrough | Build semantic product search a chat client can call; show relevance, failure behaviour and the path from demo to production; one safe degraded mode | S01.01, S01.02, S01.03, S01.07 | The catalogue doubles mid-demo and one index partition is stale |
| Customer solution and demo | 6 h plus 15-min demo | Choose a real enterprise workflow, build the smallest convincing solution, present why it should or should not advance; identity, data handling and approval boundaries included | S01.01, S01.04, S01.07 | The customer forbids retention of prompts and retrieved documents |
| Plan, build, review | 30-min plan, 2-h build, 30-min review | Plan one useful product, build the narrowest valuable workflow, review code and trade-offs; every material decision owned | S01.01, S01.04, S01.07 | The chosen SDK abstraction prevents the required recovery path |
| Mini team inbox | 2 h plus 20-min review | Domain core of a team inbox: conversations, authorized sends, unread cursors, lifecycle transitions; retries never create duplicate visible messages | S01.02, S01.03, S01.05, S01.08 | Two clients reconnect and replay the same send concurrently |

**Timed architecture**

| Scenario | Timebox | Prompt | Primary chapters | Failure branch |
| --- | --- | --- | --- | --- |
| Private-corpus RAG | 45 min | Enterprise assistant over private documents with per-user permissions, freshness and evidence-backed answers; multi-tenant; permissions change during the day; no cross-tenant cache leakage | S01.01, S01.03, S01.05 | A user's group membership is revoked while an answer is streaming |
| Durable webhook delivery | 45 min | Accept customer, JSON payload and destination URL; deliver and expose status for 24 hours; destinations slow or malicious; outcome can be unknown | S01.02, S01.08 | The receiver commits the event but drops the response |
| Two-week messaging MVP | 45 min | Design a team-messaging product as a two-week MVP, then make delivery reliable without overbuilding v1; per-conversation ordering | S01.02, S01.03, S01.07 | A reconnecting client receives an old cursor after failover |
| Ambiguous AI system design | 45 min | Turn an underspecified enterprise AI request into a defensible architecture; requirements arrive incrementally; one action is irreversible | S01.01, S01.04, S01.08 | The interviewer changes the data-residency requirement halfway through |
| Regulated provider placement | 40 min | Choose direct API, Bedrock or Vertex for a regulated customer; private connectivity preferred; a new model feature is time-sensitive; audit evidence mandatory | S01.05, S01.07 | The selected managed platform trails a required feature by six weeks |
| Claims document pipeline | 60 min | Backfill ten years of files while processing new events through the same governed sink; tenant isolation; late and duplicate events; schema changes during backfill | S01.03, S01.08 | One large tenant becomes a hot partition and starves the live stream |

**Incident defence**

| Scenario | Timebox | Prompt | Primary chapters | Failure branch |
| --- | --- | --- | --- | --- |
| Four-hour provider outage | 30 min | Primary provider fails for four hours against a 99.9% SLO; lead the technical response; partial streams, behaviour-changing fallback, queued writes with unknown outcomes | S01.04, S01.08 | The fallback passes health checks but violates a high-risk policy slice |
| Latency, duplicate-write, missing-evidence incident | 35 min | p95 from 1.2 to 9.4 s, duplicate CRM writes after retries, answers without evidence; diagnose all three without replaying unknown writes | S01.06, S01.08 | Disabling retries improves latency but increases lost updates |
| 100-times scale defence | 30 min | The take-home works; defend what changes and what stays stable at 100x data and traffic; no generic horizontal scaling; first measurement before each change | S01.06, S01.01 | The new bottleneck is a third-party synchronous API with fixed quotas |
| Broken API service debugging | 45 min | A service leaks memory, stalls under concurrency and intermittently returns stale results; diagnose and repair live; observations precede edits | S01.02, S01.04, S01.08 | The local repair passes but fails in CI because runtime configuration differs |

## Completion and evidence

Chapter status is documentation status. No S01 build exists yet; the thin vertical slice described in S01.01 (one approval-gated write through the whole path, done when five deterministic failure tests pass) is the first build when one is scheduled. Sources carried from the earlier notes were not re-fetched on 23 October 2026 and are marked as such in each chapter.

[Back to AI Production Systems](../README.md)
