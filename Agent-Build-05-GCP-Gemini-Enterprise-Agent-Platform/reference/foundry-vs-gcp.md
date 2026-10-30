# Foundry ↔ GCP: the concept map, one row per concept (25 Oct 2026)

Expands the "Foundry ↔ GCP concept map" table in [`reading-map-gcp-agents-2026-10-25.md`](reading-map-gcp-agents-2026-10-25.md). Left column is the Microsoft Foundry track (`Agent-Build-02`), right column is this track. Map letters cite the GCP reading map; Foundry facts are as its own chapters state them and are not re-cited here. Names follow the GCP map's Naming section: Gemini Enterprise Agent Platform (ex-Vertex AI), Agent Runtime (ex-Agent Engine, API resource still `ReasoningEngine`), Agent Search (ex-Vertex AI Search), Gemini Enterprise (ex-Agentspace). The "Interview sentence" is the one line to say when asked "what is the GCP equivalent of X?".

## Landing zone

| Foundry | GCP | Where they differ | Interview sentence |
|---|---|---|---|
| Foundry resource + project | GCP project + region, plus `us`/`eu`/`global` endpoints (A9) | No project-inside-account hierarchy; folders and org policy do the tiering (I1); 24 regions including `europe-west2`, `global` only for Memory Bank and Sessions (A9) | "A Foundry project maps to a GCP project; the tiering Foundry does with resource-plus-project, GCP does with folders and org policy." |
| Landing zone Basic / Standard | VPC-SC perimeter, PSC interface, CMEK, org policy `constraints/vertexai.allowedModels` (I2, I3, F5, F6) | Agent Runtime has no internet egress inside VPC-SC; proxy VM plus Cloud NAT (I2); PSC needs a /28 network attachment and cannot change without recreate (I3) | "Standard landing zone on GCP is a VPC-SC perimeter with a PSC interface and CMEK, and the agent loses the internet unless you give it a proxy." |
| Model allow-listing via RBAC and deployments | `constraints/vertexai.allowedModels` with `predict`, `deploy`, `tune` actions, up to 500 values (F6) | Enforced by org policy, not by what is deployed; `gcp.restrictEndpointUsage` blocks the `global` endpoint (F6) | "On GCP model access is an org policy constraint, so a project cannot call a model the folder forbids." |
| Security controls matrix per service | VPC-SC, CMEK, data residency: yes for Runtime, Evals, Sessions, Memory Bank, Code Execution; no for Example Store; not for preview models (F4) | Explicit per-service matrix with a preview-model carve-out (F4) | "Check the matrix: Example Store and preview models are outside VPC-SC and CMEK." |
| Project managed identity roles | Agent Runtime service agent `service-PROJECT_NUMBER@gcp-sa-aiplatform-re.iam.gserviceaccount.com`; roles `roles/aiplatform.user`, `reasoningEngineServiceAgent`, `agentDefaultAccess`, `agentContextEditor`, `artifactregistry.reader` (I6) | Service agent is created on first deploy; custom images fail with IMAGE_PULL_BACKOFF without the Artifact Registry reader binding (I6, I8) | "Grant the Runtime service agent Artifact Registry reader before the first custom-image deploy." |
| CMEK on the AI resource | `encryptionSpec.kmsKeyName`, key ring in the same region, `roles/cloudkms.cryptoKeyEncrypterDecrypter` to the platform service agent (F5, I4) | Not supported on `global` or multi-region endpoints, so CMEK and global Memory Bank exclude each other (A9, F5) | "CMEK forces a regional endpoint; you give up `global` Sessions and Memory Bank." |
| Reference architecture | Enterprise GenAI blueprint: `common`, `development`, `non-production`, `production` folders, one PSC endpoint per Shared VPC, Terraform `terraform-google-enterprise-genai` (I1) | The blueprint is dated 2024-03-28 and predates the rename (I1) | "The blueprint is the folder layout; the agent services are newer than the page." |

## Agents

