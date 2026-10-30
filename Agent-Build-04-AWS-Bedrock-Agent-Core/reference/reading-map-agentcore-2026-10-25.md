# Reading map — Amazon Bedrock AgentCore and Bedrock for agents (crawled 25 Oct 2026)

Every B-chapter cites this map by letter (B2, D4, I3 ...). Each entry: URL, the page or announcement date, one line on what it says, status. "Verify" marks a fact that was reported second-hand or a page that could not be fetched on the day. The fetch day was 25 Oct 2026; re-fetch anything older than three months before quoting it in a review.

Primary date source: the AgentCore release notes, https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html (entries through Oct 2026).

## A. Overview and status

| # | Source | Date | What it says | Status |
|---|---|---|---|---|
| A1 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html | n.d. (fetched 25 Oct 2026) | Thirteen components: Harness, Runtime, Memory, Gateway, Identity, Code Interpreter, Browser, Observability, Payments, Evaluations, Optimization, Policy, Registry | current |
| A2 | release notes (above) "October 2025 – General Availability" | 13 Oct 2025 | Runtime, Gateway, Identity, Memory, Code Interpreter, Browser, Observability GA; preview launch Jul 2025 | GA |
| A3 | https://aws.amazon.com/about-aws/whats-new/2026/03/policy-amazon-bedrock-agentcore-generally-available/ | 3 Mar 2026 | AgentCore Policy GA, 13 regions | GA |
| A4 | https://aws.amazon.com/about-aws/whats-new/2026/03/agentcore-evaluations-generally-available | 31 Mar 2026 | AgentCore Evaluations GA, 9 regions | GA |
| A5 | https://aws.amazon.com/about-aws/whats-new/2026/04/agentcore-new-features-to-build-agents-faster/ | 22 Apr 2026 | Harness preview; CLI preview context | superseded by A6 |
| A6 | https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-agentcore-harness-generally-available/ | Jun 2026 | Harness GA (managed agent loop powered by Strands) | GA |
| A7 | https://aws.amazon.com/blogs/machine-learning/the-future-of-managing-agents-at-scale-aws-agent-registry-now-in-preview/ | 9 Apr 2026 | AWS Agent Registry preview | superseded by A8 |
| A8 | https://aws.amazon.com/about-aws/whats-new/2026/08/aws-agent-registry-generally-available | 31 Aug 2026 (a migration guide says 6 Aug, verify) | Agent Registry GA: Organizations auto-detection, CMK, RAM sharing, PrivateLink, MCP endpoint, approval workflows | GA |
| A9 | https://aws.amazon.com/about-aws/whats-new/2026/08/aws-bedrock-agentcore-runtime-instances-generally-available/ | 6 Aug 2026 | Runtime Instances (EC2 capacity providers, GPU, 14-day sessions) GA | GA |
| A10 | https://aws.amazon.com/about-aws/whats-new/2026/09/new-agentcore-runtime-generally-available/ | 18 Sep 2026 | Runtime platform version V2, snapshot cold starts | GA |
| A11 | https://aws.amazon.com/about-aws/whats-new/2026/08/bedrock-agentcore-payments-ga/ | 18 Aug 2026 | Payments GA (x402, MPP) | GA, out of scope |
| A12 | https://docs.aws.amazon.com/bedrock/latest/userguide/agents-classic-maintenance-mode.html | n.d. (fetched 25 Oct 2026) | "Amazon Bedrock Agents Classic": maintenance mode, closed to new accounts from 30 Jul 2026 (CreateAgent/InvokeInlineAgent return 403), model catalogue frozen, no EOL date; migrate to Harness or Runtime; KBs and Guardrails unaffected | retiring |
| A13 | https://aws.amazon.com/bedrock/agentcore/pricing/ | fetched 25 Oct 2026 | Consumption pricing, see L | current |
| A14 | https://aws.amazon.com/bedrock/agentcore/faqs/ | fetched 25 Oct 2026 | VPC connectivity across services; A2A "coming soon" wording still present | partly stale |
| A15 | compliance entries in release notes | Jun 2026 SOC 1/2/3; Feb 2026 ISO + CSA STAR; May 2026 GovCloud US-West | | current |

