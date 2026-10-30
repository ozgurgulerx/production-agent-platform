# Foundry and Azure production build checklist

Merged 30 October 2026. Implement each capability as a small build, then combine it into the production reference agent. The documentation-derived checklist is **Source A**; the job-description-derived architecture/code list is **Source B**. The repeated paste of Source A is included once. Overlapping source items remain visible rather than being silently discarded.

Source B: [Azure architect mastery and code list](/Users/ozgurguler/Downloads/azure-architect-mastery-and-code-2026-10-30.md). Sources are unchanged. Original architecture IDs 1–27, code IDs C1–C28, evidence tags, exercises, priorities, and planning material are retained. Source claims and version details are not newly fact-checked in this merge.

## Build evidence for each capability

- [ ] Write the implementation yourself; record the code path and dependency versions.
- [ ] Demonstrate the successful flow and a relevant failure/denied-access flow.
- [ ] Capture a reproducible command, trace/test result, and relevant measured latency/cost/quality.
- [ ] Explain the identity, network, data, safety, and rollback boundaries relevant to that build.
- [ ] Mark complete only with evidence; repo files and sample code do not establish proficiency or successful deployment.

For architecture/regulatory topics, produce and defend the design/evidence artifact as well as any applicable control implementation. These are build contracts, not supplied solutions. The user owns the code and tests.

## Contents