| Foundry | GCP | Where they differ | Interview sentence |
|---|---|---|---|
| Agent Service: prompt agents and hosted agents | Agent Runtime, API resource `ReasoningEngine` (A5) | No prompt-agent object; every agent is code deployed from Developer Connect, source, Dockerfile, image or SDK object (I7) | "GCP has no declarative prompt agent; everything is an ADK app on Agent Runtime." |
| `PromptAgentDefinition` + `POST /responses` | ADK `LlmAgent` + `:query` / `:streamQuery` on the resource URL (C3) | Invocation is per-agent REST under `{LOCATION}-aiplatform.googleapis.com/.../reasoningEngines/{ID}:query`, not one Responses endpoint (C3) | "Each agent is its own endpoint; there is no shared Responses API." |
| Hosted agent on Agent Framework | ADK app on Agent Runtime, or Cloud Run via `adk deploy cloud_run` (B7, C2) | Agent Runtime builds the container and runs `api_server --a2a` on 8080 (C2); Cloud Run is the self-host path with `get_fast_api_app` (B7) | "Agent Runtime is the managed host; Cloud Run is the same ADK app when you want to own the container." |
| Agent Framework workflows | ADK `SequentialAgent`, `LoopAgent`, `ParallelAgent`, graph workflows new in 2.0 (B2) | In-process code, not a separate hosted type; state flows through `output_key` and `{placeholder}` (B2) | "Workflows are ADK code inside the same deployment, not a platform object." |
| Agent versions | Agent Runtime revisions and traffic split, preview (C4) | No rollback verb; rollback is a manual split to an earlier active revision; 950 revisions per agent, archived ones unrecoverable (C4, A10) | "Rollback on GCP is shifting traffic to a previous revision, and revisions are preview." |
| Memory store + memory search tool | Memory Bank + Sessions (A2, B5) | GA on `us`/`eu`/`global`; metered as Agent Platform compute since Sep 2026 (A2); `VertexAiSessionService` needs an Agent Runtime resource (B5) | "Memory Bank is GA and billed as compute; Sessions are the conversation store it reads from." |
| Hosted agent deployment via `azd` | `adk deploy agent_engine`, `agentplatform.Client().runtimes`, Terraform `google_vertex_ai_reasoning_engine`, agents-cli (B6, A5, I8, I12) | SDK mid-migration: `vertexai.agent_engines` old, `agentplatform` new (A5); agent-starter-pack in maintenance mode, agents-cli is the successor (I11, I12) | "Deploy with `adk deploy agent_engine` or the `agentplatform` client; the old `vertexai.agent_engines` surface is on its way out." |
| Agent templates and samples | Agent Garden, preview; Application Design Center templates "Simple Agent Platform" and "Agent Platform with governance" (A7) | Deployed through agents-cli or registered into Gemini Enterprise (A7) | "Agent Garden is a sample catalogue, preview, not a runtime." |
| Custom orchestration | Subclass `BaseAgent`, override `_run_async_impl`, yield `Event`s (B3) | State is `ctx.session.state`; one `parent_agent` (B3) | "When the three workflow agents do not fit, you write the loop yourself in a `BaseAgent`." |
| Middleware and filters | ADK callbacks before/after agent, model and tool, plus error callbacks; a list stops at the first truthy result (B4) | Callbacks are where guardrails, logging and tool filtering live in code (B4) | "Callbacks are the ADK middleware; return a value to short-circuit." |
| Service quotas | 90 `Query`/`StreamQuery` per minute, 10 concurrent `BidiStreamQuery`, 100 regional resources, 950 revisions per agent, not adjustable (A10) | Express mode is roughly a tenth of each limit (A10) | "Ninety queries a minute per project-region is the number to size against." |
| Sandboxes | Code Execution, Computer Use and Shell sandboxes GA Sep 2026 (A2, A4) | Separate `sandboxes` surface in the new SDK (A5) | "Sandboxes are a platform service, not something the agent container runs." |

## Tooling and identity

