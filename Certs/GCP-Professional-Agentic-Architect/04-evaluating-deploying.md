# Section 4: Evaluating and deploying agentic workflows (~22%)

Objectives verbatim from the exam guide PDF (Sep 2026).

## 4.1 Evaluating agents in development and in production

- [ ] Creating test sets for agent evaluation (e.g., golden data, prompts, and edge cases)
- [ ] Creating continuous evaluation pipelines to assess an agent's tool execution based on established success criteria
- [ ] Determining the appropriate evaluation framework and tooling (e.g., ADK evaluation tooling (evalset), Agent Platform Gen AI evaluation service, and custom autoraters)
- [ ] Evaluating an agentic system against a golden dataset to assess agent response and retrieval quality (e.g., using ADK)
  - Know how to: ADK `.evalset.json` and `adk eval` (trajectory and response-match metrics), Gen AI evaluation service agent metrics (tool use, trajectory exact/in-order/any-order match, final response), custom pointwise/pairwise autoraters, running evals in Cloud Build or Agent Runtime; RAG retrieval metrics.
  - Read: ADK evaluation https://google.github.io/adk-docs/evaluate/ · Gen AI evaluation service overview https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview · Evaluate agents https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents · Define your metrics (custom autoraters) https://cloud.google.com/vertex-ai/generative-ai/docs/models/determine-eval · In repo: F05 (Azure equivalent), S04.

## 4.2 Deploying and scaling production workloads

- [ ] Selecting optimal deployment runtime based on the use case, requirements, and cost (e.g., Agent Runtime, Cloud Run, and GKE)
- [ ] Troubleshooting agent issues (e.g., drift, tool invocation latency, agent reasoning loops, and system failures)
- [ ] Monitoring and optimizing agents for performance, reliability, and cost (e.g., identify logic errors, latency bottlenecks, and hallucinations)
  - Know how to: `adk deploy agent_engine|cloud_run|gke`, Agent Runtime managed sessions/memory/scaling vs Cloud Run (container, concurrency, min instances) vs GKE (GPU, Agent Sandbox); Cloud Trace spans from ADK (OpenTelemetry), Cloud Logging, Cloud Monitoring dashboards, Agent Runtime observability; token/cost controls, Gemini context caching, loop guards (max iterations in LoopAgent).
  - Read: ADK deploy https://google.github.io/adk-docs/deploy/ · Deploy to Agent Runtime https://cloud.google.com/agent-platform/docs/agent-engine/deploy · Cloud Run for agents https://cloud.google.com/run/docs/ai-agents · Agent Runtime monitoring https://cloud.google.com/agent-platform/docs/agent-engine/monitoring · Tracing in Agent Runtime https://cloud.google.com/agent-platform/docs/agent-engine/tracing · Cloud Trace https://cloud.google.com/trace/docs · Context caching https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview
