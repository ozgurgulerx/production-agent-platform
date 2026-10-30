# Domain 2: Implement generative AI and agentic solutions (30–35%)

Largest domain. Objectives verbatim from the 16 Apr 2026 outline. Page dates are `ms.date` on 25 Oct 2026.

In repo: [F03 Creating agents](../../Agent-Build-02-Microsoft-Foundry/F05-Creating-Agents/README.md), [F04 Tooling](../../Agent-Build-02-Microsoft-Foundry/F06-Agent-Tooling-MCP-and-Integration/README.md), [F05 Evals](../../Agent-Build-02-Microsoft-Foundry/F08-Evals-Tracing-and-Release/README.md), [Foundry agents reading map](../../Agent-Build-02-Microsoft-Foundry/reference/reading-map-foundry-agents-2026-10-25.md), [S03](../../Agent-Build-01-Fundamentals/S03-AI-Agents-Tools-and-MCP/), [S04](../../Agent-Build-01-Fundamentals/S04-Agentic-Workflows-and-Harnesses/).

## 2.1 Build generative applications by using Foundry

- [ ] Deploy and consume LLMs, small models, code models, and multimodal models
  - Know how to: deploy from the catalog, call via the OpenAI v1 Responses API and the Foundry SDK, send image/audio inputs, pick a Phi or Codex-class model for the task.
  - Read: Responses API https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses (2026-08-18) · Vision-enabled chat models https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/gpt-with-vision (2026-07-29) · Foundry SDK overview https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview · Deployment types https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types
- [ ] Implement retrieval-augmented generation (RAG) in an application
  - Know how to: chunk, embed, index with integrated vectorization, query hybrid + semantic ranker, cite; or use the AI Search tool / Foundry IQ knowledge base from an agent.
  - Read: RAG in Foundry https://learn.microsoft.com/en-us/azure/foundry/concepts/retrieval-augmented-generation (2026-08-21) · RAG and generative AI in AI Search https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview (2026-08-04) · AI Search tool for agents https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/ai-search (2026-10-08) · Create a knowledge base https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base (2026-08-12) · In repo: F08.
- [ ] Design workflows, tool-augmented flows, and multistep reasoning pipelines
  - Know how to: Agent Framework `WorkflowBuilder` (sequential, concurrent, handoff, group chat, Magentic), checkpoints, `.as_agent()` hosted; why Foundry declarative workflows retire 1 Dec 2026.
  - Read: Agent Framework overview https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview (2026-07-29) · Workflow concepts https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/ · Workflow capabilities (HITL, checkpoints) https://learn.microsoft.com/en-us/agent-framework/workflows/ · Foundry workflows (preview, retiring) https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/workflow (2026-07-31) · In repo: S04.
- [ ] Evaluate models and apps, including detecting fabrications, relevance, quality, and safety
  - Know how to: build a dataset, run built-in evaluators via the SDK and portal, compare runs, LLM-as-judge rubric generation, groundedness vs Groundedness Pro.
  - Read: Built-in evaluators https://learn.microsoft.com/en-us/azure/foundry/concepts/built-in-evaluators (2026-09-09) · Evaluate agents https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/evaluate-agent (2026-10-01) · Observability concept https://learn.microsoft.com/en-us/azure/foundry/concepts/observability · In repo: F05.
- [ ] Integrate generative workflows into applications by using Foundry SDKs and connectors
  - Know how to: `AIProjectClient`, `project.get_openai_client()`, connections (`azd ai connection create`), Logic Apps and Power Platform connectors, Semantic Kernel / Agent Framework `FoundryChatClient`.
  - Read: SDK overview https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview (2026-10-06) · Responses API quickstart (ephemeral agent) https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/responses-api (2026-07-07) · Foundry samples https://github.com/microsoft-foundry/foundry-samples · In repo: F02.
- [ ] Configure an application to connect to a Foundry project
  - Know how to: project endpoint vs account endpoint, token scope `https://ai.azure.com/.default`, `DefaultAzureCredential`, env vars (`FOUNDRY_PROJECT_ENDPOINT`), connection strings in `azure.yaml`.
  - Read: Prompt agent quickstart https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/prompt-agent (2026-09-09) · RBAC roles needed https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry

## 2.2 Build agents by using Foundry

- [ ] Define agent roles, goals, conversation-tracking approach, and tool schemas
  - Know how to: `PromptAgentDefinition(model, instructions, tools)`, conversations vs `previous_response_id`, JSON-schema tool definitions, agent versions immutable (`name:version`).
  - Read: Agent Service overview https://learn.microsoft.com/en-us/azure/foundry/agents/overview (2026-09-25) · Development lifecycle https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/development-lifecycle · Runtime components https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/runtime-components · Function calling https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/function-calling (2026-04-30) · In repo: F03.