| Foundry | GCP | Where they differ | Interview sentence |
|---|---|---|---|
| Entra Agent ID (blueprint → instance) | Agent Identity: SPIFFE principal `principal://TRUST_DOMAIN/NAMESPACE/AGENT_NAME`, `identity_type=AGENT_IDENTITY` (C5, D9) | Opt-in per deployment; unset means a service account (C5); 24 h x509, bound tokens, no long-lived keys (D9, D10); delete and recreate yields a new principal (D10) | "Agent Identity is a per-agent SPIFFE principal you opt into on deploy; forget the flag and you get a service account." |
| Six connection auth types | ADK `AuthScheme` + `AuthCredentialTypes`: API key, HTTP, OAuth2, OIDC, service account (D5) | Auth is per tool or toolset in code, not a project-level connection object; interactive flow via `adk_request_credential` (D5) | "There is no connection object; each toolset carries its own auth scheme and credential." |
| MCP tool on the agent | `McpToolset` with Stdio, SSE or StreamableHTTP params, `tool_filter`, defined synchronously in `agent.py` (D3) | No auto-reconnect on session restore (D3); built-in tools cannot sit beside function tools, one built-in per agent, `AgentTool` as the workaround (D4) | "McpToolset is the MCP client; the rule to remember is one built-in tool per agent." |
| Toolbox | MCP Toolbox for Databases (`tools.yaml`) on Cloud Run, plus Agent Registry (D6, D7, D8, F7) | Toolbox is a database MCP server you host with `authRequired` and Google auth services (D7); the registry is the catalogue (F7) | "Toolbox on GCP is a DB-to-MCP server you run; the catalogue is Agent Registry." |
| APIM + API Center | Apigee MCP + API hub (D12, D13) | Apigee ingests OpenAPI 3.0.x and serves `tools/list` and `tools/call`; API hub MCP server GA Jul 2026, Agent Registry sync preview (D12, D13) | "Apigee is the gateway, API hub is the catalogue, and the sync into Agent Registry is still preview." |
| A2A v1.0 tool | `RemoteA2aAgent` and `to_a2a`, Agent Registry, Agent Gateway (C7, F7) | Experimental in ADK; Gemini Enterprise speaks 0.3 streaming and needs `a2a.compat.v0_3` (C7, C9) | "ADK A2A is experimental and the end-user layer is a protocol version behind." |
| OpenAPI tool | `OpenAPIToolset`, one `RestApiTool` per operation, name from `operationId` (D2) | 600 s httpx timeout, OpenAPI 3.x only (D2) | "Same idea, one tool per operation, auth attached to the toolset." |
| Function tools | Plain Python functions auto-wrapped in `FunctionTool`; `LongRunningFunctionTool`; `ToolContext` hidden from the model (D1) | Docstring is the description; return a dict with `status` (D1) | "A function with a docstring is a tool; `ToolContext` is how it reaches state." |
| Toolbox hosting | Cloud Run with `toolbox-identity` service account, `tools.yaml` as a Secret Manager secret, callers need `roles/run.invoker` (D8) | Secrets mounted as a file; Google auth service in `tools.yaml` with `authRequired` per tool (D7, D8) | "Toolbox runs on Cloud Run with its config in Secret Manager and IAM on the invoker." |
| Local MCP client for testing | Gemini CLI `mcpServers` block, `/mcp auth` (H6) | OAuth block in `settings.json`; `includeTools`/`excludeTools` (H6) | "Test the MCP server from Gemini CLI before an agent depends on it." |
| Workload identity options | Workload Identity Federation, service accounts, managed workload identities, agent identities (D11) | The page ranks agent identities as more secure than service accounts (D11) | "Four identity options; agent identity is the one built for agents." |

## Evals and observability

