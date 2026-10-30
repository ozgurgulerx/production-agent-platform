# F08 capability builds — Evaluations, telemetry, release and cost

## Build contract

Status: **planned; functionality unverified**. Build one capability at a time using the existing module and labs. Record environment/dependency versions, permitted assistance, positive and negative results, and trace/test evidence. The learner writes code and tests; these contracts do not supply hidden implementations. Verify dated API and availability claims before execution.

### Versioned evaluation contract

- [ ] Build: Maintain repeatable internal/external/combined questions with expected outcomes and dataset provenance. Target exact agent versions; distinguish violence, fluency, task adherence, groundedness, similarity and tool-call accuracy. Include custom rubrics where justified.
- [ ] Verify: Poll with a deadline, handle canceled/failed runs and fail on evaluator errors or missed thresholds. Demonstrate a deliberately bad agent version blocked by the gate.

### Trace and operational measurement

- [ ] Build: Instrument model, retrieval and tool spans with correlation and safe token/cost metadata. Configure sampling/redaction and write KQL for p95, errors, usage and cost per request. Compare offline judgments with online success measures.
- [ ] Verify: Inspect exported traces for sensitive data; test missing telemetry and model/tool error diagnosis. Record sample/window and cost source, not invented rates.

### Release and rollback

- [ ] Build: Create a manifest binding prompt/agent/model/index/toolbox/dataset versions and dependency locks. Apply the same quality definitions to CI and continuous evaluation; demonstrate canary and independent rollback.
- [ ] Verify: Block a bad release, restore prior versions and test conversation compatibility. Keep optimizer candidates separate from the evaluation holdout; require evidence rather than universal score-delta thresholds.

### FinOps and optimization

- [ ] Build: Measure tokens per feature, cost per 1,000 requests, PTU utilization where available and anomaly thresholds. Compare caching/routing/tier options against a quality constraint and workload profile.
- [ ] Verify: Replay a bounded cost spike or token-budget breach and verify alert/gateway response. Record historical pricing as a dated assumption and verify current prices before purchase.

## Exact checklist targets

Each ID below is a distinct occurrence in the [full coverage matrix](../reference/production-build-coverage.md). Source wording is retained, including historical names and unfinished placeholders; it is not a fresh API guarantee. Compound items may require several small builds. Mark complete only after recording evidence.

- [ ] **CB013** — plan and manage costs [link](https://learn.microsoft.com/en-us/azure/foundry/concepts/manage-costs)
- [ ] **CB060** — azd ai agent eval with eval.yaml and optimizer workflow (azd ai agent optimize, trace | dataset sources and CI quality gates)
- [ ] **CB122** — Maintain a repeatable dataset: internal, external, and combined-source questions.
- [ ] **CB123** — Run batch evaluations against a specific agent version.
- [ ] **CB124** — Evaluate violence, fluency, and task adherence; inspect scores and failures.
- [ ] **CB125** — *(empty source checkbox retained; resolve scope before implementation)*
- [ ] **CB126** — Built-in evaluators (`GroundednessEvaluator`, `RelevanceEvaluator`, `CoherenceEvaluator`, `FluencyEvaluator`, `SimilarityEvaluator`, `F1ScoreEvaluator`, safety evaluators via `AzureAIProject`, agent evaluators: `IntentResolutionEvaluator`, `ToolCallAccuracyEvaluator`, `TaskAdherenceEvaluator`), custom evaluator as a class or prompty, `evaluate(data=jsonl, evaluators={...}, azure_ai_project=...)`, column mapping, local vs cloud runs, thresholds and pass/fail, simulators (adversarial simulator, direct/indirect attack simulator), red-teaming agent, continuous evaluation on traces.
- [ ] **CB127** — Exercise: eval harness as a pytest module that fails CI when groundedness drops below threshold; run it in GitHub Actions on PR.
- [ ] **CB128** — Azure Monitor + App Insights + OpenTelemetry (traces with span-level eval scores),
- [ ] **CB129** — `configure_azure_monitor(connection_string=...)`, OpenAI instrumentation (`opentelemetry-instrumentation-openai-v2`), Agent Framework / Foundry tracing flags, GenAI semantic convention attributes (`gen_ai.request.model`, `gen_ai.usage.input_tokens`, …), custom spans around tools and retrieval, attaching eval scores to spans, sampling, PII redaction in traces, KQL queries over `dependencies`/`traces`/`customEvents` in App Insights for p95 and cost per request.
- [ ] **CB130** — Exercise: trace the tool-calling loop end to end, write the KQL that returns p95 latency and tokens per request by tool for the last hour.
- [ ] **CB131** — Foundry Evaluations: built-in evaluators (groundedness, relevance, coherence, fluency, similarity, safety evaluators, agent evaluators: intent resolution, tool-call accuracy, task adherence), custom evaluators, local vs cloud evaluation runs, continuous evaluation on traces.
- [ ] **CB132** — Observability: OpenTelemetry GenAI semantic conventions, Azure Monitor / App Insights, Foundry tracing, span attributes for tokens and cost, evaluator scores attached to spans, alerting on drift in eval scores or cost per request.
- [ ] **CB133** — Release engineering: prompt and agent versioning, eval gates in GitHub Actions, canary by APIM traffic split, rollback of prompt/model/index independently, release manifest, change record for the client's CAB.
- [ ] **CB134** — Cost telemetry: tokens per feature, chargeback, PTU utilisation, anomaly alerts.
- [ ] **CB135** — Define "resolved"/"success" for the agent and the offline + online measurement for it.
- [ ] **CB136** — Foundry Evaluations: built-in evaluators (groundedness, relevance, coherence, fluency, similarity, safety evaluators, agent evaluators: intent resolution, tool-call accuracy, task adherence), custom evaluators, local vs cloud evaluation runs, continuous evaluation on traces.
- [ ] **CB137** — Observability: OpenTelemetry GenAI semantic conventions, Azure Monitor / App Insights, Foundry tracing, span attributes for tokens and cost, evaluator scores attached to spans, alerting on drift in eval scores or cost per request.
- [ ] **CB138** — Release engineering: prompt and agent versioning, eval gates in GitHub Actions, canary by APIM traffic split, rollback of prompt/model/index independently, release manifest, change record for the client's CAB.
- [ ] **CB139** — Cost telemetry: tokens per feature, chargeback, PTU utilisation, anomaly alerts.
- [ ] **CB140** — Define "resolved"/"success" for the agent and the offline + online measurement for it.
- [ ] **CB151** — Non-functional budget to state unprompted: p95 latency per hop, tokens per request, cost per 1k requests, availability target, RPO/RTO for memory and audit stores, max blast radius of a prompt-injection event.
- [ ] **CB152** — Token economics per model, PTU arithmetic (PTU per TPM, reservation discounts, utilisation targets), prompt caching savings, semantic cache hit-rate, batch API discount, model routing policy, cost per 1k requests on A3, chargeback design, budget alerts.
- [ ] **CB158** — Traces + latency/error monitoring.

## Completion evidence

- [ ] Store the artifact path, reproducible command, observed outcome, limitations and next gap in the existing study log.
- [ ] Preserve current labs; link to shared concepts rather than importing another stage’s implementation.
- [ ] Do not label a sample, empty test collection or planned experiment as verified functionality.
