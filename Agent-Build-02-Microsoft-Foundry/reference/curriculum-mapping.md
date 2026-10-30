# Foundry curriculum mapping and depth standard



This addition translates the job-ad synthesis into the fourteen-module Foundry curriculum. The original numbered requirements and exercises remain the source inventory. A requirement being mapped does not mean its implementation works or that the learner has demonstrated mastery. The job-ad attribution is inherited from the supplied synthesis, not an independent re-review of each advertisement.

The [complete build coverage matrix](production-build-coverage.md) maps all 229 checkbox occurrences from the [preserved merged checklist](production-build-checklist.md) to module-level build contracts; the table below preserves the original architecture/code crosswalk.

## Curriculum mapping and depth

Architecture and code item numbers below cover the complete original inventory. Each item has one primary home; supporting modules may link to it. Certification and wider-platform material may have an external home rather than expanding this section indefinitely.

| Module or destination | Architecture items | Code items | Required depth and evidence |
|---|---|---|---|
| F01 Reference Architecture and WAF | 1, 2, 9, 14 | — | Architecture 3: defensible design, ADRs, targets and measured results; revisit after the build. |
| F02 Landing Zones and Networking | 11 | C17 | Architecture 3 / code F2: network paths, DNS, policy, Bicep review and a scoped reproducible deployment. |
| F03 Identity and Zero Trust | 3 | C1 | Architecture 3 / code F3: token and trust flows, least privilege, denied-access diagnosis. |
| F04 Foundry SDKs and Deployment | 4, 27 | C2, C3, C8, C11, C19, C25, C27 | Core SDK/Python F3; configuration/CLI F2; alternative provider and .NET awareness or bounded comparison. Fundamentals embedded as prerequisites. |
| F05 Creating Agents | 5, 12, 19, 22 | C4, C12, C20, C21 | Core framework F3, persistence F2; compare hosting and alternative frameworks through bounded exercises. Voice remains awareness. |
| F06 Agent Tooling MCP and Integration | 10, 18 | C13, C16, C26 | Integration architecture 3; messaging/MCP F2 with selected timed drills; low-code alternatives awareness. |
| F07 RAG on AI Search | 6, 13, 21 | C5, C10, C14, C23 | Search F3; ingestion/storage F2; data-platform integration and GraphRAG comparison before optional builds. |
| F08 Evals Tracing and Release | 8, 16 | C6, C7 | F3 evaluation and telemetry; measured success, p95, cost, release gate and rollback evidence. |
| F09 APIM AI Gateway | 20 | C18 | F2 policy authoring; token limits, identity, routing, fallback and failure evidence. Supports architecture items 2, 8, 16. |
| F10 Security and Governance | 15, 24 | — | Architecture 3 for threat/control and governance evidence; applies F03 identity and F02 resource-policy foundations. |
| F14 Responsible AI and Safety | 7 | C9, C24 | Architecture 3 for harm and oversight decisions; Content Safety F2; bounded red-team evidence through F08. |
| F11 Copilot Studio and M365 Boundary | 17 | C15, C22 | Architecture 3 for boundary decisions; Graph F2; one Copilot integration demonstrated with evidence in the existing Copilot section. |
| F12 Fine Tuning and Model Routing | 23 | — | Decision-level architecture 2; preserve existing deeper labs. C3 supplies platform context, C18 owns routing implementation. |
| F13 Foundry Local | — | C28 | Awareness F1, optional F2 build; preserve existing local labs. Original proposal’s “28” means C28. |
| Existing certification section | 25, 26 | — | Vocabulary and current exam objectives; verify exam status before scheduling. No duplicated certification curriculum. |

F08 owns FinOps measurement, F01 owns cost assumptions and budgets, and F09 owns gateway enforcement. F03 owns identity principles; F06 applies them to MCP. F10 owns security threat/control and governance evidence; F14 owns harm assessment, safety controls and human oversight; F08 owns evaluation execution. F11 links to Agent-Build-03-Microsoft-Copilot-Studio for authoring depth.

## Depth contract for every core module

Each module must include prerequisites, clear learning outcomes, explanations with a worked scenario, design alternatives, failure diagnosis, learner exercises, evidence requirements, and dated official references. Avoid a chapter that is only a list of links. Split substantial material into focused documents when useful, without generating empty scaffolds.

Record architecture score and code score separately, initially **unassessed**. Evidence records include date, task, assistance allowed, result, limitations, and next gap. F3 requires a timed learner-written exercise without AI; copied or agent-generated code is not evidence of F3. Architecture 3 requires built evidence and real numbers, not just a diagram.

### F01 Reference Architecture and WAF