- [Infrastructure as code and repeatable provisioning](#infrastructure-as-code-and-repeatable-provisioning)
- [Foundry Setup and developer surfaces](#foundry-setup-and-developer-surfaces)
- [Models, deployment tiers, routing, and fine-tuning](#models-deployment-tiers-routing-and-fine-tuning)
- [Model APIs and inference](#model-apis-and-inference)
- [Agent Generation and runtime choices](#agent-generation-and-runtime-choices)
- [MCP Tooling and integration](#mcp-tooling-and-integration)
- [Agent Security, identity, and governance](#agent-security-identity-and-governance)
- [EVALS](#evals)
- [OBSERVABILITY](#observability)
- [Release engineering and LLMOps](#release-engineering-and-llmops)
- [TRUST & SAFETY](#trust--safety)
- [OPTIMIZATION and COST](#optimization-and-cost)
- [Enterprise production capabilities and Well-Architected design](#enterprise-production-capabilities-and-well-architected-design)
- [Azure deployment, networking, compute, and messaging](#azure-deployment-networking-compute-and-messaging)
- [APIM AI gateway](#apim-ai-gateway)
- [AI SEARCH and enterprise RAG](#ai-search-and-enterprise-rag)
- [Data stores and grounding platforms](#data-stores-and-grounding-platforms)
- [Microsoft 365, Copilot Studio, and Graph](#microsoft-365-copilot-studio-and-graph)
- [Certification and Azure fundamentals](#certification-and-azure-fundamentals)

## GIT

Source A retains Git as a study topic; implementation and release tasks also appear under C8 and the release section.

## TERRAFORM AND INFRASTRUCTURE AS CODE

Source A retains Terraform as a study priority. Source B's C17 says Bicep hands-on and Terraform awareness only. Both are preserved; the current user intention is to build capabilities, not silently drop Terraform. Decide the implementation depth when starting that block.

### Infrastructure as code and repeatable provisioning

#### C17. Infrastructure as code: Bicep (and Terraform awareness only)

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 2 — write with docs open, understand every line.*

- [ ] Bicep for the reference architecture: Foundry resource and project, model deployments, AI Search, Storage, Key Vault, Cosmos, Container Apps environment and app with managed identity, role assignments (`Microsoft.Authorization/roleAssignments` with role definition ids), private endpoints and private DNS zones, APIM with policies, Log Analytics and App Insights, Azure Policy assignments; `az deployment group what-if`; parameter files per environment. Terraform (azurerm / azapi) is off the study plan but you must read it, since many clients mandate it (Uniting People, Full Stack Engineer ads).
- [ ] Exercise: deploy A3's infrastructure from Bicep with no portal clicks; destroy and redeploy.

## FOUNDRY

### Foundry Setup and developer surfaces

#### Documentation checklist — Foundry Setup

- [ ] Configure project endpoint, model deployment, and connection IDs via .env.
- [ ] Confirm region, model, tool, and preview support.

#### Documentation checklist — OTHERS

- [ ] Foundry Canvas
- [ ] Foundry Toolkit for VSC
- [ ] Foundry Skill for CC / Github Copilot
- [ ] plan and manage costs [link](https://learn.microsoft.com/en-us/azure/foundry/concepts/manage-costs)

#### C19. Azure CLI and `az ai`/`az cognitiveservices`/`az search`/`az containerapp`

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 2 — write with docs open, understand every line.*

- [ ] Create and inspect every resource above from the CLI; role assignment commands; `az containerapp up`, revisions and traffic splitting for canaries; `az monitor` queries. Interviewers watch for CLI fluency as a proxy for having done it.

#### C27. C# / .NET awareness — `Azure.AI.Projects`, `Microsoft.Agents.AI.Foundry`, `Azure.AI.OpenAI`; read a .NET agent sample and map it to the Python one. Hays AI Developer names C#.

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 3 — read fluently, build once.*

- [ ] C# / .NET awareness — `Azure.AI.Projects`, `Microsoft.Agents.AI.Foundry`, `Azure.AI.OpenAI`; read a .NET agent sample and map it to the Python one. Hays AI Developer names C#.

### Models, deployment tiers, routing, and fine-tuning

#### Documentation checklist — Models

- [ ] Standard pay-per-token
- [ ] Provisioned Throughput -
- [ ] Managed Compute - OS models on dedicated GPU capacity wo building an inference stack
  - [ ] Deploy with managed compute [link](https://learn.microsoft.com/en-us/azure/foundry/how-to/deploy-models-managed?tabs=openai-entra&pivots=ai-foundry-portal)
- [ ] Serving fine-tuned LoRA adapters (preview) [link](https://learn.microsoft.com/en-us/azure/foundry/concepts/managed-compute-overview)
  - [ ] Adapter deployment overview [link](https://learn.microsoft.com/en-us/azure/foundry/concepts/adapter-deployment-overview)
  - [ ] ==Depoy fine-tuned LoRA adapters== [link](https://learn.microsoft.com/en-us/azure/foundry/how-to/deploy-lora-managed-compute) - how are they fine-tuned?
- [ ] Deploy using code [link](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/create-model-deployments?pivots=programming-language-cli)
- [ ] Deployment types
  - [ ] flex processing
  - [ ] priority processing
  - [ ] provisioned spill-over
- [ ] fine-tuning [fine-tuning](https://learn.microsoft.com/en-us/azure/foundry/fine-tuning/overview)
  - [ ] …

#### 4. Azure OpenAI and Foundry model layer — the platform facts [ADS][MKT]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 1 — must be at 3 before any screen (the whiteboard set).*

- [ ] Foundry resource vs project vs hub (classic vs new Foundry); project endpoint shape; model catalogue (OpenAI, Anthropic Claude in Foundry, Mistral, Llama, Phi, DeepSeek), serverless vs managed compute deployments, Models-as-a-Service billing.
- [ ] Deployment types: Standard, Global Standard, Data Zone (EU/US), Provisioned (PTU), Global Batch; data residency implications of each — the FS client question.
- [ ] Quotas and limits: TPM/RPM per deployment, quota per region, how to request more, how APIM smooths it.
- [ ] Responses API vs Chat Completions; structured outputs; function/tool calling; prompt caching; reasoning models and their cost/latency profile; fine-tuning options and when not to.
- [ ] Content filtering: default severity levels, custom filters, prompt shields (jailbreak, indirect injection), groundedness detection, protected-material detection, asynchronous filter mode, modified-content-filter approval for regulated use.
- [ ] Data handling: no training on customer data, abuse monitoring and the opt-out process, logging retention — the DPO question.

#### 20. Model routing and open-weight on Azure

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 3 — differentiators the stronger ads name.*

- [ ] Model router in Foundry, small-model-first with escalation, Phi / Mistral / Llama serverless, evaluation-driven routing, latency and cost tables.

#### 23. Fine-tuning and distillation on Azure (decision-level)

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 3 — differentiators the stronger ads name.*

- [ ] When SFT beats prompting, Foundry fine-tuning options, cost, eval before/after, distillation workflow.

#### C25. Anthropic SDK against Foundry — `anthropic` client with `base_url` at the Foundry `/anthropic` endpoint and Entra token; tool use and MCP connector; for clients choosing Claude in Foundry.

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 3 — read fluently, build once.*

- [ ] Anthropic SDK against Foundry — `anthropic` client with `base_url` at the Foundry `/anthropic` endpoint and Entra token; tool use and MCP connector; for clients choosing Claude in Foundry.

### Model APIs and inference

#### Documentation checklist — Model API’s

- [ ] Responses API [link](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses?tabs=python)
  - [ ] ….all the tools under it — [source link unfinished; resolve before build]
  - [ ] websockets mode
  - [ ] tool search
  - [ ] deep research
  - [ ] ==multi-agent orchestration== [link](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses-multi-agent)
  - [ ] predicted outputs
  - [ ] prompt caching
- [ ] Decisions API [link](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/decisions?tabs=python)
- [ ] Webhooks [webhooks](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/webhooks?tabs=python-key)

#### C2. OpenAI SDK against Azure: `openai` (AzureOpenAI / AsyncAzureOpenAI) and Responses API

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 1 — write from memory, no AI, under the clock.*

- [ ] Client construction with `azure_endpoint`, `api_version`, `azure_ad_token_provider`; deployments vs model names; Responses API (`client.responses.create`, `previous_response_id`, tools, `text.format` for structured outputs) and Chat Completions legacy; streaming (`stream=True`, event types), tool calling loop (tool_calls → execute → return tool results → loop with max iterations), structured outputs with Pydantic (`client.beta.chat.completions.parse` / Responses `text_format`), prompt caching behaviour, `usage` accounting for cost, timeouts and `max_retries`, handling content-filter errors (`content_filter` finish reason, 400 with `content_filter_result`), batch API, embeddings.
- [ ] Exercise (your standing 45-minute drill): tool-calling loop with two tools, typed with Pydantic, structured final output, retries, token/cost tally, tests mocking the client. Then the same with streaming.

#### 22. Voice and real-time (awareness)

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 3 — differentiators the stronger ads name.*

- [ ] Azure OpenAI Realtime / gpt-realtime, Speech service, Azure Communication Services, Dynamics 365 Contact Centre, latency budgets.

### Agent Generation and runtime choices

#### Documentation checklist — Agent Generation

- [ ] Create and target explicit agent versions.
- [ ] Implement conversation handling via the Responses API.

**Path 1 — Foundry Agent Service: prompt agent**
- [ ] Create agent via Projects SDK: model + instructions + tool
- [ ] Invoke agent and verify tool execution.

**Path 2 — Foundry Agent Service: hosted agent -**
Foundry handles infrastructure, scaling, and session management.
- [ ] Containerize LangGraph or Agent Framework agent. (main.py, azure.yaml, requirements.txt)
- [ ] Deploy via azd (azd ai agent extension) ; verify endpoint, tool execution, and managed scaling.
  - [ ] set the standalone context - azd ai project set | azd ai project show
  - [ ] azd ai connection | toolbox | skill | routine
  - [ ] azd ai agent eval with eval.yaml and optimizer workflow (azd ai agent optimize, trace | dataset sources and CI quality gates)
  - [ ] azd ai agent publish, and publish through Microsoft 365

- [ ] Foundry Model Endpoints - keyless authantication with Microsoft Entra ID...~[link](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/endpoints?tabs=python)~
- [ ] Foundry model router deployment - default behavior vs custom model subset to choose from
  - [ ] RBAC integration - who can call which model deployments
  - [ ] Data residency requirements
  - [ ] Rate limiting and quotas

#### Documentation checklist — Agent Capabilities

- [ ] Agent memory
- [ ] Foundry IQ

#### 5. Agent platform choice on Azure: Foundry Agent Service vs Agent Framework vs Copilot Studio vs LangGraph [ADS][COG]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 1 — must be at 3 before any screen (the whiteboard set).*

- [ ] Foundry Agent Service: hosted threads/runs, built-in tools (file search, AI Search, Bing grounding, Azure Functions, OpenAPI tools, MCP tools), connected agents, tracing, when it is enough and when it isn't (custom orchestration, non-Azure models, bring-your-own storage).
- [ ] Microsoft Agent Framework (AutoGen + Semantic Kernel successor, GA 1.0 April 2026): agents, workflows (graph-based), handoffs, middleware, context providers (memory), MCP and A2A support, hosting on Container Apps / AKS / Functions; why it replaced Semantic Kernel in your Priorities tab.
- [ ] Copilot Studio: low-code agents, grounding on SharePoint/Dataverse/AI Search, topics, generative orchestration, Power Platform connectors, governance via Power Platform admin centre and DLP, when to escalate to a pro-code Foundry agent, how the two interoperate (Copilot Studio calling Foundry agents / MCP, Foundry agents published to M365 Copilot). Two of the three £800 ads require it.
- [ ] LangGraph on Azure: when a client already runs it; checkpointing to Cosmos/Postgres; same reference architecture around it.
- [ ] A one-table trade-off you can draw: control, hosting, governance, skills needed, lock-in, cost, time-to-production.

#### 19. A2A and multi-agent topology

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 3 — differentiators the stronger ads name.*

- [ ] Agent Framework workflows, connected agents in Foundry, A2A agent cards, supervisor/worker vs handoff, when multi-agent is wrong; observability across agents.

#### C3. Foundry SDK: `azure-ai-projects` (>=2.0)

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 1 — write from memory, no AI, under the clock.*

- [ ] `AIProjectClient(endpoint, credential)` with the project endpoint `https://<resource>.services.ai.azure.com/api/projects/<project>`; getting an OpenAI-compatible client from the project (`project_client.get_openai_client()` style accessor — check the 2.x name), connections (AI Search, Storage, Key Vault connections and how a tool resolves them), deployments listing, datasets and indexes, evaluations (create run, built-in evaluator ids, read results), agents: create agent with instructions and tools, threads/conversations, runs, polling vs streaming, run steps and tool call inspection, file search / AI Search / OpenAPI / Azure Function / MCP / Bing grounding tool definitions, connected agents, tracing enablement.
- [ ] Exercise: create an agent with an AI Search tool and an OpenAPI tool, run a thread, print each tool call and its result, attach an evaluation run on the transcript, tear down. Know which parts are preview.

#### C4. Microsoft Agent Framework: `agent-framework`

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 1 — write from memory, no AI, under the clock.*

- [ ] `FoundryChatClient` (and the Azure OpenAI / OpenAI chat clients), `ChatAgent` / agent creation with instructions and `tools=[python functions]` (how function schemas are derived from type hints and docstrings), `run` vs `run_stream`, threads and session state, middleware (logging, guardrail, approval), context providers (memory: Foundry memory store, mem0, Redis), workflows (graph of executors, edges, conditional routing, fan-out/fan-in, human-in-the-loop checkpoints), handoffs, MCP tool integration (`MCPStdioTool` / streamable HTTP tool), A2A hosting, OpenTelemetry setup, hosting as an ASGI app on Container Apps.
- [ ] Exercise: rebuild the OpenAI Agents SDK triage-and-handoff sample in Agent Framework with one MCP tool and a workflow checkpoint requiring approval; same tests; commit. This is the "Semantic Kernel/MAF working fluency" line in your Priorities tab.

#### C20. LangGraph on Azure — `langchain-openai` `AzureChatOpenAI`, `langchain-community` AzureSearch vector store, `langgraph` checkpointers (Cosmos / Postgres), running the same agent as in 4 for the "client already runs LangGraph" case.

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 3 — read fluently, build once.*

- [ ] LangGraph on Azure — `langchain-openai` `AzureChatOpenAI`, `langchain-community` AzureSearch vector store, `langgraph` checkpointers (Cosmos / Postgres), running the same agent as in 4 for the "client already runs LangGraph" case.

#### C21. OpenAI Agents SDK against Azure — `OpenAIChatCompletionsModel` / Responses with an AzureOpenAI client, tracing export to App Insights; your by-heart SDK pointed at Azure endpoints.

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 3 — read fluently, build once.*

- [ ] OpenAI Agents SDK against Azure — `OpenAIChatCompletionsModel` / Responses with an AzureOpenAI client, tracing export to App Insights; your by-heart SDK pointed at Azure endpoints.

#### C28. Local and edge — Foundry Local (ONNX / small models on device), when a client raises on-prem or offline; awareness only.

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 3 — read fluently, build once.*

---

### MCP Tooling and integration

#### Documentation checklist — MCP Tooling

- [ ] Foundry Toolbox - Microsoft's managed way to assemble an MCP tool server [link](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/toolbox-overview)
- [ ] Foundry MCP Server - agents to use Foundry services
- [ ] Connect an external MCP server, e.g. Microsoft Learn.
- [ ] Configure MCP tool approvals; handle approval requests.
- [ ] Handle unavailable optional MCP tools with explicit degraded behavior.
- [ ] Validate MCP tool safety controls beyond model content filters.

#### 18. MCP on Azure

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 3 — differentiators the stronger ads name.*

- [ ] Hosting MCP servers (Container Apps, Functions remote MCP), API Center as MCP registry, APIM in front of MCP (auth, rate limit), Foundry Agent Service MCP tool, Copilot Studio MCP connectors; auth per S27; tool design quality (S03.04).

#### C16. MCP on Azure: `mcp` Python SDK + hosting

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 2 — write with docs open, understand every line.*

- [ ] `FastMCP` server with tools/resources/prompts, streamable HTTP transport, OAuth 2.1 with Entra as authorisation server (protected resource metadata, audience/scope validation, no passthrough), hosting on Container Apps or Functions remote MCP, registering in API Center, fronting with APIM; MCP client from Agent Framework and Foundry Agent Service. Carries your S03.03 / S27 work.

#### C26. Azure Functions remote MCP and Logic Apps agent loops — awareness of the no-code/low-code agent surfaces clients will ask about.

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 3 — read fluently, build once.*

- [ ] Azure Functions remote MCP and Logic Apps agent loops — awareness of the no-code/low-code agent surfaces clients will ask about.

### Agent Security, identity, and governance

#### Documentation checklist — ==🟡Agent Security & Governance==

- [ ] Entra ID
  - [ ] user identity
  - [ ] app registrations
  - [ ] managed identities
  - [ ] agent identity
- [ ] Microsoft Agent 365 Integration with Foundry [link](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/agent-365-integration)
- [ ] Agent Routines [link](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/routines)
- [ ] Workflows [link](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/workflow)
- [ ] Autopilots [link](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/autopilot-overview)
- [ ] publish & share [link](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/publish-copilot?tabs=portal)
  - [ ] publish with a virtual network
- [ ] Agent identity and access [link](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/identity-access-overview)
  - [ ] Azure RBAC permission bundles for Microsoft Foundry -
    - [ ] Foundry User, Foundry Owner, Foundry Account Owner, and Foundry Project Manager
- [ ] content filters
  - [ ] Content Safety (prompt shields, groundedness, protected material)
- [ ] OIDC vs OAuth 2.0 vs SAML in one line each; when SAML still appears (legacy enterprise SSO, federation), why OIDC for apps and agents.
- [ ] Entra ID: app registrations, service principals, managed identities (system vs user-assigned), workload identity federation (GitHub Actions → Azure without secrets), on-behalf-of flow, client credentials, PKCE for public clients, token audiences and scopes, Conditional Access, Privileged Identity Management.
- [ ] Agent identity design: the agent has its own identity; tools are called with the user's delegated token (OBO) or the agent's identity with scoped RBAC; per-call authorisation; consent and admin consent for tool scopes; token lifetime and revocation; Entra Agent ID concepts.
- [ ] MCP server auth on Azure: Entra as authorisation server, protected-resource metadata, scopes per tool, audience validation, no token passthrough (ties to S03.03 / S27).
- [ ] Zero Trust planes: identity (strong auth, CA), device (compliance), network (private endpoints, no public ingress, NSG/ASG, Azure Firewall egress allow-list), application (APIM policies, WAF on Front Door / App Gateway), data (classification, Purview, CMK, RBAC on indexes), visibility (Sentinel, Defender).
- [ ] RBAC on data planes: Azure OpenAI roles, AI Search roles, Storage data roles, Key Vault RBAC vs access policies; security-trimmed retrieval (filter on group claims / ACLs in the index).

Observability [link](https://learn.microsoft.com/en-us/azure/foundry/concepts/observability)

#### 3. Identity, authorisation and Zero Trust for agents [COG][ADS]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 1 — must be at 3 before any screen (the whiteboard set).*

- [ ] OIDC vs OAuth 2.0 vs SAML in one line each; when SAML still appears (legacy enterprise SSO, federation), why OIDC for apps and agents.
- [ ] Entra ID: app registrations, service principals, managed identities (system vs user-assigned), workload identity federation (GitHub Actions → Azure without secrets), on-behalf-of flow, client credentials, PKCE for public clients, token audiences and scopes, Conditional Access, Privileged Identity Management.
- [ ] Agent identity design: the agent has its own identity; tools are called with the user's delegated token (OBO) or the agent's identity with scoped RBAC; per-call authorisation; consent and admin consent for tool scopes; token lifetime and revocation; Entra Agent ID concepts.
- [ ] MCP server auth on Azure: Entra as authorisation server, protected-resource metadata, scopes per tool, audience validation, no token passthrough (ties to S03.03 / S27).
- [ ] Zero Trust planes: identity (strong auth, CA), device (compliance), network (private endpoints, no public ingress, NSG/ASG, Azure Firewall egress allow-list), application (APIM policies, WAF on Front Door / App Gateway), data (classification, Purview, CMK, RBAC on indexes), visibility (Sentinel, Defender).
- [ ] RBAC on data planes: Azure OpenAI roles, AI Search roles, Storage data roles, Key Vault RBAC vs access policies; security-trimmed retrieval (filter on group claims / ACLs in the index).

#### C1. Identity: `azure-identity`

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 1 — write from memory, no AI, under the clock.*

- [ ] `DefaultAzureCredential`, `ManagedIdentityCredential` (system and user-assigned, client_id), `AzureCliCredential`, `ClientSecretCredential` only for tests, `OnBehalfOfCredential`, `WorkloadIdentityCredential` for AKS and GitHub Actions federation; `get_token(scope)` and the scope strings you must know: `https://cognitiveservices.azure.com/.default`, `https://search.azure.com/.default`, `https://ai.azure.com/.default`, `https://graph.microsoft.com/.default`, `https://vault.azure.net/.default`.
- [ ] `get_bearer_token_provider(credential, scope)` to feed the OpenAI client without keys.
- [ ] Exercise: an httpx client that calls Azure OpenAI with a managed identity token, refreshes it, retries 429/5xx with jitter, and never logs the token. 25 minutes, tests with a fake token provider.

#### C11. Key Vault and configuration: `azure-keyvault-secrets`, `azure-appconfiguration`

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 2 — write with docs open, understand every line.*

- [ ] `SecretClient`, caching secrets at startup, rotation handling, Key Vault references in Container Apps / App Service, App Configuration feature flags for prompt/model toggles.

### EVALS

#### Documentation checklist — EVALS

- [ ] Maintain a repeatable dataset: internal, external, and combined-source questions.
- [ ] Run batch evaluations against a specific agent version.
- [ ] Evaluate violence, fluency, and task adherence; inspect scores and failures.
- [ ]

#### C6. Evaluation: `azure-ai-evaluation`

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 1 — write from memory, no AI, under the clock.*

- [ ] Built-in evaluators (`GroundednessEvaluator`, `RelevanceEvaluator`, `CoherenceEvaluator`, `FluencyEvaluator`, `SimilarityEvaluator`, `F1ScoreEvaluator`, safety evaluators via `AzureAIProject`, agent evaluators: `IntentResolutionEvaluator`, `ToolCallAccuracyEvaluator`, `TaskAdherenceEvaluator`), custom evaluator as a class or prompty, `evaluate(data=jsonl, evaluators={...}, azure_ai_project=...)`, column mapping, local vs cloud runs, thresholds and pass/fail, simulators (adversarial simulator, direct/indirect attack simulator), red-teaming agent, continuous evaluation on traces.
- [ ] Exercise: eval harness as a pytest module that fails CI when groundedness drops below threshold; run it in GitHub Actions on PR.

### OBSERVABILITY

#### Documentation checklist — OBSERVABILITY

- [ ] Azure Monitor + App Insights + OpenTelemetry (traces with span-level eval scores),

#### C7. Observability: `azure-monitor-opentelemetry`, `opentelemetry-*`

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 1 — write from memory, no AI, under the clock.*

- [ ] `configure_azure_monitor(connection_string=...)`, OpenAI instrumentation (`opentelemetry-instrumentation-openai-v2`), Agent Framework / Foundry tracing flags, GenAI semantic convention attributes (`gen_ai.request.model`, `gen_ai.usage.input_tokens`, …), custom spans around tools and retrieval, attaching eval scores to spans, sampling, PII redaction in traces, KQL queries over `dependencies`/`traces`/`customEvents` in App Insights for p95 and cost per request.
- [ ] Exercise: trace the tool-calling loop end to end, write the KQL that returns p95 latency and tokens per request by tool for the last hour.

### Release engineering and LLMOps

#### Documentation checklist — LLMOps / AgentOps on Azure: evals, tracing, release ~ADS~[LOOP]

- [ ] Foundry Evaluations: built-in evaluators (groundedness, relevance, coherence, fluency, similarity, safety evaluators, agent evaluators: intent resolution, tool-call accuracy, task adherence), custom evaluators, local vs cloud evaluation runs, continuous evaluation on traces.
- [ ] Observability: OpenTelemetry GenAI semantic conventions, Azure Monitor / App Insights, Foundry tracing, span attributes for tokens and cost, evaluator scores attached to spans, alerting on drift in eval scores or cost per request.
- [ ] Release engineering: prompt and agent versioning, eval gates in GitHub Actions, canary by APIM traffic split, rollback of prompt/model/index independently, release manifest, change record for the client's CAB.
- [ ] Cost telemetry: tokens per feature, chargeback, PTU utilisation, anomaly alerts.
- [ ] Define "resolved"/"success" for the agent and the offline + online measurement for it.

#### 8. LLMOps / AgentOps on Azure: evals, tracing, release [ADS][MKT][LOOP]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 1 — must be at 3 before any screen (the whiteboard set).*

- [ ] Foundry Evaluations: built-in evaluators (groundedness, relevance, coherence, fluency, similarity, safety evaluators, agent evaluators: intent resolution, tool-call accuracy, task adherence), custom evaluators, local vs cloud evaluation runs, continuous evaluation on traces.
- [ ] Observability: OpenTelemetry GenAI semantic conventions, Azure Monitor / App Insights, Foundry tracing, span attributes for tokens and cost, evaluator scores attached to spans, alerting on drift in eval scores or cost per request.
- [ ] Release engineering: prompt and agent versioning, eval gates in GitHub Actions, canary by APIM traffic split, rollback of prompt/model/index independently, release manifest, change record for the client's CAB.
- [ ] Cost telemetry: tokens per feature, chargeback, PTU utilisation, anomaly alerts.
- [ ] Define "resolved"/"success" for the agent and the offline + online measurement for it.

#### C8. Production Python stack (your SDE persona)

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 1 — write from memory, no AI, under the clock.*

- [ ] `httpx` async clients with timeouts/limits, `pydantic` v2 models and settings (`pydantic-settings` for env/Key Vault), `FastAPI` (dependencies, background tasks, SSE streaming endpoint, health/readiness), `pytest` + `pytest-asyncio` + `respx`/mocks, `tenacity` or hand-rolled backoff, `uv`, `ruff`, `mypy --strict`, `pre-commit`, structured logging (`structlog`), Dockerfile (multi-stage, non-root, `uv` lockfile), GitHub Actions (OIDC login to Azure with `azure/login`, build and push to ACR, deploy to Container Apps, run evals), `.env` discipline, secrets never in code.

### TRUST & SAFETY

#### Documentation checklist — TRUST & SAFETY

#### 7. Responsible AI design, Microsoft-flavoured, mapped to regulation [COG][ADS][MKT]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 1 — must be at 3 before any screen (the whiteboard set).*

- [ ] Microsoft Responsible AI Standard principles; harm taxonomy for the use case; transparency note; impact assessment template; human oversight points.
- [ ] Technical controls: Content Safety categories and thresholds, prompt shields, groundedness, PII detection (Language service), red-team evidence (PyRIT, Foundry red-teaming agent), eval gates.
- [ ] Regulatory mapping: EU AI Act risk tier for the use case, GPAI vs deployer obligations, Article 50 transparency, logging and record-keeping; UK: FCA Consumer Duty, SS1/23 model risk management, SMCR accountability, DORA for ICT third-party risk; GDPR Article 22 and DPIA triggers; NIST AI RMF functions (Govern, Map, Measure, Manage); ISO/IEC 42001 AIMS clauses.
- [ ] Be able to produce: system card outline, DPIA outline, model risk record, approval-gate checklist. Governance as artefact, not reading list (Boston Hale, TEKsystems ads).

#### 15. AI security architecture and threat modelling [ADS][MKT]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 2 — expected of an architect, examined at the client interview.*

- [ ] OWASP LLM Top 10 (2025), MITRE ATLAS, prompt injection (direct, indirect via retrieved content and tool results), tool-based exfiltration, excessive agency, insecure output handling, supply chain (models, skills, MCP servers), data poisoning of indexes; controls: input/output filters, tool allow-lists and scopes, egress control, sandboxing of code execution, human approval for irreversible actions, canary tokens, rate limits, logging for forensics; red-teaming with PyRIT; Defender for AI / Defender for Cloud AI workload protection; Sentinel analytics for AI.

#### 24. Governance tooling

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 3 — differentiators the stronger ads name.*

- [ ] Azure Policy for AI, Purview AI Hub / DSPM for AI, Defender for Cloud AI posture, audit logging to Log Analytics with retention, Entra access reviews for agent identities, Power Platform DLP for Copilot Studio.

#### C9. Content Safety: `azure-ai-contentsafety`

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 2 — write with docs open, understand every line.*

- [ ] `ContentSafetyClient.analyze_text` / `analyze_image`, categories and severity, blocklists, Prompt Shields (`shield_prompt` for user prompts and documents — indirect injection), groundedness detection, protected material detection; where to place each in the request path; how to fail closed and log.
- [ ] Exercise: middleware for the agent that runs Prompt Shields on every retrieved chunk before it enters context and records the decision in the trace.

#### C24. PyRIT — red-teaming orchestrators against your agent, converters, scorers; produce the red-team evidence file for A11.

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 3 — read fluently, build once.*

- [ ] PyRIT — red-teaming orchestrators against your agent, converters, scorers; produce the red-team evidence file for A11.

### OPTIMIZATION and COST

#### Documentation checklist — OPTIMIZATION

#### Documentation checklist — COST

- [ ] Non-functional budget to state unprompted: p95 latency per hop, tokens per request, cost per 1k requests, availability target, RPO/RTO for memory and audit stores, max blast radius of a prompt-injection event.

#### 16. FinOps for GenAI with numbers [MKT][LOOP]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 2 — expected of an architect, examined at the client interview.*

- [ ] Token economics per model, PTU arithmetic (PTU per TPM, reservation discounts, utilisation targets), prompt caching savings, semantic cache hit-rate, batch API discount, model routing policy, cost per 1k requests on A3, chargeback design, budget alerts.

### Enterprise production capabilities and Well-Architected design

#### Documentation checklist — Foundry — Enterprise Production Capabilities

- [ ] Entra identity + least-privilege RBAC; test denied access.
- [ ] Private inbound endpoint + isolated outbound networking.
- [ ] Supported model content filters; test blocked input/output.
- [ ] Application/non-MCP tool safety controls where filters do not apply.
- [ ] Applicable Azure Policy assignments + compliance/enforcement.
- [ ] Traces + latency/error monitoring.
- [ ] Every component must have an answer to: identity, network path, data residency (UK South / UK West, EU Data Boundary), what is logged, what is private.
- [ ] Doc anchors: Azure Well-Architected Framework (five pillars, AI workload guidance), Azure OpenAI baseline reference architecture (Architecture Center), Foundry networking / Private Link docs, APIM GenAI gateway policies.

#### Documentation checklist — Well-Architected pillars applied to an AI workload, with NFR numbers ~COG~[LOOP]

- [ ] Reliability: multi-region model deployments, APIM backend pools and circuit breaker, retry/backoff with jitter, idempotent tool calls, queue-based load levelling, graceful degradation (smaller model, cached answer, human route).
- [ ] Security: identity-first (no keys), least-privilege RBAC roles (Cognitive Services OpenAI User vs Contributor, Search Index Data Reader), private endpoints, CMK, Content Safety, prompt-injection controls, egress control for tools.
- [ ] Cost optimisation: PTU vs pay-as-you-go break-even, prompt caching, semantic caching at APIM, model routing (small-first), token budgets per feature, chargeback via APIM subscriptions.
- [ ] Operational excellence: tracing, eval gates in CI, prompt/version registry, release manifest, rollback of prompt/model/index versions, runbooks.
- [ ] Performance efficiency: streaming, parallel tool calls, async ingestion, index partitioning, embeddings batch sizes, PTU sizing arithmetic.
- [ ] Be able to put a number against each pillar for A3.

#### 1. Reference architecture: RAG + agent on Azure for a regulated FS client [COG][ADS][MKT]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 1 — must be at 3 before any screen (the whiteboard set).*

- [ ] Draw from memory, in under ten minutes, with these named: Entra ID (user identity, app registrations, managed identities, agent identity), APIM in front of Azure OpenAI / Foundry models (AI gateway: token-rate limits, quota per consumer, semantic caching, model-fallback policy, key-less managed-identity auth, logging to App Insights / Event Hubs), Private Link + private endpoints + DNS zones for every PaaS hop, Key Vault (secrets, CMK), Azure AI Search (hybrid vector + BM25 + semantic ranker, security-trimmed indexes, indexers vs push), Azure OpenAI / Foundry model deployments (Standard vs Provisioned Throughput Units vs Data Zone / Global Standard, content filters), Foundry Agent Service or Agent Framework host on Container Apps / AKS, Cosmos DB (sessions, memory, audit), Storage (documents, eval sets), Document Intelligence (ingestion), Content Safety (prompt shields, groundedness, protected material), Azure Monitor + App Insights + OpenTelemetry (traces with span-level eval scores), Foundry Evaluations, Service Bus / Event Grid for async tool execution, Azure Functions / Durable Functions for long-running or human-approval steps, Defender for Cloud + Purview for data governance.
- [ ] Non-functional budget to state unprompted: p95 latency per hop, tokens per request, cost per 1k requests, availability target, RPO/RPO for memory and audit stores, max blast radius of a prompt-injection event.
- [ ] Every component must have an answer to: identity, network path, data residency (UK South / UK West, EU Data Boundary), what is logged, what is private.
- [ ] Doc anchors: Azure Well-Architected Framework (five pillars, AI workload guidance), Azure OpenAI baseline reference architecture (Architecture Center), Foundry networking / Private Link docs, APIM GenAI gateway policies.

#### 2. Well-Architected pillars applied to an AI workload, with NFR numbers [COG][MKT][LOOP]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 1 — must be at 3 before any screen (the whiteboard set).*

- [ ] Reliability: multi-region model deployments, APIM backend pools and circuit breaker, retry/backoff with jitter, idempotent tool calls, queue-based load levelling, graceful degradation (smaller model, cached answer, human route).
- [ ] Security: identity-first (no keys), least-privilege RBAC roles (Cognitive Services OpenAI User vs Contributor, Search Index Data Reader), private endpoints, CMK, Content Safety, prompt-injection controls, egress control for tools.
- [ ] Cost optimisation: PTU vs pay-as-you-go break-even, prompt caching, semantic caching at APIM, model routing (small-first), token budgets per feature, chargeback via APIM subscriptions.
- [ ] Operational excellence: tracing, eval gates in CI, prompt/version registry, release manifest, rollback of prompt/model/index versions, runbooks.
- [ ] Performance efficiency: streaming, parallel tool calls, async ingestion, index partitioning, embeddings batch sizes, PTU sizing arithmetic.
- [ ] Be able to put a number against each pillar for A3.

#### 9. The A3 walk, as spoken answer [LOOP]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 1 — must be at 3 before any screen (the whiteboard set).*

- [ ] Three minutes: what is deployed, where, eval scores, p95, cost per 1k, the OAuth/MCP trust boundary, fallback and human-review path, what you would change for a bank. Every number real.

#### 14. Architecture practice artefacts [COG][MKT]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 2 — expected of an architect, examined at the client interview.*

- [ ] HLD / LLD structure, ADR template and three real ADRs from A3 (platform choice, identity model, retrieval design), target and transition states, NFR budget table, threat model (STRIDE + OWASP LLM Top 10 + MITRE ATLAS), rollout/rollback plan, handover pack, design-authority review checklist, cost model. Defend each under challenge. This is A12.

### Azure deployment, networking, compute, and messaging

#### Documentation checklist — Azure Deployment

- [ ] Service Bus / Event Grid for async tool execution,
- [ ] Azure Functions / Durable Functions for long-running or human-approval steps,
- [ ] Defender for Cloud + Purview for data governance.
- [ ] Foundry Agent Service or Agent Framework host on Container Apps / AKS,
- [ ] Cosmos DB (sessions, memory, audit),
- [ ] Storage (documents, eval sets),
- [ ] Document Intelligence (ingestion),

#### 10. API-led, microservices and event-driven integration for agents [COG][ADS]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 2 — expected of an architect, examined at the client interview.*

- [ ] Service Bus (queues, topics, sessions, dead-letter, scheduled messages) vs Event Grid (push, event-driven fan-out, CloudEvents) vs Event Hubs (streaming); when each.
- [ ] Async tool execution: request/response over queues, correlation IDs, outbox pattern, idempotency keys, exactly-once myths, saga / compensation for multi-step agent actions, human-approval step as a durable wait (Durable Functions, Logic Apps), replay and poison handling.
- [ ] API design: APIM products/subscriptions, versioning, OpenAPI as tool schema, backend pools, policy expressions, GraphQL where relevant.
- [ ] Enterprise integration: Logic Apps connectors, Dataverse, SAP (OData / BTP), ServiceNow, Salesforce; Microsoft Graph for M365 data (Access Computer Consulting ad).

#### 11. Networking and landing zone for AI [ADS][MKT]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 2 — expected of an architect, examined at the client interview.*

- [ ] Hub-spoke, Azure Virtual Network Manager, private endpoints and Private DNS zones for OpenAI, Search, Storage, Key Vault, Cosmos, Container Apps; Azure Firewall egress with FQDN rules; Front Door + WAF; no public endpoints on PaaS; ExpressRoute/VPN for on-prem; managed VNet for Foundry hub/projects; Container Apps environment VNet integration; AKS private cluster.
- [ ] Landing-zone accelerators (ALZ, AI landing zone), policy as code (Azure Policy initiatives for AI: deny public network access, require CMK), management groups, subscription vending.
- [ ] Data residency: UK South / UK West pairing, EU Data Boundary, where Global Standard routes inference.

#### 12. Compute and hosting choices [ADS]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 2 — expected of an architect, examined at the client interview.*

- [ ] Container Apps (jobs, scale to zero, Dapr, sidecars) vs AKS (when the client's platform team mandates it; Workload Identity, KEDA, ingress, Azure CNI, private cluster, GitOps/Flux) vs Functions / Durable Functions vs App Service; GPU needs (rare in this lane). Hays, Uniting People and Deloitte name AKS/Kubernetes.
- [ ] Temporal / Durable Functions / Logic Apps for long-running agent workflows (Uniting People ad names Temporal).

#### C13. Messaging: `azure-servicebus`, `azure-eventgrid`, `azure-functions`

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 2 — write with docs open, understand every line.*

- [ ] Service Bus sender/receiver, sessions, dead-letter handling, peek-lock and completion, scheduled messages; Event Grid publish/subscribe with CloudEvents; Azure Functions Python v2 model with triggers (HTTP, Service Bus, timer), Durable Functions orchestrations with `wait_for_external_event` for human approval. This is the event-driven answer Cognizant asks for, in code.
- [ ] Exercise: tool execution over Service Bus with idempotency key in Cosmos and a Durable Functions approval step.

### APIM AI gateway

#### Documentation checklist — APIM

APIM in front of Azure OpenAI / Foundry models (AI gateway: token-rate limits, quota per consumer, semantic caching, model-fallback policy, key-less managed-identity auth, logging to App Insights / Event Hubs), Private Link + private endpoints + DNS zones for every PaaS hop, Key Vault (secrets, CMK),

#### C18. APIM AI-gateway policies (XML you can read and edit)

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 2 — write with docs open, understand every line.*

- [ ] `azure-openai-token-limit`, `azure-openai-emit-token-metric`, `azure-openai-semantic-cache-lookup/store`, `llm-*` equivalents for non-OpenAI models, backend pools with priority/weight and circuit breaker, `authentication-managed-identity`, `validate-jwt` / `validate-azure-ad-token`, rate-limit-by-key, `set-backend-service` for model routing, logging to Event Hub; APIM for MCP servers.
- [ ] Exercise: write the policy for token limits per subscription + managed-identity auth + fallback to a second deployment; test with a load script and read the metrics.

### AI SEARCH and enterprise RAG

#### Documentation checklist — AI SEARCH

Azure AI Search (hybrid vector + BM25 + semantic ranker, security-trimmed indexes, indexers vs push),

#### Documentation checklist — Enterprise RAG on Azure AI Search, including GraphRAG ~COG~[MKT]

- [ ] Ingestion: Document Intelligence layout model, chunking strategies (fixed, semantic, layout-aware, parent-child), integrated vectorisation vs custom pipeline, skillsets vs push API, incremental indexing, index versioning and blue/green reindex.
- [ ] Retrieval: hybrid (vector + BM25 + RRF), semantic ranker, filters and security trimming, query rewriting, multi-index federation, agentic retrieval / knowledge agents in AI Search, reranking with cross-encoders.
- [ ] Evaluation: groundedness, relevance, retrieval recall@k, answer correctness; building the golden set; Foundry evaluators vs promptfoo/RAGAS.
- [ ] Advanced: ColBERT-style late interaction, RAPTOR hierarchical summaries, GraphRAG (community summaries, entity graphs, when it beats vector RAG, cost), permission-aware RAG, freshness and TTL.
- [ ] Numbers to carry: index size vs tier, embedding cost per million tokens, p95 retrieval latency, recall uplift from hybrid vs vector-only on your own set.

#### 6. Enterprise RAG on Azure AI Search, including GraphRAG [COG][ADS][MKT]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 1 — must be at 3 before any screen (the whiteboard set).*

- [ ] Ingestion: Document Intelligence layout model, chunking strategies (fixed, semantic, layout-aware, parent-child), integrated vectorisation vs custom pipeline, skillsets vs push API, incremental indexing, index versioning and blue/green reindex.
- [ ] Retrieval: hybrid (vector + BM25 + RRF), semantic ranker, filters and security trimming, query rewriting, multi-index federation, agentic retrieval / knowledge agents in AI Search, reranking with cross-encoders.
- [ ] Evaluation: groundedness, relevance, retrieval recall@k, answer correctness; building the golden set; Foundry evaluators vs promptfoo/RAGAS.
- [ ] Advanced: ColBERT-style late interaction, RAPTOR hierarchical summaries, GraphRAG (community summaries, entity graphs, when it beats vector RAG, cost), permission-aware RAG, freshness and TTL.
- [ ] Numbers to carry: index size vs tier, embedding cost per million tokens, p95 retrieval latency, recall uplift from hybrid vs vector-only on your own set.

#### 21. Document AI and structured extraction

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 3 — differentiators the stronger ads name.*

- [ ] Document Intelligence custom models, Content Understanding, structured outputs with JSON schema, OCR fallbacks; GCS ad names document extraction/OCR.

#### C5. Azure AI Search: `azure-search-documents`

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 1 — write from memory, no AI, under the clock.*

- [ ] `SearchClient`, `SearchIndexClient`, `SearchIndexerClient`; index schema (fields, `SearchField` with `vector_search_dimensions` and profile), vector search config (HNSW/exhaustive KNN, vectorizers), semantic configuration, `search(search_text=..., vector_queries=[VectorizedQuery/VectorizableTextQuery], query_type="semantic", filter=..., select=..., top=...)`, hybrid scoring and RRF, `IndexDocumentsBatch` upload/merge, indexers + skillsets + integrated vectorisation, security filters (`search.in(groups, ...)`), scoring profiles, facets, agentic retrieval / knowledge agent APIs (check current preview name).
- [ ] Exercise: build an index with hybrid + semantic, ingest 200 chunks with embeddings, run vector-only vs hybrid vs hybrid+semantic on a 30-question golden set, compute recall@5, print the table. 60 minutes.

#### C10. Document Intelligence: `azure-ai-documentintelligence`

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 2 — write with docs open, understand every line.*

- [ ] `DocumentIntelligenceClient.begin_analyze_document("prebuilt-layout", ...)`, output formats (markdown for RAG), tables, paragraphs with roles, figures, page-aware chunking; custom extraction models; Content Understanding (newer) for multimodal. GCS ad: document extraction / OCR.
- [ ] Exercise: PDF → markdown → layout-aware chunks → index, with page citations preserved end to end.

### Data stores and grounding platforms

#### 13. Data platform as grounding layer [MKT]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 2 — expected of an architect, examined at the client interview.*

- [ ] Microsoft Fabric (OneLake, Lakehouse, Data Agents, mirroring), Azure Databricks (Unity Catalog, Mosaic AI, Vector Search), Synapse legacy, Cosmos DB (vector search, change feed, session store), Azure SQL / PostgreSQL (pgvector), Purview (classification, lineage, DLP), Text-to-SQL patterns and their guardrails.

#### C12. Cosmos DB: `azure-cosmos`

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 2 — write with docs open, understand every line.*

- [ ] Containers, partition key design for sessions (`/session_id`) and audit (`/tenant_id`), TTL, change feed for async processing, vector search in Cosmos (DiskANN), point reads vs queries and RU cost, optimistic concurrency with ETag — the memory and audit store in the reference architecture.

#### C14. Storage: `azure-storage-blob`

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 2 — write with docs open, understand every line.*

- [ ] Upload/download, SAS vs managed identity, lifecycle, immutability (WORM) for audit sets, event-driven ingestion with Event Grid on blob created.

#### C23. Fabric and Databricks hooks — Fabric REST/notebooks, OneLake shortcuts, Databricks SDK and Mosaic AI Vector Search, Unity Catalog grants; enough to read a client's grounding layer.

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 3 — read fluently, build once.*

- [ ] Fabric and Databricks hooks — Fabric REST/notebooks, OneLake shortcuts, Databricks SDK and Mosaic AI Vector Search, Unity Catalog grants; enough to read a client's grounding layer.

### Microsoft 365, Copilot Studio, and Graph

#### 17. Microsoft 365 Copilot and the agent surface [ADS]

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 2 — expected of an architect, examined at the client interview.*

- [ ] M365 Copilot extensibility (declarative agents, custom engine agents, Copilot connectors / Graph connectors), Copilot Studio agents published to Teams/M365, SharePoint grounding and oversharing risk (Purview, Restricted SharePoint Search), licensing basics, adoption governance. Hays £800 says Copilot must-have.

#### C15. Microsoft Graph: `msgraph-sdk` (Python) / Graph REST

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 2 — write with docs open, understand every line.*

- [ ] App-only vs delegated permissions, consent, `GraphServiceClient`, reading mail/calendar/SharePoint/Teams on behalf of the user, throttling; needed for M365-facing agents (Access Computer Consulting, Copilot-adjacent ads).

#### C22. Copilot Studio and Power Platform surface — Copilot Studio agent authoring (topics, generative orchestration, knowledge sources, actions calling Foundry/MCP/REST), Power Platform CLI (`pac`) for ALM of agents, Dataverse basics, DLP policies; declarative agents for M365 Copilot via Teams Toolkit / Agents Toolkit (manifest JSON). Read and demo level, not daily coding.

*Source B: Part 2 — SDKs, tooling and code (what you write); Tier 3 — read fluently, build once.*

- [ ] Copilot Studio and Power Platform surface — Copilot Studio agent authoring (topics, generative orchestration, knowledge sources, actions calling Foundry/MCP/REST), Power Platform CLI (`pac`) for ALM of agents, Dataverse basics, DLP policies; declarative agents for M365 Copilot via Teams Toolkit / Agents Toolkit (manifest JSON). Read and demo level, not daily coding.

### Certification and Azure fundamentals

#### 25. AI-102 objectives (week 9) — Foundry, Azure OpenAI, AI Search, Document Intelligence, Language, Vision, Speech, Content Safety, agents; the exam frames the vocabulary SI panels use.

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 4 — certification and vocabulary layer.*

- [ ] AI-102 objectives (week 9) — Foundry, Azure OpenAI, AI Search, Document Intelligence, Language, Vision, Speech, Content Safety, agents; the exam frames the vocabulary SI panels use.

#### 26. AZ-305 objectives (week 16) — identity, governance, data storage, business continuity, compute, networking, migration; the architect tie-breaker.

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 4 — certification and vocabulary layer.*

- [ ] AZ-305 objectives (week 16) — identity, governance, data storage, business continuity, compute, networking, migration; the architect tie-breaker.

#### 27. Azure fundamentals you must not fumble — resource groups vs subscriptions vs management groups, RBAC vs Azure Policy vs locks, regions and availability zones, ARM/Bicep basics, tags and cost allocation, Monitor vs Log Analytics vs App Insights, Key Vault vs App Configuration, Entra tenants vs subscriptions.

*Source B: Part 1 — Architecture mastery (what you design and defend); Tier 4 — certification and vocabulary layer.*

---

## Original source priorities and planning context

The following source material is retained as provenance and study targets; its original “superseded” wording refers to Source B's earlier inputs, not to this merge.

### Source B provenance and rating scales

Single reference, built 30 Oct 2026, merging the architecture mastery list and the SDK/code list (both superseded by this file). Sources: Cognizant Azure AI Tech/Solution Architect req (27 Oct); London_Contract_Roles digest Azure ads 22–30 Oct (Hays £800 investment manager, Adecco £700–800, Experis, Uniting People/Apollo, Hays AI Developer, NXA, GCS, Access Computer Consulting, Talent Smart, TEKsystems, Boston Hale, Summer-Browning/Morson); the 13 Oct market studies; ai_role_requirements copy.md (7 Oct). Part 1 is what you must be able to design and defend; Part 2 is what you must be able to write. The crosswalk ties them so every architecture item has the code that proves it.

Rating scales. Architecture (Part 1, items 1–27): 0 cannot explain · 1 can describe · 2 can whiteboard and defend · 3 have built it and can quote numbers · 4 can teach it and cite the doc. Code (Part 2, items C1–C28): F0 never used · F1 can read it · F2 can write it with docs open · F3 can write it from memory in a timed exercise · F4 can review someone else's and spot the production gaps. Targets before January: 3 / F3 on tier 1 and tier 2, 2 / F2 on tier 3, 1–2 on tier 4.

Legend: [ADS] = named in the Oct ads · [COG] = Cognizant req · [MKT] = 13 Oct market studies · [LOOP] = interview-loop evidence rather than ad text.

Package facts checked 30 Oct 2026 against learn.microsoft.com: the Foundry SDK is `azure-ai-projects>=2.0.0` for new Foundry projects (1.x is Foundry classic); `azure-ai-inference` is being deprecated and retires 30 May 2026 — do not learn it; Microsoft Agent Framework 1.0 shipped 3 April 2026 as `agent-framework` with `FoundryChatClient` in `agent_framework.foundry`; Claude models in Foundry are reached through the Anthropic SDK at the `/anthropic` endpoint. Re-check versions before each build block; this layer moves monthly.

### Original tier contracts

#### Part 1 — Architecture mastery (what you design and defend)

##### Tier 1 — must be at 3 before any screen (the whiteboard set)

##### Tier 2 — expected of an architect, examined at the client interview

##### Tier 3 — differentiators the stronger ads name

##### Tier 4 — certification and vocabulary layer

#### Part 2 — SDKs, tooling and code (what you write)

Numbered C1–C28 so the crosswalk references them. Python first; C# awareness only where ads name it (Hays AI Developer: Python/C#). Ads and the Cognizant req say "hands-on"; Talent Smart says "must code without AI assistants"; TEKsystems says "personally built and operated".

##### Tier 1 — write from memory, no AI, under the clock

##### Tier 2 — write with docs open, understand every line

##### Tier 3 — read fluently, build once

### Crosswalk — architecture item → code that proves it

| Part 1 architecture item | Part 2 code items |
|---|---|
| 1 Reference architecture RAG + agent | C1 identity, C2 OpenAI SDK, C3 Foundry SDK, C5 AI Search, C7 observability, C17 Bicep, C18 APIM policies |
| 2 Well-Architected with NFR numbers | C7 observability (KQL for p95 and cost), C18 APIM (limits, fallback), C8 production stack |
| 3 Identity, authorisation, Zero Trust | C1 azure-identity, C16 MCP auth with Entra, C15 Graph permissions, C11 Key Vault |
| 4 Azure OpenAI / Foundry model layer | C2 OpenAI SDK, C3 Foundry SDK, C9 Content Safety, C25 Anthropic on Foundry |
| 5 Agent platform choice | C3 Foundry agents, C4 Agent Framework, C20 LangGraph, C21 OpenAI Agents SDK, C22 Copilot Studio |
| 6 Enterprise RAG and GraphRAG | C5 AI Search, C10 Document Intelligence, C14 Storage, C12 Cosmos vectors |
| 7 Responsible AI and regulation | C9 Content Safety, C6 safety evaluators, C24 PyRIT |
| 8 LLMOps / AgentOps | C6 azure-ai-evaluation, C7 observability, C8 GitHub Actions, C19 CLI canaries |
| 9 The A3 walk | all tier 1 code, with real numbers from C7 |
| 10 API-led, event-driven integration | C13 Service Bus / Event Grid / Durable Functions, C18 APIM |
| 11 Networking and landing zone | C17 Bicep (private endpoints, DNS zones), C19 CLI |
| 12 Compute and hosting | C8 Dockerfile and Actions, C17 Container Apps / AKS in Bicep |
| 13 Data platform grounding | C12 Cosmos, C23 Fabric / Databricks hooks |
| 14 Architecture artefacts (A12) | C17 Bicep as LLD, C7 numbers for the NFR table |
| 15 AI security and threat modelling | C9 Prompt Shields, C16 MCP scopes, C24 PyRIT, C18 validate-jwt |
| 16 FinOps | C2 usage accounting, C18 token metrics, C7 cost KQL |
| 17 M365 Copilot surface | C22 Copilot Studio / declarative agents, C15 Graph |
| 18 MCP on Azure | C16 |
| 19 A2A and multi-agent | C4 workflows and handoffs |
| 20 Model routing | C18 set-backend-service, C2 |
| 21 Document AI | C10 |
| 23 Fine-tuning | C3 fine-tuning via Foundry |
| 24 Governance tooling | C17 Azure Policy assignments, C19 |

### Interview prompts to rehearse against this list

- "Whiteboard a RAG + agent platform for a UK bank's complaints team. Go." (1, 2, 3, 6, 7)
- "The CISO says no public endpoints and no keys. Show me." (3, 11)
- "OIDC or SAML for the agent? Why?" (3)
- "How do you stop an agent emailing a customer twice if the tool times out?" (10)
- "What does the release manifest contain and what do you roll back first?" (8)
- "What are your eval scores, p95 and cost per 1k on the thing you built?" (9)
- "Foundry Agent Service, Agent Framework or Copilot Studio for this?" (5)
- "Map this use case to the EU AI Act and SS1/23 and tell me what evidence the model risk team needs." (7)
- "PTU or pay-as-you-go at 40 million tokens a day?" (16)
- "Give me three ADRs from your reference build." (14)
- "What is in your threat model and which control covers indirect prompt injection from a retrieved PDF?" (15)
- "A GraphRAG index costs how much more than a vector index and when is it worth it?" (6)

### Decks this list feeds

S28 Azure AI Foundry (new cards for 1, 4, 5, 6, 8, 17–24), S27 OAuth for tools (3), S26 API performance & security (10, 11), S25 security (15), S30 AI governance & regulation (7, 24), S07 RAG (6), S01 production architecture (2, 12, 13, 14).

### Repos to read and reproduce (Azure column of your Reading Map)

- microsoft/agent-framework (python/packages/core, azure-ai, samples/workflows)
- Azure/azure-sdk-for-python: sdk/ai/azure-ai-projects samples, sdk/evaluation/azure-ai-evaluation samples, sdk/search/azure-search-documents samples
- Azure-Samples/azure-search-openai-demo (the canonical RAG app: read the retrieval, auth and eval code)
- Azure-Samples/openai-aca-lz and the Azure OpenAI landing-zone / baseline reference architectures (Bicep)
- Azure-Samples/AI-Gateway (APIM GenAI policies labs)
- Azure-Samples/remote-mcp-functions-python and Azure-Samples/mcp-container-ts/py samples
- Azure/PyRIT
- microsoft/graphrag
- modelcontextprotocol/python-sdk

### How this maps onto the daily plan

- The 45-minute no-AI exercise rotates through C1, C2, C5, C6, C8, C13 (and C16 once a week).
- The 1.5–2h A3 build block takes C3, C4, C5, C7, C9, C17, C18 in that order until A3 shows eval scores, p95 and cost per 1k from real traces.
- The 60-minute AI-dev-tools block is where Claude Code / Codex may be used — for scaffolding tiers 2–3, never for the exercise.
- Every item closed produces cards into S28 (Foundry), S27 (OAuth), S26 (API), S04 (evals) and SW02 (Python interview coding).

## Source differences and open items to resolve before building

- [ ] Reconcile Terraform hands-on scope with Source B C17's awareness-only wording; retain Bicep too.
- [ ] Check current SDK/API names before each build: the sources mix threads/runs/connected agents with newer conversations/responses/agent versions. Do not implement legacy names just because they are preserved here.
- [ ] Re-check package versions, preview/GA status, model availability, CLI commands, and roles against the local documentation and official sources at build time.
- [ ] Source B says “RPO/RPO”; Source A says “RPO/RTO”. Keep both source texts and set explicit recovery-point and recovery-time objectives in the build.
- [ ] Resolve Source A's unfinished Responses “all tools” link and fine-tuning ellipsis. The empty EVALS checkbox is retained as an unfilled source slot.
- [ ] Verify dated certification names and regulatory applicability before using them as current requirements; this merge makes no new certification or legal assessment.
- [ ] Verify source claims about memory, identity, deployment ownership, managed compute, and Toolbox against the chosen product/API version.

## Existing repository modules and labs

Read-only inspection on 30 October 2026. The repo's own track README marks all proficiency unassessed and existing code not newly runtime-verified. **No lab was executed or deployed for this merge.** Code presence below means existing material, not production readiness. Relative “F03/F05/F08” references inside older lab prose may predate module renaming; use the actual paths linked here.

| Module | Subject/build starting point | Existing lab directories |
|---|---|---|
| [F01](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F01-Reference-Architecture-and-WAF/README.md) | Reference Architecture and WAF | Module study/design material; no numbered lab directory found. |
| [F02](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F02-Landing-Zones-and-Networking/README.md) | Landing Zones and Networking | Module study/design material; no numbered lab directory found. |
| [F03](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F03-Identity-and-Zero-Trust/README.md) | Identity and Zero Trust | Module study/design material; no numbered lab directory found. |
| [F04](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F04-Foundry-SDKs-and-Deployment/README.md) | Foundry SDKs and Deployment | Module study/design material; no numbered lab directory found. |
| [F05](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F05-Creating-Agents/README.md) | Creating Agents | [01-seven-ways](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F05-Creating-Agents/labs/01-seven-ways/README.md)<br>[02-hosted-agents](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F05-Creating-Agents/labs/02-hosted-agents/README.md)<br>[03-multi-agent-workflow](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F05-Creating-Agents/labs/03-multi-agent-workflow/README.md)<br>[04-memory](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F05-Creating-Agents/labs/04-memory/README.md)<br>[05-knowledge-ai-search](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F05-Creating-Agents/labs/05-knowledge-ai-search/README.md) |
| [F06](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F06-Agent-Tooling-MCP-and-Integration/README.md) | Agent Tooling MCP and Integration | [01-identity-conditional-access](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F06-Agent-Tooling-MCP-and-Integration/labs/01-identity-conditional-access/README.md)<br>[02-mcp-tool](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F06-Agent-Tooling-MCP-and-Integration/labs/02-mcp-tool/README.md)<br>[03-toolbox](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F06-Agent-Tooling-MCP-and-Integration/labs/03-toolbox/README.md)<br>[04-mcp-auth-apim](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F06-Agent-Tooling-MCP-and-Integration/labs/04-mcp-auth-apim/README.md)<br>[05-private-tool-catalog](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F06-Agent-Tooling-MCP-and-Integration/labs/05-private-tool-catalog/README.md)<br>[06-a2a](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F06-Agent-Tooling-MCP-and-Integration/labs/06-a2a/README.md) |
| [F07](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F07-RAG-on-AI-Search/README.md) | RAG on AI Search | [01-knowledge-base](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F07-RAG-on-AI-Search/labs/01-knowledge-base/README.md) |
| [F08](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F08-Evals-Tracing-and-Release/README.md) | Evals Tracing and Release | [01-observability](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F08-Evals-Tracing-and-Release/labs/01-observability/README.md)<br>[02-evals](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F08-Evals-Tracing-and-Release/labs/02-evals/README.md) |
| [F09](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F09-APIM-AI-Gateway/README.md) | APIM AI Gateway | Module study/design material; no numbered lab directory found. |
| [F10](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F10-Security-and-Governance/README.md) | Responsible AI Security and Governance | Module study/design material; no numbered lab directory found. |
| [F11](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F11-Copilot-Studio-and-M365-Boundary/README.md) | Copilot Studio and M365 Boundary | Module study/design material; no numbered lab directory found. |
| [F12](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F12-Fine-Tuning-and-Model-Routing/README.md) | Fine Tuning and Model Routing | [01-sft-ticket-tone](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F12-Fine-Tuning-and-Model-Routing/labs/01-sft-ticket-tone/README.md) |
| [F13](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F13-Foundry-Local/README.md) | Foundry Local | [01-local-ticket-agent](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F13-Foundry-Local/labs/01-local-ticket-agent/README.md) |

### Lab inventory and evidence status

| Lab | Artifacts found | Verification status |
|---|---|---|
| [01-seven-ways](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F05-Creating-Agents/labs/01-seven-ways/README.md) | 01-walkthrough.ipynb, 03-voice-prompt-agent.py, _common.py, 02-prompt-agent-sdk.py, 06-invoke-everything.py, 04-ephemeral-agent.py, 07-versions-and-publish.py, 05-foundry-agent-af.py, azure.yaml | Existing code/configuration/notebook material; functionality unverified. |
| [02-hosted-agents](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F05-Creating-Agents/labs/02-hosted-agents/README.md) | deploy.sh, invoke.py, main.py, deploy_with_sdk.py, azure.yaml, langgraph.json | Existing code/configuration/notebook material; functionality unverified. |
| [03-multi-agent-workflow](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F05-Creating-Agents/labs/03-multi-agent-workflow/README.md) | run_local.py, azure.yaml, deploy_workflow.py, main.py | Existing code/configuration/notebook material; functionality unverified. |
| [04-memory](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F05-Creating-Agents/labs/04-memory/README.md) | agent-memory.ipynb | Existing code/configuration/notebook material; functionality unverified. |
| [05-knowledge-ai-search](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F05-Creating-Agents/labs/05-knowledge-ai-search/README.md) | foundry-iq-grounding.ipynb | Existing code/configuration/notebook material; functionality unverified. |
| [01-identity-conditional-access](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F06-Agent-Tooling-MCP-and-Integration/labs/01-identity-conditional-access/README.md) | entra-agent-id-ca.ipynb | Existing code/configuration/notebook material; functionality unverified. |
| [02-mcp-tool](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F06-Agent-Tooling-MCP-and-Integration/labs/02-mcp-tool/README.md) | mcp_tool_demo.py, logic-apps-mcp.ipynb | Existing code/configuration/notebook material; functionality unverified. |
| [03-toolbox](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F06-Agent-Tooling-MCP-and-Integration/labs/03-toolbox/README.md) | toolbox_demo.py, connectors-mcp.ipynb | Existing code/configuration/notebook material; functionality unverified. |
| [04-mcp-auth-apim](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F06-Agent-Tooling-MCP-and-Integration/labs/04-mcp-auth-apim/README.md) | mcp_auth_matrix.py, apim-ai-gateway.ipynb | Existing code/configuration/notebook material; functionality unverified. |
| [05-private-tool-catalog](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F06-Agent-Tooling-MCP-and-Integration/labs/05-private-tool-catalog/README.md) | private_tool_catalog.py, tool-catalog-registration.ipynb | Existing code/configuration/notebook material; functionality unverified. |
| [06-a2a](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F06-Agent-Tooling-MCP-and-Integration/labs/06-a2a/README.md) | logic-apps-invoke-agent-a2a.ipynb, a2a_demo.py, workflow.json | Existing code/configuration/notebook material; functionality unverified. |
| [01-knowledge-base](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F07-RAG-on-AI-Search/labs/01-knowledge-base/README.md) | connect_agent.py, provision_kb.py | Existing code/configuration/notebook material; functionality unverified. |
| [01-observability](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F08-Evals-Tracing-and-Release/labs/01-observability/README.md) | observability-otel.ipynb | Existing code/configuration/notebook material; functionality unverified. |
| [02-evals](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F08-Evals-Tracing-and-Release/labs/02-evals/README.md) | 06_agent_optimizer.py, 02_rubric_generation.py, 04_scheduled_trace_eval.py, _common.py, 01_batch_eval_agent_target.py, 03_continuous_evaluation_rule.py, eval.yaml, 05_red_team.py | Existing code/configuration/notebook material; functionality unverified. |
| [01-sft-ticket-tone](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F12-Fine-Tuning-and-Model-Routing/labs/01-sft-ticket-tone/README.md) | make_dataset.py, job.yaml, submit_sft.py | Existing code/configuration/notebook material; functionality unverified. |
| [01-local-ticket-agent](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/F13-Foundry-Local/labs/01-local-ticket-agent/README.md) | local_ticket_agent.py, olive_optimize.sh | Existing code/configuration/notebook material; functionality unverified. |

### Static observations for choosing a build

- F06's MCP script contains tool construction and an approval-response loop; F07's knowledge-base connection script contains a project connection, agent version, and retrieval invocation; F08's batch-evaluation script contains dataset upload, evaluator definition, run submission, and result polling. These are implementation material, not empty placeholders, but were not run.
- F08's evaluation README explicitly uses a separate environment because its examples need newer Projects SDK surfaces than the Agent Framework adapter environment permits. Inspect each lab's requirements before execution; do not blindly share the root `.venv`.
- F05 includes prompt/hosted-agent, workflow, memory, and AI Search examples. F06 includes MCP, toolbox, auth/APIM, private catalog, and A2A examples. F07 supplies knowledge-base material; F08 supplies observability and evaluations; F12 supplies SFT; F13 supplies local-runtime material.
- Existing labs are starting points for individual capability builds, not proof that every checklist item is already implemented. Architecture, Terraform, release, networking, and governance gaps remain tasks until their own evidence exists.

### Supporting local references

- [README.md](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/README.md)

- [README.md](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/labs-setup/README.md)

- [curriculum-mapping.md](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/reference/curriculum-mapping.md)

- [requirements-map.md](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/reference/requirements-map.md)

- [sdk-compatibility.md](/Users/ozgurguler/Developer/Projects/python0x/Agent-Build-02-Microsoft-Foundry/reference/sdk-compatibility.md)

- [INDEX.md](/Users/ozgurguler/Developer/Projects/python0x/documentation/INDEX.md)

- [README.md](/Users/ozgurguler/Developer/Projects/foundry-samples-reference/README.md)