Not verified today: any re:Inforce 2026 AgentCore announcement; a Nova Act × AgentCore 2026 launch; Nova 2 Pro / Omni GA.

## B. Harness and Runtime

| # | Source | Date | What it says |
|---|---|---|---|
| B1 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html | n.d. | Runtime overview: microVM per session, container (ARM64 in ECR) or direct code zip, two compute types (microVM, Instances) |
| B2 | https://aws.amazon.com/about-aws/whats-new/2025/11/amazon-bedrock-agentcore-runtime-code-deployment/ | 4 Nov 2025 | Direct code deploy for Python; Node.js added Apr 2026; Python 3.14 since Mar 2026 (release notes) |
| B3 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-how-it-works.html | n.d. | platformVersion V1 vs V2 (snapshot restore, P75 cold start 1.9–2.0 s vs 5.4–30 s; container must pass /ping within 120 s; env-var limit; 5 regions) |
| B4 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-sessions.html | n.d. | runtimeSessionId ≥33 chars, 15 min idle, 8 h max (14 d on Instances), states Active/Idle/Stopped, StopRuntimeSession, 409 RetryableConflictException, session storage / S3 Files / EFS mounts (May 2026), headers `X-Amzn-Bedrock-AgentCore-Runtime-Session-Id` and `Mcp-Session-Id` |
| B5 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-invoke-agent.html | n.d. | `invoke_agent_runtime(agentRuntimeArn, runtimeSessionId, payload, qualifier)`, payload ≤100 MB, SSE or JSON; OAuth inbound requires raw HTTPS |
| B6 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-long-run.html | n.d. | `/ping` Healthy / HealthyBusy, `add_async_task` / `complete_async_task`, custom `@app.ping`; HealthyBusy keeps the session past idle up to 8 h |
| B7 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agent-runtime-versioning.html | n.d. | Immutable versions on every update; `DEFAULT` endpoint tracks latest; custom endpoints pinned; `update_agent_runtime_endpoint` for promote/rollback; no weighted routing at the Runtime (A/B is Gateway rules or Optimization) |
| B8 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-mcp.html | n.d. | MCP mode: container at 0.0.0.0:8000/mcp, stateless default, stateful since Mar 2026 (elicitation, sampling, progress); invoke URL `https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{urlencoded-arn}/invocations?qualifier=DEFAULT` |
| B9 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a.html | n.d. | A2A mode: port 9000, JSON-RPC passthrough, card at `/.well-known/agent-card.json` served through `.../invocations/...`, SigV4 or JWT |
| B10 | release notes Dec 2025 / Mar 2026 / Jun 2026 | | WebSocket bidirectional streaming (`InvokeAgentRuntimeWithWebSocketStream`), AG-UI protocol, `InvokeAgentRuntimeCommand` shell exec and interactive terminals |
| B11 | A6 + release notes Sep 2026 | | Harness: `CreateHarness` / `InvokeHarness`, model configs (bedrock, openai, gemini, litellm), tools (inline_function, agentcore_gateway, remote_mcp, browser, code interpreter), skills, lifecycle hooks, interactive shells, custom OpenAI apiBase; exports to Strands code |
| B12 | release notes Jul–Aug 2026 | | Quotas: 1,000 TPS data plane, 25 TPS new sessions, 5,000 active sessions (us-east-1 / us-west-2) |
| B13 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/using-any-agent-framework.html | n.d. | Strands, LangGraph, Google ADK, OpenAI Agents SDK on Runtime; contract = HTTP 8080 `/invocations` + `/ping`, or MCP 8000 |
| B14 | https://aws.amazon.com/blogs/developer/building-and-deploying-net-ai-agents-with-amazon-bedrock-agentcore/ | 2026 | Microsoft Agent Framework (.NET) on AgentCore via `AWS.AgentCore.Hosting`; no Python MAF sample found (verify) |

## C. CLI, SDK, CDK