Teach the end-to-end request path, ownership boundaries, hosting choice, data classification, NFR tradeoffs and all five WAF pillars. Begin with a small reference design; expand only to meet a stated requirement. Do not imply every service in item 1 must be deployed.

Required outputs: HLD and request sequence; component identity/network/residency/logging matrix; NFR budget; three ADRs covering platform, identity and retrieval; target/transition views; rollout/rollback and handover outline; ten-minute whiteboard and three-minute spoken walkthrough. Distinguish targets, illustrative calculations and actual measurements.

Failure exercise: model throttling or unavailable retrieval, with a defensible degraded mode and recovery path. Completion requires defending alternatives and reconciling the original budget with observed quality, latency and cost.

### F03 Identity and Zero Trust

Teach applications versus service principals, system/user-assigned identities, token audience/scopes, delegated versus application permissions, OBO, developer authentication, CI federation, agent identity and per-tool authorisation. Cover SAML briefly as enterprise context. Use existing OAuth/MCP fundamentals as prerequisites, not duplicated chapters.

Required outputs: token-flow diagrams; principal-to-resource permission matrix; a learner-written token-provider client; one delegated/application-permission comparison; MCP audience/scope validation exercise; permission-filtered retrieval design linked to F07. Apply Zero Trust to identity, network, application, data and visibility.

Failure exercises: wrong audience, insufficient role, expired credentials, missing consent and attempted cross-user retrieval. Completion requires explaining 401 versus 403, demonstrating denied access, and showing that tokens and private content are absent from logs. Managed identity is an Azure runtime path, not a replacement for local Mac sign-in.

### F10 Security and Governance, with F14 Responsible AI and Safety

F10 teaches trust boundaries, excessive agency, insecure output handling, exfiltration, supply-chain threats and governance controls. F14 teaches use-case harms, content controls, prompt-injection safety, human oversight and responsible-AI assessments. Map threats to preventive, detective and recovery controls across identity, retrieval, tools, gateway and runtime. Explain where filters help and their limits.

Required outputs: F10 owns the scenario-specific threat model, security control/evidence matrix, audit/release governance and incident response notes. F14 owns the harm/control/evidence matrix, safety red-team interpretation, system-card and impact-assessment outlines, and human-oversight criteria. The shared A11 pack links both sets; F08 retains evaluation execution and results. Link existing red-team and safety labs rather than copying them.

Failure exercise: an injected retrieved document requests an unauthorised tool action. Evidence must show the control outcome and remaining risk. Regulatory study must distinguish jurisdiction, entity, use case and obligations; a checklist does not establish compliance. Verify applicable official guidance when writing legal mappings. No mandatory exhaustive legal survey or full governance-tool deployment.

### F11 Copilot Studio and M365 Boundary

Teach platform choice, grounding permissions, delegated/application access, DLP, oversharing, integration ownership and lifecycle. Distinguish a managed service, an orchestration framework and an authoring platform; they can be combined.

Required outputs: a platform-choice table; sequence diagram for one Copilot-to-Foundry or MCP integration; permission/DLP analysis; demonstrated handoff with results stored in the existing Copilot section; release/rollback and operational ownership explanation.

Failure exercises: denied consent, inaccessible grounding and integration failure. Completion requires demonstrating the boundary and defending when pro-code is warranted. Keep detailed Copilot authoring and M365 implementation in the existing companion section.

## Strengthening the existing modules

- F02: complete the existing skeleton; validate network assumptions per service and deployment type. Include DNS and egress diagnosis, policy evaluation and residency constraints.
- F04: retain the substantial SDK/deployment material. Add endpoint/client distinctions, deployment types, quotas, configuration, secret rotation and CI federation where missing. Keep dependency upgrades separate from path migration.
- F05: retain all existing hosting/framework labs. Add persistence ownership, TTL, concurrency, audit design and hosting decision exercises. Partition keys must follow access patterns rather than be copied as universal defaults.
- F06: add a scoped durable tool workflow covering correlation, duplicate delivery, idempotency, poison handling and approval. Include compensation and recovery reasoning; avoid deploying every messaging product.
- F07: precede Foundry IQ with foundational hybrid/semantic retrieval, document ingestion with page citations, permission enforcement, freshness and index replacement. Compare vector-only, hybrid and semantic retrieval on a labelled dataset. GraphRAG and data-platform integrations are optional extensions after this core.
- F08: extend existing evaluation/tracing content with release manifests, real KQL measurements, offline/online success definitions and rollback of separately versioned components. State dataset size and measurement limitations.
- F09: expand the current short outline into substantive policy teaching and exercises. Show token limits, managed identity, routing, fallback, cache isolation and metrics. Specify stable endpoints and conversation behaviour before assigning a canary exercise.
- F12/F13: preserve all fine-tuning and local-runtime assets. Lower study priority does not mean reduced or deleted content.