| Foundry | GCP | Where they differ | Interview sentence |
|---|---|---|---|
| Evaluators, batch and continuous evals | ADK `adk eval` with `*.evalset.json`, plus Agent Platform Evals (`client.evals`, `EvalTask`) (E1, E2, E3) | Trajectory metrics are first class (`tool_trajectory_avg_score`, `trajectory_exact_match`); the agent evaluation module is preview (E3); no first-party Cloud Build wiring page (E7) | "Two layers: `adk eval` in CI for trajectories, platform evals for rubric and LLM-judge metrics, and the CI wiring is yours." |
| Evaluation metrics catalogue | computation (`bleu`, `rouge_l`, `exact_match`), adaptive rubrics, static `GROUNDING`, `SAFETY`, `FLUENCY`, custom `LLMMetric` (E2) | Adaptive rubrics generated per case via `generate_rubrics` (E2) | "The judge writes the rubric per case unless you pin one." |
| Red teaming | No managed product page found (E7) | Continuous assurance framed by a codelab only (E7) | "I would say there is no managed red-teaming product on the map today." |
| Application Insights tracing | Cloud Trace via OpenTelemetry, Cloud Logging, Cloud Monitoring (E4, E5, E6) | On by default for new ADK agents on Agent Runtime since Jun 2026 (A2); message content capture is a consent flag (E4); metrics under `aiplatform.googleapis.com/ReasoningEngine` (E5) | "Tracing is on by default; the decision you still make is whether to capture message content." |
| Audit logs | Cloud Audit Logs on `aiplatform.googleapis.com`; Data Access logs must be enabled (F8) | Admin Activity always on, Data Access opt-in (F8) | "Admin logs are free and on; turn on Data Access logs before you need them." |
| Platform metrics | `reasoning_engine/request_count`, `/request_latencies`, `/cpu/allocation_time`, `/memory/allocation_time`; "Agent Runtime Overview" dashboard (E5) | Example alert at p99 5,000 ms (E5) | "Alert on request latency p99 from the built-in dashboard first." |
| Logs | `reasoning_engine_stdout`, `_stderr`, `_build`; filter on `resource.labels.reasoning_engine_id` (E6) | `google.cloud.logging.Client().setup_logging()` in the agent (E6) | "Three log streams per agent; the build log is where deploy failures are." |
| CI pipeline | agents-cli `eval run|generate|grade|compare|optimize`; starter-pack `.cloudbuild/pr_checks.yaml`, `staging.yaml`, `deploy-to-prod.yaml` (E7, I11, I12) | No first-party page wiring `adk eval` into Cloud Build (E7) | "The CI gate is a pytest around `AgentEvaluator`, and the pipeline is yours." |

## Governance

| Foundry | GCP | Where they differ | Interview sentence |
|---|---|---|---|
| Content safety + guardrails | Model Armor floor settings and templates, plus Gemini safety settings (F1, F2, F3) | Floor settings bind at org, folder or project and templates cannot be weaker (F1); `INSPECT_ONLY` versus `INSPECT_AND_BLOCK` (F2); safety thresholds default `OFF` for gemini-3.5-flash and later (F3) | "The floor is the minimum nobody can turn off; templates and safety settings sit above it." |
| Agent catalogue and governance policies | Agent Registry (`Agent`, `McpServer`, `Endpoint`, `Service`), Agent Gateway, IAM policies with CEL on `mcp.toolName` (F7) | Gateway is default-deny with dry-run mode; up to 5,000 resources; GKE and Cloud Run gateways "coming soon" (F7) | "Registry to find it, Gateway to reach it, CEL on the tool name to limit it." |
| Agent registration for end users | Register in Gemini Enterprise by `reasoningEngines` path or by pasted A2A card; role `discoveryengine.agentspaceAdmin` (C8, C9) | ADK agents must be hosted on Agent Runtime to register; app location must match the region prefix (C8) | "Gemini Enterprise is where users meet the agent, and it only accepts Runtime-hosted ADK agents or A2A cards." |
| Gemini safety settings | `HARM_CATEGORY_*` thresholds, `HarmBlockMethod`, non-configurable `PROHIBITED_CONTENT` and `SPII` (F3) | Default threshold `OFF` for gemini-3.5-flash and later (F3) | "Safety settings default to off on current models; Model Armor is the enforced layer." |
| Gateway policy trial | `iamEnforcementMode: "DRY_RUN"` and Model Armor `INSPECT_ONLY` on Agent Gateway (F7) | Dry-run before deny (F7) | "Turn the gateway on in dry-run, read the logs, then enforce." |