- [ ] Build agents that integrate retrieval, function-calling, and conversation memory
  - Know how to: file search + AI Search tool + function tool on one agent, memory store (preview) with embedding deployment, conversation retention.
  - Read: File search https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/file-search (2026-09-30) · What is memory https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-memory · Memory usage https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/memory-usage · Cosmos DB memory devblog https://devblogs.microsoft.com/cosmosdb/powering-memory-in-foundry-agent-service-with-azure-cosmos-db
- [ ] Integrate agent tools, including APIs, knowledge stores, search, content understanding, and custom functions
  - Know how to: toolbox vs inline tools, MCP (auth modes: key, agent identity, project MI, user delegation, OAuth passthrough), OpenAPI tool, code interpreter, web/Bing search, SharePoint (preview), Fabric data agent (preview); tool search (GA) and skills (preview).
  - Read: Toolbox overview https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/toolbox-overview (2026-07-28) · MCP tool https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol (2026-09-29) · MCP authentication https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication · OpenAPI tool https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/openapi · Migrate tool availability table https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/migrate · In repo: F04, S03 reading map.
- [ ] Implement orchestrated multi-agent solutions
  - Know how to: A2A tool (`a2a` GA v1.0, `a2a_preview` 0.3) and its six auth methods; Agent Framework orchestrations hosted as one hosted agent; Connected Agents tool is not available in the new service.
  - Read: A2A tool https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/agent-to-agent (2026-10-04) · A2A authentication https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/agent-to-agent-authentication · Host Agent Framework agents https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/framework-hosted-agents · In repo: F03 section D, S04.
- [ ] Build autonomous or semiautonomous workflows with safeguards and approval flow controls
  - Know how to: tool `approval_mode`, Agent Framework `RequestInfoExecutor` / `ctx.request_info()`, checkpoint and resume, Routines (GA Sep 2026) for scheduled/triggered runs, long-running hosted agents (preview).
  - Read: Workflow capabilities https://learn.microsoft.com/en-us/agent-framework/workflows/ · Agent Framework checkpoints https://learn.microsoft.com/en-us/agent-framework/workflows/ · Agent Service what's new (routines, long-running) https://learn.microsoft.com/en-us/azure/foundry/whats-new-foundry · In repo: S04.09 Harness Engineering.
- [ ] Integrate monitoring into deployed agents, evaluate agent behavior, and perform error analysis
  - Know how to: App Insights connection injected into hosted agents, trace tool spans, continuous evaluation on live traffic, agent evaluators (intent resolution, task adherence, tool call accuracy), error analysis in the portal, agent optimizer (preview).
  - Read: Trace agent setup https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/trace-agent-setup (2026-07-31) · Agent evaluators https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/agent-evaluators · Agent optimizer https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/agent-optimizer-overview (2026-08-07) · Monitor agents dashboard https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/how-to-monitor-agents-dashboard · In repo: F05.

## 2.3 Optimize and operationalize generative AI systems

- [ ] Tune generation behavior, such as prompt engineering and adjusting model parameters
  - Know how to: system vs developer messages, few-shot, temperature/top_p/max tokens, reasoning effort and verbosity on GPT-5.x, structured outputs (JSON schema), prompt caching.
  - Read: Prompt engineering techniques https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering (2026-05-13) · Reasoning models https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning (2026-09-21) · Structured outputs https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs (2026-08-24) · Prompt caching https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching
- [ ] Implement model reflection, chain-of-thought evaluations, and self-critique loops
  - Know how to: reflection/critic pattern in Agent Framework workflows, evaluator-in-the-loop, reasoning summaries from the Responses API, rubric-based LLM judges.
  - Read: Agent Framework orchestrations https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/ · Responses API reasoning items https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses · Evaluate agents (rubric generation) https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/evaluate-agent · In repo: S04.
- [ ] Set up observability by implementing tracing, token analytics, safety signals, and latency breakdowns
  - Know how to: OpenTelemetry + App Insights, token usage per span, content-filter results in logs, Azure Monitor workbooks, APIM `llm-emit-token-metric`.
  - Read: Observability concept https://learn.microsoft.com/en-us/azure/foundry/concepts/observability (2026-10-15) · Tracing concept https://learn.microsoft.com/en-us/azure/foundry/observability/concepts/trace-agent-concept · APIM AI gateway https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities · In repo: F09.
- [ ] Orchestrate multiple models, flows, or hybrid LLM and rules engines
  - Know how to: model router deployment and routing modes, model cascading (small first), rules/validators around LLM calls, Logic Apps or Durable Functions for deterministic steps.
  - Read: Model router https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/model-router · Model router how it works https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-router-how-it-works · Evals for model router (devblog, May 2026) https://devblogs.microsoft.com/foundry/how-to-run-evals-for-model-router/