| # | Source | Date | What it says |
|---|---|---|---|
| C1 | https://github.com/aws/bedrock-agentcore-starter-toolkit | README banner, fetched 25 Oct 2026 | **Deprecated.** "Do not use this toolkit. Use the AgentCore CLI instead"; last PyPI 0.3.14 on 6 Oct 2026; dev guide says `pip uninstall` it because it shadows the new binary. Legacy commands `configure / launch / invoke / status / destroy`, `--local`, `.bedrock_agentcore.yaml` are no longer documented |
| C2 | https://github.com/aws/agentcore-cli/releases | 1.0.0 on 22 Oct 2026 | Node CLI `npm install -g @aws/agentcore` (Node 20.12+): `create --template agent-python-strands|agent-python-strands-container|...`, `add runtime|harness|memory|gateway|tool|payment-manager`, `remove`, `build`, `deploy`, `dev --mode browser` (Agent Inspector), `invoke --runtime|--harness|--gateway ... --local`, `status`, `logs`, `traces`, `export`, `eval ...`, `migrate`, `update`; direct resource groups `harness/runtime/memory/identity/gateway/payment` |
| C3 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-cli.html | n.d. | Config `agentcore/agentcore.json`, `aws-targets.json`, `.env.local`, per-harness `harness.yaml`; deploys through a thin CDK app on `@aws/agentcore-cdk`; teardown `agentcore remove all --yes && agentcore deploy --yes` |
| C4 | https://github.com/aws/agentcore-cli/blob/main/docs/local-development.md | 2026 | `agentcore dev` runs uvicorn with hot reload, `agentcore dev "<prompt>"` invokes; Docker only for container agents |
| C5 | https://pypi.org/pypi/bedrock-agentcore/json | 1.25.0 on 23 Oct 2026 | `bedrock-agentcore`, requires boto3 ≥1.43.115; extras `a2a`, `a2a-v1`, `ag-ui`, `strands-agents`, `langgraph`, `deepeval`, `ragas`, `autoevals`, `simulation` |
| C6 | https://github.com/aws/bedrock-agentcore-sdk-python | fetched 25 Oct 2026 | `BedrockAgentCoreApp`, `@app.entrypoint` (sync `def handler(payload, context)` with `context.session_id`, or async generator), `@app.ping`, `add_async_task`; guidance: validate `prompt` is a string (toolUse-injection) |
| C7 | PyPI | 21 Oct 2026 | `strands-agents` 1.62.0, `strands-agents-tools` 0.8.10, `strands-agents-evals` 1.7.0, `strands-harness`; `boto3` 1.43.118 (22 Oct) with clients `bedrock-agentcore`, `bedrock-agentcore-control`, `agent-registry` |
| C8 | https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/multi-agent-patterns/ | n.d. | Agents-as-tools, Swarm, Graph, Workflow; hooks; middleware; `agent.cancel()`; BidiAgent; A2A server/client |
| C9 | https://github.com/strands-agents/sdk-python/releases | Oct 2026 | Strands harness package and `@strands-agents/cli`; no product named "Strands Agent Builder" found (verify) |
| C10 | local venv inspection, 25 Oct 2026 | | Ground truth for every lab: boto3 operation names and input shapes, SDK signatures (see `labs-setup/00-setup/README.md` for how to regenerate) |

## D. Gateway

| # | Source | Date | What it says |
|---|---|---|---|
| D1 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-core-concepts.html | n.d. | Three target classes: MCP targets (Lambda, API Gateway REST (Dec 2025), OpenAPI, Smithy, remote MCP servers, integrations, connectors), HTTP passthrough targets, Inference targets (Jul 2026); inbound CUSTOM_JWT / AWS_IAM / AUTHENTICATE_ONLY / NONE |
| D2 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-target-http-runtime.html | Jul 2026 | AgentCore Runtime agents as Gateway targets GA; A2A services and any HTTP endpoint as passthrough; URL `https://{gwId}.gateway.bedrock-agentcore.{region}.amazonaws.com/{targetName}/invocations`; outbound modes add caller IAM credentials and token passthrough |
| D3 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-using-mcp-semantic-search.html | n.d. | Enable `searchType: SEMANTIC` at creation; tool `x_amz_bedrock_agentcore_search` with `{"query": ...}`; not for HTTP/Runtime targets; 18 regions |
| D4 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-interceptors.html | n.d. | One REQUEST + one RESPONSE Lambda interceptor per gateway; transform, validate, custom authz; `passRequestHeaders` off by default |
| D5 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-using.html | n.d. | Supported MCP versions 2026-07-28 (stateless, no initialize), 2025-11-25, 2025-06-18, 2025-03-26; MCP sessions with `Mcp-Session-Id`, streaming, elicitation/sampling passthrough (May 2026) |
| D6 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-agent-integration.html | n.d. | Strands: `MCPClient(lambda: streamablehttp_client(url, headers={"Authorization": f"Bearer {token}"}))` → `list_tools_sync()` → `Agent(tools=...)` |
| D7 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html | n.d. | 1,000 gateways/account, 100 targets/gateway, 1,000 tools/target, 15-min invocation timeout, 200 TPS tool calls, search 25/min, 6 MB payload (adjustable) |
| D8 | release notes Apr–Oct 2026 | | 3LO on MCP targets GA (Apr), VPC egress (Apr), weighted routing rules with session stickiness (Jun), configurable rate limits RPS/TPM/connections (Aug), InvokeModel wire-format translation + model fallback / circuit breaker + Step Functions connector + private CA (Oct) |
| D9 | release notes Jun–Jul 2026 | | Web Search connector GA (Jun/Jul 2026); Managed Knowledge Base as a Gateway target (see J) |