## Knowledge

| Foundry | GCP | Where they differ | Interview sentence |
|---|---|---|---|
| Foundry IQ knowledge base | Agent Search data store, RAG Engine corpus, or grounding tool (H9, H11, H12, H13) | Three products, one decision; data store is managed search, corpus is a managed pipeline you parameterise, grounding is the model's view of either (H13) | "A data store is not a corpus is not a grounding tool; pick by who owns retrieval." |
| Knowledge sources (indexed and remote) | Data store sources: website, BigQuery, Cloud Storage, Workspace, Cloud SQL, Spanner, Firestore, Bigtable, AlloyDB, JSON (H9) | No remote-source concept on the data store; live sources are grounding options such as Elasticsearch or your own search API (H12) | "Indexed sources live in the data store; live sources are grounding sources on the model call." |
| Web knowledge source | Google Search grounding, `google_search` tool, `renderedContent` must be rendered in production (B8, H12) | One built-in per agent; suggestions rendering is a stated requirement (B8, D4) | "Google Search grounding comes with a rendering obligation." |
| Gemini Enterprise connectors | 19 GA, around 100 preview including Custom MCP Server (H10) | End-user layer, owned by the Gemini Enterprise admin, not by the agent team (H10, C9) | "Connectors are what the assistant knows, not what my agent knows." |
| RAG regions and stores | RAG Engine GA `europe-west3/4`; RagManagedDb, Vector Search, Pinecone GA; VPC-SC and CMEK (H11) | Not GA in `europe-west2`, so the corpus lives in a different region from the agent (H11, A9) | "RAG Engine is the one I can put behind VPC-SC with CMEK in a European region today." |
| Agent memory versus knowledge | Memory Bank is what the agent learned from users; data store or corpus is what the company wrote (A2, H13) | Different owners, different APIs (`memory_banks` versus `discoveryengine`) (A5, H9) | "Memory is per user and learned; knowledge is shared and authored." |
| Grounding tool shapes | google-genai `Tool(retrieval=Retrieval(vertex_ai_search=VertexAISearch(datastore=...)))`; ADK `VertexAiSearchTool(data_store_id=...)` (H12, B9) | Per-user filter by overriding `_build_vertex_ai_search_config` (B9) | "Same data store, two SDK shapes; the ADK one is a built-in tool with the one-per-agent rule." |

## Tuning

| Foundry | GCP | Where they differ | Interview sentence |
|---|---|---|---|
| Fine-tuning (SFT) | Supervised tuning via `client.tunings.tune`, JSONL `contents` with `user` and `model` roles (G3, G4) | Gemini 3.5 and 3.1 tune and serve on `us`/`eu` multi-region only; 131,072 tokens per example, 1 GB JSONL, adapter sizes 1 to 16 (G2) | "SFT on GCP is a tuning job you start from google-genai and serve from a `us` or `eu` endpoint." |
| Preference and RL tuning | Preference tuning on 2.5 models only; RL fine-tuning pre-GA with reward functions up to 16 (G1, G6) | The 2.5 family retired on 2026-10-20 (B10), so preference tuning has no current base on the map | "Preference tuning has no live base model today; RL tuning is pre-GA." |
| Tuned model in the agent | `LlmAgent(model="projects/P/locations/L/endpoints/ENDPOINT_ID")` with `GOOGLE_GENAI_USE_ENTERPRISE=TRUE` (G9) | The endpoint path is the model string (G9) | "Point the agent's model string at the tuned endpoint; nothing else changes." |
| Open-model tuning | SFT for Gemma 4, Gemma 3, Qwen 3.x, Llama; distillation from MaaS teachers into open students (G7) | Distillation only for open students (G7) | "Distil into Gemma, then run it locally; that is the bridge to G07." |
| Tuning cost | Pricing page not fetched; snippet only (G8) | Verify before quoting (G8) | "I would check the pricing page rather than quote a number." |

