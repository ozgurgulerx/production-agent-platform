# Foundry + Agent Framework — tools and MCP reading map (23 Oct 2026)

Full crawl of the Microsoft Learn pages on tools and MCP for Foundry Agent Service and Microsoft Agent Framework (Python pivot). ~60 pages. Dates are the page footer (ms.date where the footer differs). Word counts approximate. Stage this serves: S_AF03.01 MCP tool on Foundry, then S_AF03.02 auth, S_AF03.03 tool design, S_AF03.04 security, S_AF03.05 evals. Section H is the capability matrix (from Ozgur's separate check, corrected against the crawl).

## Read order (what to memorise vs skim)

Tier 1 — section by section, recite from memory, cards into S28 Azure AI Foundry (protocol-level facts into S03 + MCP):
1. B1 Connect agents to MCP servers
2. C1 Create and manage a toolbox + A1 What is Toolbox
3. B2 Set up authentication for MCP tools + C4 Toolbox authentication + A5 Agent identity concepts
4. F5 Hosted MCP tools + F6 Local MCP tools (Agent Framework) + F7 Foundry Toolbox integration
5. E1 Govern MCP tools with an AI gateway + E7 Secure access to MCP servers in APIM

Tier 2 — read once, keep notes:
C5 Tool search, C6 Skills, C3 Use a toolbox with a hosted agent, A3 Tool best practices, B3 Build and register an MCP server, E11/E12 Functions MCP, E14/E15 Container Apps MCP, E9 Network isolation matrix, D2 Function calling, D1 OpenAPI, F2 Function tools, F3 Tool approvals, F4 Controlling tool availability, G5/G6 Middleware, G12 Agent safety.

Tier 3 — whiteboard literacy only:
everything else below.

Interview model to carry: three execution locations for an MCP tool call — (a) Foundry Agent Service executes it (prompt agent `mcp` tool or toolbox; `mcp_approval_request` / `mcp_approval_response`; 100-s non-streaming limit; background mode for MCP tasks), (b) Agent Framework hosted marker (`get_mcp_tool`, same service-side execution), (c) Agent Framework local client (`MCPStreamableHTTPTool` / `MCPStdioTool`; your process holds the connection, identity, retries and trust boundary). Toolbox sits in front of (a) and (b) as the governed endpoint; APIM sits in front of everything as the gateway. Toolbox does not rate-limit or IP-restrict (APIM does), does not run tool code, and does not enforce `require_approval` — the consuming agent does.

## A. Foundry concepts

- A1 **What is Toolbox in Microsoft Foundry?** — https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/toolbox-overview — 2026-07-31 — ~1,230 — Build/Discover/Consume/Govern; 20-tool table of toolbox vs direct-only (function calling, Bing, computer use, image gen, SharePoint, Fabric data agent, Azure Functions are direct-only; tool search, skills, reminder are toolbox-only); versioning, Entra + OAuth passthrough, RAI policies at toolbox level.
- A2 **Types of tools in Microsoft Foundry Agent Service** — https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/tool-catalog — 2026-07-31 — ~2,650 — built-in vs custom; runtime `structured_inputs` templates for file_search / code_interpreter / mcp (server_label, server_url, headers vary per request); `MCPTool` with `project_connection_id`; `OpenApiTool` anonymous vs API key.
- A3 **Tool best practices** — https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/tool-best-practice — 2026-09-24 — ~930 — `tool_choice` auto/required/none; credential and tool-output hygiene; model + region gating.
- A4 **Build with runtime components** — https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/runtime-components — 2026-10-06 — ~5,870 — agents (name + version), conversations, responses; `background=True` poll loop; `store=False`; output item types.
- A5 **Agent identity concepts** — https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/agent-identity — 2026-08-25 — ~3,065 — agent identities as Entra service principals, blueprint + federated credential; four-stage token exchange; audience = downstream resource, not the MCP URL; shared vs published identity; role rename Azure AI → Foundry.
- A6 **Quotas and limits** — https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions — 2026-10-15 — ~4,430 — 128 tools per agent (`tool_limit_exceeded`); vector-store file limits; tool-by-region/model matrix.
- A7 **Hosted agents** — https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents — 2026-10-19 — ~3,330 — per-session VM-isolated sandboxes; tools via Toolbox MCP endpoint.

## B. Foundry MCP how-to and auth

- B1 **Connect agents to Model Context Protocol servers** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol — 2026-10-08 — ~8,390 — `mcp` tool fields: `server_url`, unique `server_label`, `allowed_tools` (default all), `require_approval` = `always` (default) / `never` / `{"never":[…]}` / `{"always":[…]}`, `project_connection_id`; six connection auth types (none, custom-keys, oauth2, user-entra-token, project-managed-identity, agentic-identity); Foundry-managed OAuth connector list; `CONSENT_REQUIRED` −32006; 100-s non-streaming timeout; background mode (preview, needs MCP tasks on the server, gpt-5.4/5.5); private MCP = Standard setup + Container Apps internal ingress on delegated subnet; hosting table Container Apps vs Functions; "Invalid tool schema" = `anyOf`/`allOf`/multi-type params; Foundry User vs Project Manager roles.
- B2 **Set up authentication for MCP tools** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication — 2026-09-04 — ~3,380 — five methods (key, Entra agent identity, Entra project MI, OAuth passthrough, unauthenticated); managed vs custom OAuth; scopes space-separated, `offline_access` for refresh; Microsoft-audience tokens cannot be passed to third-party servers; `oauth_consent_request` / `mcp_approval_request` items; Foundry Agent Consumer role; same tenant only.
- B3 **Build and register an MCP server** — https://learn.microsoft.com/en-us/azure/foundry/mcp/build-your-own-mcp-server — 2026-09-21 — ~2,230 — azd template `remote-mcp-functions-python`; endpoint `/runtime/webhooks/mcp`; `mcp_extension` system key as `x-functions-key`; register in API Center.
- B4 **Create a private tool catalog (preview)** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/private-tool-catalog — 2026-08-19 — ~850 — API Center as org MCP registry; Data Reader role; discovery in Build > Tools.
- B5 **Foundry MCP Server best practices and security** — https://learn.microsoft.com/en-us/azure/foundry/mcp/security-best-practices — 2026-08-21 — ~1,490 — the hosted Foundry MCP Server (`https://mcp.ai.azure.com`, preview, no SLA, no Private Link); Conditional Access; write-operation risks.
- B6 **Get started with Foundry MCP Server in VS Code** — https://learn.microsoft.com/en-us/azure/foundry/mcp/get-started — 2026-08-19 — ~1,060 — Entra OBO flow, Copilot agent mode.
- B7 **Available tools for Foundry MCP Server** — https://learn.microsoft.com/en-us/azure/foundry/mcp/available-tools — 2026-08-19 — ~4,385 — 79 tools, 17 categories.

## C. Foundry toolbox

- C1 **Create and manage a toolbox** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/toolbox — 2026-10-21 — ~7,530 — consumer endpoint `/toolboxes/{name}/mcp` serves `default_version`, `/versions/{v}/mcp` for testing; first version auto-promoted; one unnamed tool per type; `require_approval` enforced by the agent, not the endpoint; `rai_policy_name` guardrails; skills as `skill://{name}` resources; scope `https://ai.azure.com/.default`; `stream=True` required.
- C2 **Quickstart: toolbox with a hosted agent** — https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/quickstart-toolbox-agent — 2026-09-11 — ~2,770 — env vars, container sizing, `azure.yaml`.
- C3 **Use a toolbox with a hosted agent** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/use-toolbox-hosted-agent — 2026-09-29 — ~1,490 — `FoundryToolbox` / `AddFoundryToolboxes`, LangGraph `AzureAIProjectToolbox`; `_meta.tool_configuration.require_approval` must be enforced by the runtime; 401/403/consent troubleshooting.
- C4 **Toolbox authentication** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/tool-authentication — 2026-09-29 — ~1,890 — auth lives on the connection (six `authType` values); `--kind remote-tool` vs `remote-a2a`; `x-agent-foundry-call-id` must be forwarded; Foundry Agent Consumer role; same tenant.
- C5 **Enable tool search in a toolbox** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/tool-search — 2026-08-19 — ~3,010 — `{"type":"toolbox_search"}`; meta-tools `tool_search` (limit 5 default, 10 max) and `call_tool`; BM25 over name/description/params; `tool_configs` pin / `additional_search_text` / `"*"`; auto-pin per user; recommended at 10+ tools. (Foundry's answer to S03.05.)
- C6 **Use skills in Foundry (preview)** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/skills — 2026-10-15 — ~4,540 — versioned immutable `SKILL.md`; exposed as MCP Resources (SEP-2640); `Foundry-Features: Skills=V1Preview` header; same project only.
- C7 **Network isolation for a toolbox** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/toolbox-network-isolation — 2026-08-15 — ~570 — toolbox inherits project networking; MCP/OpenAPI/A2A via delegated subnet.
- C8 **Reminder tool** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/reminder-tool — 2026-07-22 — ~1,080 — toolbox-only, hosted agents only.

## D. Other Foundry tool types

- D1 **OpenAPI tools** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/openapi — 2026-08-21 — ~7,480 — auth `anonymous` / `connection` / `managed_identity` (+ `audience`); one API-key scheme per tool; JSON bodies only.
- D2 **Function calling** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/function-calling — 2026-10-14 — ~3,370 — Responses loop `function_call` → `function_call_output` by `call_id`; 10-minute run expiry; `strict: true`. (Client-side execution — the contrast with MCP.)
- D3 **A2A agent endpoint** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/agent-to-agent — 2026-09-14 — ~4,670 — `a2a` (1.0 GA) vs `a2a_preview`; Foundry target URL and audience; Connected Agents replaced by A2A/workflows.
- D4 **Azure Functions tool** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/azure-functions — 2026-08-24 — ~3,985 — queue-trigger pattern, Standard setup only.
- D5 **Web search tool** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/web-search — 2026-09-11 — ~5,700 — `WebSearchTool` vs `WebSearchToolboxTool`; Bing data outside the Azure compliance boundary.

## E. Governance, networking, hosting

- E1 **Govern MCP tools by using an AI gateway (preview)** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/governance — 2026-08-19 — ~1,210 — APIM routing only for new portal-created MCP tools without managed OAuth, applied at creation; gateway URL `*.azure-api.net/mcp/...`; `rate-limit-by-key`, 429/403, `X-RateLimit-Remaining`; no tool traces logged.
- E2 **Configure AI Gateway in Foundry resources** — https://learn.microsoft.com/en-us/azure/foundry/configuration/enable-ai-api-management-gateway-portal — 2026-08-06 — ~1,780 — per-resource APIM, per-project TPM/quota.
- E3 **Bring your own model** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/ai-gateway — 2026-08-13 — ~2,800 — BYOM, not MCP governance (slug is misleading).
- E4 **About MCP servers in API Management** — https://learn.microsoft.com/en-us/azure/api-management/mcp-server-overview — 2026-10-20 — ~1,200 — tiers; Streamable HTTP `/mcp`, SSE deprecated; tools only.
- E5 **Expose REST API as an MCP server (APIM)** — https://learn.microsoft.com/en-us/azure/api-management/export-rest-mcp-server — 2026-04-30 — ~1,330 — `https://<apim>.azure-api.net/<api>-mcp/mcp`; streaming caveats.
- E6 **Expose and govern an existing MCP server (APIM)** — https://learn.microsoft.com/en-us/azure/api-management/expose-existing-mcp-server — 2026-04-30 — ~1,400 — pass-through; MCP 2025-06-18+.
- E7 **Secure access to MCP servers in APIM** — https://learn.microsoft.com/en-us/azure/api-management/secure-mcp-servers — 2026-09-11 — ~570 — inbound subscription key or `validate-azure-ad-token`; outbound credential manager `get-authorization-context` + `set-header`.
- E8 **Register and discover MCP servers (API Center)** — https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server — 2026-06-02 — ~1,740.
- E9 **Configure network isolation for Foundry** — https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link — 2026-09-29 — ~4,300 — "Agent tools with network isolation" matrix (private MCP via subnet; which tools are unsupported isolated).
- E10 **Set up private networking for Foundry Agent Service** — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/virtual-networks — 2026-08-27 — ~4,815 — agent subnet delegated to `Microsoft.App/environments`, /24 recommended.
- E11 **Connect an MCP server on Azure Functions to Foundry** — https://learn.microsoft.com/en-us/azure/azure-functions/functions-mcp-foundry-tools — 2026-06-03 — ~2,230.
- E12 **MCP bindings for Azure Functions** — https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-mcp — 2026-08-25 — ~1,110 — tool/resource/prompt triggers; `host.json extensions.mcp`.
- E13 **Choose an Azure service for your MCP server** — https://learn.microsoft.com/en-us/azure/container-apps/mcp-choosing-azure-service — 2026-06-02 — ~1,600 — Container Apps default; App Service; Functions; AKS.
- E14 **Host MCP servers on Container Apps** — https://learn.microsoft.com/en-us/azure/container-apps/mcp-overview — 2026-02-27 — ~1,080.
- E15 **Agent Service networking deep dive** — https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/agents-networking-deep-dive — 2026-09-08 — ~2,150 — single-tenant data proxy for all tool egress.
- E16 **App Service built-in MCP authorization (preview)** — https://learn.microsoft.com/en-us/azure/app-service/configure-authentication-mcp — 2025-11-05 — ~690 — PRM metadata; Entra lacks DCR so pre-register clients; prefer OBO over pass-through.

## F. Agent Framework tools and MCP (Python)

- F1 **Tools overview** — https://learn.microsoft.com/en-us/agent-framework/agents/tools/ — 2026-09-29 — ~1,830 — tool type index; provider support matrices.
- F2 **Function tools** — https://learn.microsoft.com/en-us/agent-framework/agents/tools/function-tools — 2026-09-20 — ~2,600 — `@tool(name, description, schema, approval_mode, result_parser)`; `function_invocation_configuration` (`max_iterations`, `max_function_calls`, `max_duration_seconds`, `allow_concurrent_invocation`).
- F3 **Function tools with human-in-the-loop approvals** — https://learn.microsoft.com/en-us/agent-framework/agents/tools/tool-approval — 2026-09-28 — ~2,300 — `approval_mode` always_require / never_require; `result.user_input_requests`; `to_function_approval_response(True|False)` re-run on the same session.
- F4 **Controlling tool availability** — https://learn.microsoft.com/en-us/agent-framework/agents/tools/controlling-tool-availability — 2026-08-25 — ~1,300 — `tool_choice`; `ctx.add_tools()` / `remove_tools()`.
- F5 **Hosted MCP tools** — https://learn.microsoft.com/en-us/agent-framework/agents/tools/hosted-mcp-tools — 2026-08-25 — ~1,530 — `client.get_mcp_tool(name, url, headers, approval_mode, allowed_tools)`; `allowed_tools` None vs `[]` vs names; service-executed.
- F6 **Local MCP tools** — https://learn.microsoft.com/en-us/agent-framework/agents/tools/local-mcp-tools — 2026-09-28 — ~2,565 — `MCPStdioTool`, `MCPStreamableHTTPTool`, `MCPWebsocketTool`; `header_provider`, `static_headers`, `allowed_tools`, `approval_mode`, `tool_name_prefix`, `max_host_payload_size_bytes`; `as_mcp_server()` to expose an agent; sampling deprecated (removal by 2027-07-28).
- F7 **Foundry Toolbox integration** — https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/tools/foundry-toolbox — 2026-09-29 — ~1,225 — `FoundryToolbox` (beta); `as_skills_provider()`; env vars.
- F8 **Shell tools** — https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/tools/shell-tools — 2026-10-15 — ~2,170 — `LocalShellTool`, `DockerShellTool`, `ShellPolicy`.
- F9 **Microsoft Foundry model provider** — https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/model-providers/microsoft-foundry — 2026-10-06 — ~2,450 — `FoundryChatClient` factories `get_mcp_tool()`, `get_a2a_tool()` etc.
- F10 **Foundry Agent Service integration** — https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/agent-services/foundry — 2026-08-10 — ~1,335 — `FoundryAgent` binds to the server-side definition: hosted tools incl. MCP must be on the Foundry definition.
- F11 **A2A agent service** — https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/agent-services/a2a — 2026-10-15 — ~2,245.
- F12 **Agent skills** — https://learn.microsoft.com/en-us/agent-framework/agents/skills — 2026-08-25 — ~9,680 — `SkillsProvider`; `MCPSkillsSource` reads `skill://index.json`.

## G. Agent Framework surrounding concepts

- G1 **Overview** — https://learn.microsoft.com/en-us/agent-framework/overview/ — 2026-08-25 — ~900.
- G2 **Agent concepts** — https://learn.microsoft.com/en-us/agent-framework/concepts/agents/ — 2026-08-10 — ~340.
- G3 **Running agents** — https://learn.microsoft.com/en-us/agent-framework/concepts/agents/running-agents — 2026-10-15 — ~2,380 — `run(stream=True)`, `AgentResponse`.
- G4 **Agent pipeline architecture** — https://learn.microsoft.com/en-us/agent-framework/concepts/agents/agent-pipeline — 2026-08-25 — ~1,630 — middleware → telemetry → RawAgent → ChatClient function-invocation loop.
- G5 **Agent middleware** — https://learn.microsoft.com/en-us/agent-framework/concepts/agents/middleware/ — 2026-08-25 — ~3,600 — agent / function / chat middleware. (Where S03.06 defences live in this stack.)
- G6 **Adding middleware** — https://learn.microsoft.com/en-us/agent-framework/concepts/agents/middleware/defining-middleware — 2026-08-25 — ~2,575.
- G7 **Agent hooks** — https://learn.microsoft.com/en-us/agent-framework/agents/agent-hooks — 2026-09-03 — ~2,070 — `pre_tool_call` / `post_tool_call`, fail-closed.
- G8 **Session** — https://learn.microsoft.com/en-us/agent-framework/concepts/agents/conversations/session — 2026-08-25 — ~870.
- G9 **Storage** — https://learn.microsoft.com/en-us/agent-framework/concepts/agents/conversations/storage — 2026-10-15 — ~2,420.
- G10 **Context providers** — https://learn.microsoft.com/en-us/agent-framework/concepts/agents/conversations/context-providers — 2026-09-09 — ~2,350 — `extend_tools(source_id, tools)`.
- G11 **Compaction** — https://learn.microsoft.com/en-us/agent-framework/concepts/agents/conversations/compaction — 2026-08-25 — ~2,750.
- G12 **Agent safety** — https://learn.microsoft.com/en-us/agent-framework/concepts/agents/safety — 2026-08-25 — ~1,000 — tools run without approval by default.
- G13 **Agent security with FIDES** — https://learn.microsoft.com/en-us/agent-framework/agents/security — 2026-08-25 — ~3,450 — information-flow labels; `SecureAgentConfig`; `accepts_untrusted`.
- G14 **Agent harness** — https://learn.microsoft.com/en-us/agent-framework/concepts/harness — 2026-09-21 — ~1,100 — `create_harness_agent(...)`. (S04 harnesses chapter.)
- G15 **Foundry hosted agents** — https://learn.microsoft.com/en-us/agent-framework/hosting/foundry-hosted-agent — 2026-10-16 — ~3,675.
- G16 **Self-host A2A agents** — https://learn.microsoft.com/en-us/agent-framework/hosting/self-hosting/a2a/ — 2026-08-25 — ~1,620.
- G17 **Integrations index** — https://learn.microsoft.com/en-us/agent-framework/integrations/ — 2026-10-09 — ~200.

## H. Capability matrix (from Ozgur's 23 Oct check, corrected against the crawl)

"Hosted MCP" means Foundry invokes the remote server; it does not host your server's code. Preview labels as documented; availability varies by model, region, SDK and agent type.

Foundry Agent Service — built-in and hosted tools: web search (D5), file search, code interpreter, Azure AI Search, OpenAPI (D1), Grounding with Bing (direct only), image generation (direct only), SharePoint (direct only), Fabric data agent (direct only), Fabric IQ (preview), Work IQ (preview), browser automation (preview, Azure Playwright), computer use (preview; app executes the actions), Azure Functions (D4, direct only, Standard setup), custom function calling (D2, client executes), A2A tools (D3), memory search (preview, framework integration), reminder tool (C8, hosted agents only).

Foundry Agent Service — MCP: remote MCP invocation (B1); multiple servers per agent (unique `server_label`); `allowed_tools` allow-list; approval workflow (`require_approval`, `mcp_approval_request` → `mcp_approval_response` with `previous_response_id`) — enforced by the consuming agent runtime, not by the toolbox endpoint; custom-header auth (`custom-keys` connection); OAuth (Foundry-managed connector app for a short partner list, or own app registration; `CONSENT_REQUIRED` −32006 on first use); user Entra identity passthrough (`user-entra-token` + audience); project managed identity; agentic identity (A5); private MCP endpoints (Standard setup + BYO VNet + Container Apps internal ingress on the delegated subnet); background MCP operations (preview; only if the server implements MCP tasks and returns the related-task id, and the model supports background mode — otherwise the 100-s synchronous limit applies); MCP tasks on toolbox endpoints (preview; consuming harness must support tasks).

Foundry toolbox: single managed MCP-compatible endpoint; versioning with promote-to-default (consumer vs version-specific endpoint); centralised credential injection and token refresh; guardrails (`rai_policy_name`) on tool inputs and outputs; tool search (preview: `tool_search` + `call_tool`, BM25, explicit pin, auto-pin per user, `additional_search_text`); skills (preview; versioned `SKILL.md` delivered as MCP resources); tool-call observability (tracing, Application Insights).

Governance and catalogue (missing from the original list): APIM AI gateway in front of MCP tools (E1: rate limits, IP restriction, policies; E7: `validate-azure-ad-token` inbound, credential manager outbound); private tool catalogue via API Center (B4, E8); network-isolation matrix per tool type (E9).

Agent Framework — a separate execution layer, not automatic Foundry hosting: local MCP client (F6: `MCPStreamableHTTPTool` / `MCPStdioTool` / `MCPWebsocketTool`; your process connects and invokes); hosted MCP marker (F5: `get_mcp_tool`; looks local in code, executes service-side — missing from the original list and the usual interview trap); local function execution (F2); framework tool approvals (F3; gate locally invoked tools, hosted calls follow the provider's approval rules); local and Docker shell tools (F8; your environment, not Foundry); hosted custom agent runtime (G15; deploy a framework agent to Foundry for managed hosting).

Protocol boundary (confirmed): the Foundry MCP tool consumes tools and the approval loop; the Foundry MCP guide does not claim sampling, elicitation or prompts; APIM MCP servers expose tools only (E4); toolbox exposes tools plus resources used for skills; Agent Framework's local client has deprecated MCP sampling (removal by 2027-07-28). Honest one-liner: Foundry is a tools-only MCP client with a managed approval loop, not a full MCP host.

## Linked, not yet fetched

- Tool search with the Azure OpenAI Responses API — https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/tool-search
- Networking options for Agent Service — https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/networking-options
- Standard agent setup — https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/standard-agent-setup
- Deploy a hosted agent — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/deploy-hosted-agent
- Add a connection — https://learn.microsoft.com/en-us/azure/foundry/how-to/connections-add
- Functions MCP tutorial — https://learn.microsoft.com/en-us/azure/azure-functions/functions-mcp-tutorial
- Register Functions MCP servers in API Center — https://learn.microsoft.com/en-us/azure/azure-functions/register-mcp-server-api-center
- APIM: manage MCP servers via REST — https://learn.microsoft.com/en-us/azure/api-management/manage-mcp-servers-rest-api; monitor MCP traffic — https://learn.microsoft.com/en-us/azure/api-management/monitor-mcp-servers; validate-azure-ad-token — https://learn.microsoft.com/en-us/azure/api-management/validate-azure-ad-token-policy; credential manager — https://learn.microsoft.com/en-us/azure/api-management/credentials-overview
- Container Apps MCP tutorial (Python) — https://learn.microsoft.com/en-us/azure/container-apps/tutorial-mcp-server-python
- Agent Framework: runtime context — https://learn.microsoft.com/en-us/agent-framework/concepts/agents/middleware/runtime-context; background responses — https://learn.microsoft.com/en-us/agent-framework/agents/background-responses; observability — https://learn.microsoft.com/en-us/agent-framework/agents/observability; durable extension — https://learn.microsoft.com/en-us/agent-framework/hosting/durable-extension; Purview middleware — https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/middleware/purview
- Memory search (preview) — not yet located in the crawl; verify the Foundry memory store page before citing.

Notes: `/agents/how-to/ai-gateway` is BYOM, not MCP governance — the governance page is `/agents/how-to/tools/governance`. Several pages disagree between ms.date, footer and meta-updated_at; footer used where they differ.