## E. Identity

| # | Source | Date | What it says |
|---|---|---|---|
| E1 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/key-features-and-benefits.html | n.d. | Workload identity directory (`arn:...:workload-identity-directory/default/workload-identity/<name>`), token vault (KMS), quota 11,000 identities/account |
| E2 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-oauth.html | n.d. | Runtime inbound: IAM SigV4 (default) or `customJWTAuthorizer` (discoveryUrl, allowedClients, allowedAudience, allowedScopes, custom claims), not both; `allowedWorkloadConfiguration` restricts a JWT runtime to a Gateway (Jul 2026); `X-Amzn-Bedrock-AgentCore-Runtime-User-Id` path exists but JWT is recommended; 401 returns RFC 9728 `WWW-Authenticate: Bearer resource_metadata=...` |
| E3 | SDK (C6) | | `@requires_access_token(provider_name, scopes, auth_flow="M2M"|"USER_FEDERATION"|"ON_BEHALF_OF_TOKEN_EXCHANGE", on_auth_url, callback_url)` and `@requires_api_key`; flow inbound JWT → `GetWorkloadAccessTokenForJWT` → `GetResourceOauth2Token` → consent URL → token cached in the vault per workload + user |
| E4 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/on-behalf-of-token-exchange.html | Apr 2026 | OBO: RFC 8693 `TOKEN_EXCHANGE` (actor token M2M / `AWS_IAM_ID_TOKEN_JWT` / NONE) or RFC 7523 `JWT_AUTHORIZATION_GRANT`; pre-built `MicrosoftOauth2` (Entra OBO); `GetResourceOauth2Token --oauth2-flow ON_BEHALF_OF_TOKEN_EXCHANGE` |
| E5 | release notes Jul 2026 | | Private Key JWT client authentication via KMS; Secrets Manager ARN references for client secrets |
| E6 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-consent-portal.html | 1 Sep 2026 | Hosted Consent Portal; requires a JWT-authorised Gateway as source |
| E7 | built-in provider vendors (boto3 enum, 25 Oct 2026) | | Google, GitHub, Slack, Salesforce, Microsoft, Custom, Atlassian, LinkedIn, X, Okta, OneLogin, PingOne, Facebook, and more |

Not found: SPIFFE-style identities; an Identity-level cross-account feature (cross-account exists for Registry via RAM and for Runtime invocation via resource policies).

## F. Policy and Guardrails