## Shared scenario and artefacts

Use the existing support-ticket agent, extended into a regulated-client scenario, to connect the learning: authorised retrieval → approved tool execution → measured quality/latency/cost → gateway controls → release and governance evidence. Each stage remains independently understandable and must not import another stage's code.

Working definitions for this curriculum: **A3** is the reference build plus its measured three-minute walkthrough; **A11** is the governance and safety evidence pack; **A12** is the architecture and handover pack. These explain the labels used in the original synthesis; they do not assert the existence or contents of external project folders.

Every numerical statement must be labelled as a target, illustrative example or measured result. Measured evidence includes workload, dataset, environment, time window and method. No fabricated p95, cost, quality score or study completion.

## Repository preservation and migration rules

The future update preserves all existing labs, notebooks and outputs, sketches, source, fixtures, configuration, references and dependency declarations. Inventory tracked, untracked and ignored content and record hashes before moving files. Do not include secrets or private local state in published material.

Move the existing modules intact: F01→F02, F02→F04, F03→F05, F04→F06, F08→F07, F05→F08, F09→F09, F06→F12, F07→F13. Normalise names and trailing spaces, then repair links and path references across Markdown, scripts and notebook cells. The initial migration added F01, F03, F10 and F11 as substantive documentation; the subsequent approved split separates F10 Security and Governance from F14 Responsible AI and Safety. add study logs only for actual learning activity.

Keep labs-setup, the existing .env.example and reference reading map. Extend only identified gaps. Preserve original dependency environments during structural migration; document their compatibility constraints. Reconciling existing shared environments with the self-contained-stage rule is a separate explicit change. New stages require their own dependencies, lockfile, fixtures, source and tests when their implementation is requested.

The learner writes functions, adapters and tests. Agent-authored explanations or examples never count as learner mastery. No empty lab scaffolds, fabricated tests or passing status for incomplete work. Actual implementation verification requires relevant tests and at least 80% coverage; a document-only migration needs content/path checks, not broad suites.

## Technical review and corrections — 30 October 2026

This review does not certify all original vendor claims or lab execution. The original package paragraph is retained as historical context and must not be used as an installation instruction.

- The original architecture tier targets and code tier-2 wording conflicted. The rating paragraph now distinguishes architecture 3 from tier-2 code F2, with selected F3 drills. The original RPO/RPO typo is corrected to RPO/RTO.
- Items 5, 19 and C3 mix classic threads/runs/connected-agent language with newer Foundry APIs. Use the current API generation for new exercises and retain classic terminology only in labelled migration comparisons. Microsoft documents migration from threads to conversations and runs to responses: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/migrate . Do not translate tool availability mechanically between generations.
- The historical azure-ai-inference retirement statement uses a past date in future tense. The exact retirement date is unresolved in this review; do not repeat it as verified. Verify current migration guidance before modifying examples. Likewise, verify Agent Framework package/import names and provider-specific authentication against the selected release, rather than treating a 1.0 launch statement as a current pin.
- Record exact package versions and Python/runtime compatibility per environment, with separate “declared”, “installed” and “tested” status. Existing repository documentation records framework/evaluation dependency differences; do not flatten them into one shared upgrade. SDK reference: https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview .
- Replace blanket “private endpoints for every hop” as a design rule with a per-hop network-path and capability assessment. Preserve the original requirement as an interview constraint to analyse, not a universal platform guarantee. Architecture reference: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-chat .
- Treat regulatory mappings, service availability, role names, preview status, SDK method names and certification dates as dated verification tasks before teaching or deployment. Item 25's exam label must be checked against the current certification catalogue before booking or scheduling.
- A budget alert is not a guaranteed spending cap. Separate alerting, quotas, cleanup and any explicitly authorised shutdown automation. Treat APIM canary routing as an exercise requiring endpoint/session design, not proof that every hosted-agent service supports traffic splitting.

## Acceptance checklist for the future curriculum update

- All 27 architecture items and 28 code items have a primary destination and depth target.
- Four new modules contain explanations, alternatives, failure cases, learner exercises and evidence criteria.
- Every original repository file is accounted for after migration; changed links and paths are reviewed.
- Source dates, API generations, historical examples and unverified instructions are clearly distinguished.
- Scores remain unassessed until demonstrated; existing files alone are not proof of functionality.
- New learning work is distinguished from moving existing material. Repository changes, cloud deployment and publishing require their own explicit instructions.