## Local

| Foundry | GCP | Where they differ | Interview sentence |
|---|---|---|---|
| Foundry Local | Gemma 4 via Ollama or llama.cpp, ADK `LiteLlm` (H1, H2, H3, H8) | Same ADK code, only the model string changes: `LiteLlm(model="ollama_chat/gemma4:e4b")` (H8); use `ollama_chat` not `ollama` for tool loops (H8) | "Local on GCP is Gemma through LiteLLM in the same agent file." |
| Local model catalogue | Gemma 4 E2B, E4B, 12B, 26B A4B, 31B, Apache 2.0 (H1) | Multimodal at E2B and E4B; MoE at 26B (H1) | "Gemma 4 E4B is the laptop default; 26B A4B when there is a GPU." |
| On-device | Gemini Nano on Android through AICore and ML Kit GenAI APIs (H4) | Hybrid fallback through Firebase AI Logic (H4) | "On-device is Nano, with a cloud fallback you configure." |
| Local developer CLI | Gemini CLI 0.65 with `mcpServers` in `settings.json`; replaced by Antigravity CLI for unpaid users on 18 Jun 2026 (H5, H6) | MCP client config is a JSON block with `command`, `url` or `httpUrl` (H6) | "Gemini CLI is the local MCP client I test a server with before an agent does." |
| OpenAI-compatible local server | llama.cpp `llama-server -hf ggml-org/gemma-4-E2B-it-GGUF` on `http://localhost:8080/v1` (H3) | Alternative to Ollama when you want the OpenAI wire format (H3) | "llama.cpp gives me an OpenAI-shaped local endpoint for the same Gemma weights." |
| Supply-chain note | LiteLLM 1.82.7 and 1.82.8 compromised on 2026-03-24; pin `litellm>=1.84` (H8) | A pin, not a feature (H8) | "Pin LiteLLM above 1.84; two releases in March were compromised." |

## Status words at a glance (dates from the map)

Quote the status with its date; the Foundry track does the same with Learn page dates.

| GCP item | Status | Date | Map |
|---|---|---|---|
| Agent Identity | GA; its API in preview | 2026-04-22; 2026-06-18 | A2, C5 |
| Agent Registry | GA with A2A 1.0 and 0.3 | 2026-06-18 | A2 |
| Agent Gateway | GA | 2026-06-18 | A2, F7 |
| Observability (OTel default for new ADK agents) | GA | 2026-06-18 | A2 |
| Sessions and Memory Bank on `us`/`eu`/`global` | GA | 2026-06-17 | A2 |
| Computer Use and Shell sandboxes | GA | 2026-09-09 | A2 |
| Agent Runtime revisions and traffic split | preview (v1beta1) | 2026-10-22 | C4 |
| Agent Garden | preview | 2026-10-22 | A7 |
| Multi-agent via A2A on Agent Runtime | preview | 2026-10-23 | A5 |
| ADK A2A (`to_a2a`, `RemoteA2aAgent`) | experimental | undated | C7 |
| Agent evaluation module (trajectory `EvalTask`) | preview | 2026-10-22 | E3 |
| API hub MCP server | GA | 2026-07-24 | D13 |
| API hub to Agent Registry sync | preview | 2026-04-06 | D13 |
| RAG Engine in `europe-west3/4` | GA; other regions preview or allowlist | 2026-10-22 | H11 |
| RL fine-tuning | pre-GA | 2026-10-22 | G6 |
| Gemini 2.5 family | retired | 2026-10-20 | B10 |
| agent-starter-pack | maintenance mode | 2026-04-25 | I11 |

## How to use this page

Say the Interview sentence, then the "Where they differ" cell if asked to go deeper, then open the map letter if challenged. Where a cell says preview or experimental, the date in the map is the date to quote. Gaps from the map that affect this page: pricing (A11, G8), the Apigee tool-access page, the Agent Runtime VPC-SC page, and any managed red-teaming product.