| # | Source | Date | What it says |
|---|---|---|---|
| F1 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html | n.d. | Policy engine, associate with gateway(s), every tool call intercepted, deny-by-default, `LOG_ONLY` mode, CloudWatch decision logs; not attachable to Runtime directly |
| F2 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-scope.html | n.d. | Cedar schema: principal `AgentCore::OAuthUser` (id = JWT `sub`) or `AgentCore::IamEntity`; action `AgentCore::Action::"<Target>___<Tool>"` (Runtime target `<Target>___POST:/invocations`); resource `AgentCore::Gateway::"<arn>"`; `context.input.<param>`; no action wildcards; minimal `permit(...)` example |
| F3 | A3 + release notes | 3 Mar 2026 GA | NL → Cedar with automated-reasoning validation (overly permissive / restrictive / unsatisfiable); Dogwood language for session-aware temporal policies (≤20 per engine, 24 h window) (verify syntax); quotas 1,000 policies/engine, 10 KB/policy, 400 KB schema |
| F4 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-guardrails-in-policies.html | 17 Jun 2026 GA (https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-agentcore-policy-guardrails-generally-available/) | `when guardrails { BedrockGuardrails::ContentFilter|PromptAttack|SensitiveInformation([...],[context.input.x]) ... }`, `suppressOutput` effect; gateway role needs `bedrock:InvokeGuardrailChecks`; 7 regions |
| F5 | https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html | n.d. | Content filters (incl. Prompt Attack, image), denied topics, word filters, sensitive information (PII + regex), contextual grounding, Automated Reasoning checks (GA Aug 2025), `ApplyGuardrail`, input tagging, cross-account |
| F6 | https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-tiers.html | n.d. | Standard tier (multilingual, code-aware, prompt-leakage; needs a cross-Region guardrail profile) vs Classic; Standard for contextual grounding Oct 2026 |
| F7 | https://strandsagents.com/latest/documentation/docs/user-guide/safety-security/guardrails/ and https://aws.amazon.com/blogs/security/extend-amazon-bedrock-guardrails-to-tool-interactions-using-the-strands-agents-sdk/ | n.d. | `BedrockModel(guardrail_id, guardrail_version, guardrail_trace, guardrail_redact_input/output)`; hook-based `ApplyGuardrail` on tool I/O |
| F8 | https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec07-bp05.html | n.d. | No AWS-native agent red-team service; manual red team + Evaluations (Harmfulness / Refusal / Stereotyping) |
| F9 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-permissions.html | n.d. | Execution role trust `bedrock-agentcore.amazonaws.com` with `aws:SourceAccount` / `aws:SourceArn`; caller needs `bedrock-agentcore:InvokeAgentRuntime`; SLR `AWSServiceRoleForBedrockAgentCoreRuntimeIdentity`; resource-based policies on Runtime/Memory (Mar 2026); condition keys `RuntimeAuthorizerType`, `aws:VpceOrgID`; warning: `BedrockAgentCoreFullAccess` grants `GetWorkloadAccessTokenForUserId` |
| F10 | release notes Sep 2025 – Apr 2026; A14 | | VPC for Runtime + Memory (Sep 2025), PrivateLink control plane for Gateway/Runtime/Memory/Tools (Mar 2026), VPC egress for Identity/Gateway/Runtime (Apr 2026), tagging + CloudFormation (Sep 2025) |
| F11 | https://docs.aws.amazon.com/marketplace/latest/userguide/bedrock-agentcore-gateway.html | page says "Preview" (likely stale) | Marketplace "AI Agents and Tools": API-based tools importable into Gateway |

## G. Memory

| # | Source | Date | What it says |
|---|---|---|---|
| G1 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-types.html | n.d. | Short-term events (`CreateEvent`, `ListEvents`, `ListSessions`); long-term strategies semantic, summary, user preference, episodic (Dec 2025), built-in with overrides, custom; `RetrieveMemoryRecords`; 6 strategies per memory |
| G2 | release notes Apr–Oct 2026 | | Metadata filtering (Apr), `IngestData` for non-conversational JSON + flexible namespaces (Aug), record TTL (Oct) |
| G3 | https://aws.amazon.com/about-aws/whats-new/2026/10/agentcore-memory-consumption-based-pricing/ | 6–12 Oct 2026 | Short-term per-GB pricing ($1.00/GB ingest, $0.20/GB retrieve, $0.10/GB-month) |
| G4 | https://strandsagents.com/latest/documentation/docs/community/session-managers/agentcore-memory/ | n.d. | `AgentCoreMemorySessionManager` + `AgentCoreMemoryConfig` / `RetrievalConfig`, `pip install bedrock-agentcore[strands-agents]` |
| G5 | local venv, 25 Oct 2026 | | SDK has both `MemoryClient` (create/strategies/events/retrieve) and `MemorySessionManager` (turn-oriented); both current |

## H. Observability

