# F09 capability builds — AI gateway and routing controls

## Build contract

Status: **planned; functionality unverified**. Build one capability at a time using the existing module and labs. Record environment/dependency versions, permitted assistance, positive and negative results, and trace/test evidence. The learner writes code and tests; these contracts do not supply hidden implementations. Verify dated API and availability claims before execution.

### Identity and quota gateway

- [ ] Build: Author APIM policies for Entra validation, managed-identity backend access, token limits, consumer quotas and redacted telemetry. Compare OpenAI-specific and llm policies for supported providers.
- [ ] Verify: Demonstrate invalid token denial, missing permission, quota/429 and successful allowed call; validate metrics carry consumer/deployment identity without private payloads.

### Routing, fallback and caching

- [ ] Build: Compare Foundry model-router selection with explicit APIM backend pools, priorities/weights and circuit breaker. Configure a bounded fallback or provisioned spillover experiment only when supported; isolate semantic cache by tenant/permissions.
- [ ] Verify: Cause backend failure and verify actual model/backend, request semantics, cost and tool/conversation compatibility. Test that another user cannot receive cached protected content.

### Production gateway evidence

- [ ] Build: Load-test within agreed limits and capture token/latency/error metrics. Connect gateway controls to F08 release/cost evidence and F02 private connectivity.
- [ ] Verify: Show limits and circuit recovery under a reproducible workload; distinguish fallback success from quality equivalence.

## Exact checklist targets

Each ID below is a distinct occurrence in the [full coverage matrix](../reference/production-build-coverage.md). Source wording is retained, including historical names and unfinished placeholders; it is not a fresh API guarantee. Compound items may require several small builds. Mark complete only after recording evidence.

- [ ] **CB027** — provisioned spill-over
- [ ] **CB036** — Model router in Foundry, small-model-first with escalation, Phi / Mistral / Llama serverless, evaluation-driven routing, latency and cost tables.
- [ ] **CB063** — Foundry model router deployment - default behavior vs custom model subset to choose from
- [ ] **CB066** — Rate limiting and quotas
- [ ] **CB197** — `azure-openai-token-limit`, `azure-openai-emit-token-metric`, `azure-openai-semantic-cache-lookup/store`, `llm-*` equivalents for non-OpenAI models, backend pools with priority/weight and circuit breaker, `authentication-managed-identity`, `validate-jwt` / `validate-azure-ad-token`, rate-limit-by-key, `set-backend-service` for model routing, logging to Event Hub; APIM for MCP servers.
- [ ] **CB198** — Exercise: write the policy for token limits per subscription + managed-identity auth + fallback to a second deployment; test with a load script and read the metrics.

## Completion evidence

- [ ] Store the artifact path, reproducible command, observed outcome, limitations and next gap in the existing study log.
- [ ] Preserve current labs; link to shared concepts rather than importing another stage’s implementation.
- [ ] Do not label a sample, empty test collection or planned experiment as verified functionality.
