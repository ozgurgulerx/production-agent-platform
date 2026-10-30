# F05 capability builds — Agent generation, runtime and state

## Build contract

Status: **planned; functionality unverified**. Build one capability at a time using the existing module and labs. Record environment/dependency versions, permitted assistance, positive and negative results, and trace/test evidence. The learner writes code and tests; these contracts do not supply hidden implementations. Verify dated API and availability claims before execution.

### Prompt and hosted parity

- [ ] Build: Create explicit prompt-agent versions through Projects SDK, then package the same task in a hosted container using Agent Framework or LangGraph. Capture endpoint/context, tool behavior and deployment/version identity.
- [ ] Verify: Run the same input and one tool-failure case through both; record ownership of orchestration, scaling and session lifecycle without treating framework choice as a hosting service.

### Conversations, memory and persistence

- [ ] Build: Implement multi-turn state and compare platform history, memory stores and application-owned Cosmos/Postgres checkpoints. Select partition key/TTL from access patterns and handle concurrent writes with version/ETag checks.
- [ ] Verify: Demonstrate resume after interruption, expired state, concurrent update and cross-user isolation; show that memory deletion and audit retention have different policies.

### Framework and hosting choices

- [ ] Build: Rebuild a small handoff/workflow in Agent Framework and compare LangGraph and OpenAI Agents SDK. Inspect Foundry hosted vs Container Apps/AKS/Functions ownership and voice/realtime integration requirements.
- [ ] Verify: For self-hosted runtime prove authentication, controlled ingress/egress, readiness and durable state. Test failure recovery and explain what F06 durable execution must guarantee beyond a framework checkpoint.

### Routines, workflows and autonomy

- [ ] Build: Build one bounded trigger/routine and an explicit workflow/approval boundary; inspect autopilot support and lifecycle before enabling it. Version instructions and keep actions scoped.
- [ ] Verify: Demonstrate cancellation, duplicate trigger and unauthorized tool action. Record unsupported/retiring service surfaces rather than blindly following historical samples.

## Exact checklist targets

Each ID below is a distinct occurrence in the [full coverage matrix](../reference/production-build-coverage.md). Source wording is retained, including historical names and unfinished placeholders; it is not a fresh API guarantee. Compound items may require several small builds. Mark complete only after recording evidence.

- [ ] **CB051** — Azure OpenAI Realtime / gpt-realtime, Speech service, Azure Communication Services, Dynamics 365 Contact Centre, latency budgets.
- [ ] **CB052** — Create and target explicit agent versions.
- [ ] **CB053** — Implement conversation handling via the Responses API.
- [ ] **CB054** — Create agent via Projects SDK: model + instructions + tool
- [ ] **CB055** — Invoke agent and verify tool execution.
- [ ] **CB056** — Containerize LangGraph or Agent Framework agent. (main.py, azure.yaml, requirements.txt)
- [ ] **CB057** — Deploy via azd (azd ai agent extension) ; verify endpoint, tool execution, and managed scaling.
- [ ] **CB058** — set the standalone context - azd ai project set | azd ai project show
- [ ] **CB059** — azd ai connection | toolbox | skill | routine
- [ ] **CB067** — Agent memory
- [ ] **CB069** — Foundry Agent Service: hosted threads/runs, built-in tools (file search, AI Search, Bing grounding, Azure Functions, OpenAPI tools, MCP tools), connected agents, tracing, when it is enough and when it isn't (custom orchestration, non-Azure models, bring-your-own storage).
- [ ] **CB070** — Microsoft Agent Framework (AutoGen + Semantic Kernel successor, GA 1.0 April 2026): agents, workflows (graph-based), handoffs, middleware, context providers (memory), MCP and A2A support, hosting on Container Apps / AKS / Functions; why it replaced Semantic Kernel in your Priorities tab.
- [ ] **CB072** — LangGraph on Azure: when a client already runs it; checkpointing to Cosmos/Postgres; same reference architecture around it.
- [ ] **CB073** — A one-table trade-off you can draw: control, hosting, governance, skills needed, lock-in, cost, time-to-production.
- [ ] **CB074** — Agent Framework workflows, connected agents in Foundry, A2A agent cards, supervisor/worker vs handoff, when multi-agent is wrong; observability across agents.
- [ ] **CB077** — `FoundryChatClient` (and the Azure OpenAI / OpenAI chat clients), `ChatAgent` / agent creation with instructions and `tools=[python functions]` (how function schemas are derived from type hints and docstrings), `run` vs `run_stream`, threads and session state, middleware (logging, guardrail, approval), context providers (memory: Foundry memory store, mem0, Redis), workflows (graph of executors, edges, conditional routing, fan-out/fan-in, human-in-the-loop checkpoints), handoffs, MCP tool integration (`MCPStdioTool` / streamable HTTP tool), A2A hosting, OpenTelemetry setup, hosting as an ASGI app on Container Apps.
- [ ] **CB078** — Exercise: rebuild the OpenAI Agents SDK triage-and-handoff sample in Agent Framework with one MCP tool and a workflow checkpoint requiring approval; same tests; commit. This is the "Semantic Kernel/MAF working fluency" line in your Priorities tab.
- [ ] **CB079** — LangGraph on Azure — `langchain-openai` `AzureChatOpenAI`, `langchain-community` AzureSearch vector store, `langgraph` checkpointers (Cosmos / Postgres), running the same agent as in 4 for the "client already runs LangGraph" case.
- [ ] **CB080** — OpenAI Agents SDK against Azure — `OpenAIChatCompletionsModel` / Responses with an AzureOpenAI client, tracing export to App Insights; your by-heart SDK pointed at Azure endpoints.
- [ ] **CB096** — Agent Routines [link](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/routines)
- [ ] **CB097** — Workflows [link](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/workflow)
- [ ] **CB098** — Autopilots [link](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/autopilot-overview)
- [ ] **CB182** — Foundry Agent Service or Agent Framework host on Container Apps / AKS,
- [ ] **CB183** — Cosmos DB (sessions, memory, audit),
- [ ] **CB193** — Container Apps (jobs, scale to zero, Dapr, sidecars) vs AKS (when the client's platform team mandates it; Workload Identity, KEDA, ingress, Azure CNI, private cluster, GitOps/Flux) vs Functions / Durable Functions vs App Service; GPU needs (rare in this lane). Hays, Uniting People and Deloitte name AKS/Kubernetes.
- [ ] **CB215** — Containers, partition key design for sessions (`/session_id`) and audit (`/tenant_id`), TTL, change feed for async processing, vector search in Cosmos (DiskANN), point reads vs queries and RU cost, optimistic concurrency with ETag — the memory and audit store in the reference architecture.

## Completion evidence

- [ ] Store the artifact path, reproducible command, observed outcome, limitations and next gap in the existing study log.
- [ ] Preserve current labs; link to shared concepts rather than importing another stage’s implementation.
- [ ] Do not label a sample, empty test collection or planned experiment as verified functionality.