| # | Source | Date | What it says |
|---|---|---|---|
| H1 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html | n.d. | One-time CloudWatch Transaction Search (`aws xray update-trace-segment-destination --destination CloudWatchLogs`); `pip install aws-opentelemetry-distro>=0.18.0`; `opentelemetry-instrument python main.py`; env `AGENT_OBSERVABILITY_ENABLED`, `OTEL_PYTHON_DISTRO=aws_distro`, `OTEL_PYTHON_CONFIGURATOR=aws_configurator`, `OTEL_RESOURCE_ATTRIBUTES`, `OTEL_EXPORTER_OTLP_LOGS_HEADERS`; per-agent log group `/aws/bedrock-agentcore/runtimes/<id>-<endpoint>` (`UNIFIED_TRACES_DESTINATION_ENABLED`, Jul 2026); `DISABLE_ADOT_OBSERVABILITY` for other backends; the legacy `agent.observability.enabled` YAML key is gone |
| H2 | https://strandsagents.com/latest/documentation/docs/user-guide/observability-evaluation/traces/ | n.d. | `StrandsTelemetry().setup_otlp_exporter()` / `setup_console_exporter()`; spans agent → cycle → model → `Tool: <name>`; `gen_ai.*` attributes; `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`; Evaluations expect scope `strands.telemetry.tracer` |
| H3 | https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-observability-with-langfuse | n.d. | Langfuse as the alternative backend |
| H4 | A13 | | Observability billed at CloudWatch rates (spans $0.35/GB, logs $0.50/GB; 1 % trace-summary indexing free) |

## I. Evaluations and Optimization

| # | Source | Date | What it says |
|---|---|---|---|
| I1 | A4 | 31 Mar 2026 | Evaluations GA, 9 regions; preview Dec 2025 |
| I2 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/prompt-templates-builtin.html | n.d. | 13 built-ins: session `GoalSuccessRate` (+GT); trace `Coherence, Conciseness, Correctness (+GT), Faithfulness, Harmfulness, Helpfulness, InstructionFollowing, Refusal, ResponseRelevance, Stereotyping`; tool `ToolSelectionAccuracy, ToolParameterAccuracy`; skill evaluators `SkillSelectionAccuracy`, `SkillInstructionFollowing`; `Builtin.FailureAnalysis` Oct 2026 |
| I3 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluators.html | n.d. | Third-party DeepEval / AutoEval by id; custom LLM-as-judge (own model, instructions, schema), code-based via Lambda, derived |
| I4 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/create-online-evaluations.html | n.d. | `CreateOnlineEvaluationConfig`: log groups + serviceNames or agent endpoint; `samplingConfig.samplingPercentage` (default 10 %); ≤25 evaluators, ≤5 session filters; CLI `agentcore add online-eval --sampling-rate` |
| I5 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/on-demand-evaluations.html | n.d. | On-demand on chosen span/trace ids with ground truth |
| I6 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/results-and-output.html | n.d. | Results as OTel GenAI evaluation events (`gen_ai.evaluation.name/score`) in `/aws/bedrock-agentcore/evaluations/results/<config-id>` or the source log group; metrics `Bedrock-AgentCore/Evaluations`; console CloudWatch → GenAI Observability → agent → Evaluations tab |
| I7 | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/supported-frameworks.html | n.d. | Strands (Py/TS), LangGraph, OpenAI Agents, Vercel AI, LlamaIndex, Google ADK, Claude Agent SDK via OTel / OpenInference scope names |
| I8 | release notes Apr–Jun 2026 | | Optimization: Recommendations, A/B testing, batch evaluation, user simulation (preview 30 Apr; GA Jun 2026); Failure Insights public preview |
| I9 | https://github.com/strands-agents/evals | updated 25 Oct 2026 | `strands-agents-evals`: `Case` / `Experiment`, evaluators incl. Output, Trajectory, ToolSelectionAccuracy, ToolParameterAccuracy, GoalSuccessRate, Helpfulness, Faithfulness, Refusal, Harmfulness; `ActorSimulator`, chaos, `ExperimentGenerator`; `redteam` module present in 1.7.0 |
| I10 | https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-a-production-blueprint-with-strands-and-agentcore/ | 2026 | Strands Evals locally + AgentCore Evaluations online as one loop |
| I11 | https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html | n.d. | Bedrock Evaluations = model and RAG/KB jobs (algorithmic, human, LLM judge), not agent traces |
| I12 | A13 | | Built-in $0.0024 / $0.012 per 1K judge tokens; custom $1.50 / 1K + model cost; batch 25 % off |

