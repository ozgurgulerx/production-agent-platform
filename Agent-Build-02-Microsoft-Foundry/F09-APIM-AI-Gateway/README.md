# F09 — APIM AI Gateway

[Capability builds and exact checklist targets](capability-builds.md#build-contract)

Updated curriculum guidance — 30 October 2026. Scores are **unassessed**; retained labs are **not newly runtime-verified**. See the [depth and preservation contract](../reference/curriculum-mapping.md).

## Gateway learning path and policy reasoning

Treat three request paths separately: client → agent, agent → model and agent → tool. Each can have a different audience, backend identity and authorisation requirement. APIM can validate the caller and enforce limits, but the business backend remains responsible for whether that caller may perform the action.

Study policy flow in inbound, backend, outbound and error stages. First validate identity and establish consumer attribution; then enforce the budget appropriate to that consumer, select a compatible backend and authenticate the outbound call. Decide which failures can be retried. Never replay a business write merely because a gateway timeout resembles a model timeout.

For model fallback, compare model capabilities, context limits, content controls and permitted residency before choosing a second deployment. Circuit breaking protects a failing backend; it does not prove the alternate model meets quality requirements. Evaluate fallback answers independently. Cache design must isolate permission and tenant contexts; omit sensitive responses unless the cache key and lifecycle are defensible.

Learner exercise 1: author a policy for token limits, backend managed identity and an approved fallback. Identify the exact gateway tier and policy support from current documentation. Specify expected responses for invalid token, exhausted quota, unavailable backend and successful fallback. Use a bounded load exercise only after deployment is explicitly authorised.

Learner exercise 2: trace an authenticated MCP call through the gateway. Explain token audience validation, scopes, server-side authorisation and safe logging. Distinguish API catalogue discovery from runtime access control.

Completion evidence: policy explanation, request/identity diagram, failure matrix and measured token/latency/failover results once exercised. Policies and load scripts remain learner-authored. The original five-scenario notes below are retained as dated planning context, not proof of current gateway-tier capabilities.

References: local `documentation/current/apim/` backend, token-limit and MCP security articles; [backends](https://learn.microsoft.com/en-us/azure/api-management/backends), [MCP security](https://learn.microsoft.com/en-us/azure/api-management/secure-mcp-servers), [AI gateway overview](https://learn.microsoft.com/en-us/azure/ai-gateway/overview).

## Retained chapter material

The following material is preserved with its original scope and dates. Historical module-number references refer to the [migration mapping](../reference/curriculum-mapping.md#repository-preservation-and-migration-rules); current navigation uses folder links.

Agreed, and it's a good bet for the contract lane: APIM is the one Azure service that appears in bank briefs under three different headings (AI gateway, API security, integration) and it's where the "how do you govern this in production" question gets answered. The scenarios cluster into five, and you only need two of them deep.

**1. GenAI gateway in front of models.** APIM between your apps and Azure OpenAI / Foundry model deployments: token-limit and token-metric policies (`azure-openai-token-limit`, `azure-openai-emit-token-metric`), semantic caching, load-balanced backend pools with circuit breakers across regions or PTU-plus-PAYG, managed-identity auth to the backend, per-product quotas and chargeback by subscription key, content-safety policy, and the Foundry-side "AI Gateway" toggle that applies per-project TPM via a managed APIM. This is the one every Azure AI architect brief assumes; your task 161 covers it.

**2. MCP gateway.** APIM as MCP server or proxy: expose an existing REST API as MCP tools (`<api>-mcp/mcp`), or front an existing MCP server as a pass-through; Streamable HTTP, tools-only; inbound security by subscription key or `validate-azure-ad-token`, outbound credentials via credential manager (`get-authorization-context` + `set-header`), rate limits and IP restrictions per server, API Center as the private registry; and the Foundry side, where new portal-created MCP tools can be routed through APIM at creation. This is the one your S03 chapters need and the one that differentiates you — most candidates can't explain where the toolbox stops and APIM starts.

**3. Agent-facing API gateway.** APIM in front of the agent itself (prompt agent or hosted agent endpoint, or your FastAPI): JWT validation against Entra, subscription keys per client, rate limits per product, request/response logging with PII redaction, versioning and revisions, blue/green by pointing the API at the previous agent version. Task 162. This is where the review-board "how do we roll back" question lives.

**4. Classic enterprise API management.** Products, subscriptions, developer portal, policies pipeline (inbound/backend/outbound/on-error), named values and Key Vault, revisions and versions, self-hosted gateway, workspaces, v2 tiers and their networking (Standard v2 with Private Link, Premium v2 VNet-injected), monitoring and Application Insights, Defender for APIs. You need literacy, not depth: enough to read a platform team's APIM estate and know what each knob is.

**5. Integration patterns.** APIM in front of Logic Apps, Functions, Service Bus for async tools; OpenAPI tool in Foundry pointed at an APIM-fronted API with managed identity and audience; Azure Functions MCP needing APIM for OAuth. This is the glue between S03.04 tool design and D4 Azure Functions tools.

Depth target: 1 and 2 built and defensible, with the policies in your `infra/` folder and a few numbers (cache hit rate, token metrics, a 429 under quota, a failover); 3 built once as part of A3's release path; 4 and 5 at whiteboard level. The two mistakes to avoid: treating APIM as a security boundary on its own (it validates tokens and limits rates; the backend still authorises), and letting it become a study stream — it's build-and-productionise work attached to A3, about three sessions in total.

Reading in order: the APIM "AI gateway capabilities" overview and the GenAI gateway reference architecture (Azure Architecture Center), the four APIM MCP pages already in your reading map (E4–E7) plus the Foundry governance page (E1), the APIM policy reference for the GenAI and auth policies, and the `Azure-Samples/AI-Gateway` labs repo, which has runnable notebooks for almost every scenario above and is the fastest way to get evidence. I'll add an APIM section to the reading map when we next touch it; say so if you want it now.