## J. Knowledge

| # | Source | Date | What it says |
|---|---|---|---|
| J1 | https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-managed-knowledge-base/ | 17 Jun 2026 | Managed Knowledge Base GA: AWS-managed store/embeddings/reranker, 7 connectors (S3, SharePoint, Confluence, Web, Google Drive, OneDrive, custom), agentic multi-hop retrieval, Gateway integration; recommended default (https://docs.aws.amazon.com/bedrock/latest/userguide/kb-build-managed.html) |
| J2 | https://docs.aws.amazon.com/bedrock/latest/userguide/kb-gateway-target.html | n.d. | Managed KB as a Gateway target exposes MCP tools `Retrieve` and `AgenticRetrieveStream`; Strands via `MCPClient` + `mcp-proxy-for-aws` (SigV4) |
| J3 | https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html | n.d. | Customer-managed KB vector stores: OpenSearch Serverless/Managed, S3 Vectors (GA 2 Dec 2025), Aurora pgvector, Neptune Analytics GraphRAG, Pinecone, Redis, MongoDB Atlas; Kendra GenAI index still documented |
| J4 | https://docs.aws.amazon.com/bedrock/latest/userguide/data-source-connectors.html | n.d. | From 30 Sep 2026 new Confluence / SharePoint / Salesforce / Web connectors cannot be created on customer-managed KBs |
| J5 | https://github.com/strands-agents/tools | fetched 25 Oct 2026 | Classic `retrieve` tool deprecated → `MemoryManager` + `BedrockKnowledgeBaseStore(writable=False)` |
| J6 | https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/what-is.html | n.d. | Q Business closes to new customers 31 Jul 2026; successor Amazon Quick; Kendra maintenance mode (third-party, verify) |
| J7 | J1 pricing | | Managed KB $5/GB-month index, Retrieve $1/1K, Agentic Retrieve $4/1K; Cohere Rerank 3.5 $2/1K |

## K. Fine-tuning and model customisation

| # | Source | Date | What it says |
|---|---|---|---|
| K1 | https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html | n.d. | Methods: SFT, Reinforcement fine-tuning (Lambda or model-as-judge rewards), Distillation. **No DPO on Bedrock** (Nova Forge SDK has DPO for Nova 1.0 on SageMaker only) |
| K2 | https://docs.aws.amazon.com/bedrock/latest/userguide/custom-model-fine-tuning.html | n.d. | SFT models: Nova 2 Lite, Nova Micro/Lite/Pro, Nova Canvas, Titan Image/Embeddings, Claude 3 Haiku (us-west-2 only; EOL 10 Sep 2026 reported, verify), Llama 3.1/3.2/3.3 |
| K3 | https://docs.aws.amazon.com/bedrock/latest/userguide/rft-nova-models.html | n.d. | RFT on Nova 2 Lite (us-east-1, ≤20K prompts, one-click on-demand deploy) |
| K4 | https://docs.aws.amazon.com/bedrock/latest/userguide/fine-tuning-openai-apis.html | n.d. | gpt-oss-20b and Qwen3-32B RFT via OpenAI-compatible `bedrock-mantle` Files / Fine-tuning APIs, us-west-2 |
| K5 | https://docs.aws.amazon.com/nova/latest/userguide/fine-tune-prepare-data-understanding.html | n.d. | Nova JSONL `{"schemaVersion":"bedrock-conversation-2024","system":[{"text":...}],"messages":[{"role":"user","content":[{"text":...}]},{"role":"assistant","content":[{"text":...}]}]}`; 8–20K samples |
| K6 | https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-use.html | n.d. | Inference: Provisioned Throughput or custom model deployment for on-demand |
| K7 | https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html | n.d. | Custom Model Import (Llama 2–3.3, Mistral/Mixtral, Flan, Qwen2/2.5/3, GPT-OSS 20B/120B; <200 GB; 4 regions; per-copy billing) |
| K8 | https://aws.amazon.com/blogs/aws/introducing-amazon-nova-forge-build-your-own-frontier-models-using-nova/ and https://aws.amazon.com/blogs/aws/announcing-amazon-sagemaker-inference-for-custom-amazon-nova-models/ | Dec 2025 / Feb 2026 | Nova Forge on SageMaker; SageMaker Inference for custom Nova GA |
| K9 | https://aws.amazon.com/bedrock/pricing/ | fetched 25 Oct 2026 | Training per token × epochs; storage $1.95/model/month; RFT open-weight $80/training-hour |

## L. Local development, models, pricing

| # | Source | Date | What it says |
|---|---|---|---|
| L1 | https://strandsagents.com/latest/documentation/docs/user-guide/concepts/model-providers/ollama/ and .../llamacpp/ | n.d. | `OllamaModel(host="http://localhost:11434", model_id=...)` (`strands-agents[ollama]`), `LlamaCppModel(base_url=...)`; no Foundry Local equivalent on AWS; Nova has no open weights; no Bedrock on Outposts/Local Zones |
| L2 | C4; https://github.com/awslabs/agentcore-samples | 2026 | `agentcore dev` for local runtime; legacy `agentcore launch --local` no longer supported |
| L3 | https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html | fetched 25 Oct 2026 | Catalogue: Nova 2 Lite (GA, 1M ctx), Nova 2 Sonic / 2.5 Sonic, Nova Multimodal Embeddings (Nova 2 Pro / Omni GA not verified); Claude 5.x (Haiku 5.5 on 7 Oct 2026, Sonnet/Opus 5.5, Opus/Sonnet 5, Fable 5.1, Mythos 5.1) and 4.x; OpenAI GPT-6/5.x + gpt-oss 20b/120b; Llama 4; Gemma 3/4; DeepSeek V3.2/R1; Mistral Large 3; Qwen3; Kimi K3; MiniMax M2.5; Nemotron; Grok 4.7; GLM 5.3 |
| L4 | https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-anthropic-claude-haiku-5-5.html | Oct 2026 | Inference profiles in-Region, geo (`us.` / `eu.` / `au.` / `jp.`), global (`global.anthropic.claude-haiku-5-5`); new Claude is geo/global only; `bedrock-mantle` endpoint for OpenAI/Anthropic-native APIs |
| L5 | https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html | n.d. | `service_tier: reserved|priority|default|flex`; Priority +75 %, Flex −50 %, Batch ≈ −50 %; per-model support |
| L6 | https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html | n.d. | Intelligent Prompt Routing: default routers (Nova, Llama), configured routers via `CreatePromptRouter` with `responseQualityDifference`; $1/1K requests; English only; not for Nova 2 Lite / Claude 5.5 |
| L7 | https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html | n.d. | Most models auto-enabled on first invoke (needs `aws-marketplace:Subscribe`); Anthropic needs one-time `PutUseCaseForModelAccess`; block with SCP deny on `bedrock:InvokeModel` |
| L8 | A13 | fetched 25 Oct 2026 | Runtime V1 $0.0895/vCPU-h + $0.00945/GB-h active (no I/O-wait charge, 128 MB min); V2 $0.1276/vCPU-h + $0.0169/GB-h consumption with memory reclaimed after 120 s idle; Instances EC2 + ≈12 % fee; Gateway $0.005/1K invocations, $0.025/1K search, $0.02/100 tools indexed/month; Identity $0.010/1K tokens (free via Runtime/Gateway); Memory long-term $0.75/1K records/month, $0.50/1K retrievals; Policy $0.000025/authorization; Harness and Recommendations no separate charge |

## M. Suggested follow-ups outside this track (not done, by the user's scope rule)

- `Agent-Build-01-Fundamentals/S01.../S01.07` "Related chapters" still points to an unwritten "S03.03c AWS AgentCore"; B03 and B04 now cover it.
- `S04.09-Harness-Engineering` marks "AgentCore Policy GA 3 Mar 2026" and the `LOG_ONLY` → enforce rule as "verify"; both confirmed (F1, F3).
- `S03.05` and `S03.06` describe Cedar "on the Gateway" without dates; F1–F4 supply them.
