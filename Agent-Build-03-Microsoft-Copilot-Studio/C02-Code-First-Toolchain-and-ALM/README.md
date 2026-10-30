# C02 — The Copilot Studio toolchain: Dataverse objects, pac, the Power Platform API and ALM

Copilot Studio looks like a portal, and most people meet it as one. Underneath, every agent is a set of rows in Dataverse, every tool is a connector, and every release is a solution import. **The code-first path is not an alternative to the portal; it is the same objects reached through `pac`, the VS Code extension, the Power Platform API and the Agents SDK, which is what makes them reviewable, testable and repeatable.** This chapter maps those surfaces, the way F02 maps `azure-ai-projects` + `azd` + Bicep and B02 maps boto3 + the AgentCore CLI + CDK.

> _If it is not in a solution in Git, it is a demo._

Running scenario: the UK support-ticket agent. Facts come from the reading map [`../reference/reading-map-copilot-studio-2026-10-25.md`](../reference/reading-map-copilot-studio-2026-10-25.md); letters such as C1 or K6 refer to it. Status words are GA, preview and retiring, with dates. The labs live under `../labs-setup/` and the chapter folders; nothing in them had run on 25 Oct 2026.

## 1. Learning outcomes and study depth

By the end of C02, you should be able to:

- Distinguish tenant and environment configuration, agent objects in Dataverse, the runtime APIs a client calls, and the automation that moves a solution between environments.
- Pick the right surface for an operation: portal, `pac copilot`, VS Code extension, Power Platform API, Dataverse Web API, Direct-to-Engine, Direct Line.
- Read the YAML the VS Code extension or `pac copilot clone` produces and say which parts travel in a solution and which do not.
- Explain a release pipeline with an evaluation gate, a publish step and a rollback by solution version.
- Estimate the credits one conversation costs and name the enforcement thresholds.
- Diagnose a failed call by its auth mode, connector policy, environment and harness.

| Depth                           | Topics                                                                                                                                                            | Expected ability                                                            |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **Practice now**                | `pac copilot` clone / pull / push / pack / publish, the VS Code extension, Direct-to-Engine with `microsoft-agents-copilotstudio-client`, the evaluation REST API | Run each once, adapt configuration, explain each step.                      |
| **Understand and demonstrate**  | Solutions, connection references, environment variables, Power Platform Pipelines, credits, harness choice                                                        | Trace a release from Git to a verified publish and name the failure points. |
| **Read and recognise**          | Dataverse `bot` / `botcomponent`, Git integration, Agents SDK hosting, Agent 365 registration                                                                     | Explain their purpose and when a platform team would require them.          |
| **Defer deeper implementation** | Custom connectors at scale, the Customer Conversation harness, Apps in Copilot Studio, Managed Runtime                                                            | Study when a workload needs them; not prerequisites for the first agent.    |

The core automation path here is **`pac copilot` plus the Power Platform API from Python**, with the VS Code extension for day-to-day editing. Power Platform Pipelines literacy is useful; building a CoE pipeline estate is outside this stage.

## 2. Prerequisites

- A Microsoft 365 tenant with Copilot Studio credits (a pack or pay-as-you-go through Azure) and admin rights for the C09 labs (K5).
- A **Managed Environment** in the UK region (`crm11`), because environment groups, environment-level telemetry and CMK need one (F2, H2, F9).
- Power Platform CLI: `dotnet tool install --global Microsoft.PowerApps.CLI.Tool` then `pac auth create --deviceCode` (C1). No `pac` is installed on this machine on 25 Oct 2026.
- The Copilot Studio VS Code extension (GA Jan 2026) (C2).
- Python 3.13 venv from `../labs-setup/requirements.txt`: `microsoft-agents-copilotstudio-client` 1.9.0, `microsoft-agents-hosting-aiohttp` 1.9.0, `microsoft-agents-authentication-msal` 1.9.0, `msal` 1.39.0, `httpx`, `pyyaml` (C9).
- A **public-client app registration** with device code enabled and delegated permissions: Power Platform API `CopilotStudio.Copilots.Invoke`, Dynamics CRM `user_impersonation`, Microsoft Graph `Application.Read.All`; admin consent granted. No client secret anywhere (C8, I3).
- `.env` at the track root with `TENANT_ID`, `CLIENT_ID`, `ENVIRONMENT_ID`, `ENVIRONMENT_URL`, `AGENT_SCHEMA_NAME` (see `../.env.example`).

## 3. Understand the three layers

| Layer                  | What it is                                                                                                                                | Surfaces                                                                 |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Models you pick        | The primary model dropdown, the generative-responses model, prompt-tool models; nothing to deploy                                         | Portal, agent YAML (K1, K2)                                              |
| Agent objects          | Rows in Dataverse (`bot`, `botcomponent`), connection references, environment variables, custom connectors, flows, packaged in a solution | Portal, `pac copilot`, VS Code extension, Dataverse Web API (C1, C2, C3) |
| Automation and runtime | Solution import / export, Pipelines, Git, the Power Platform API (`copilotstudio` namespace), Direct-to-Engine, Direct Line               | `pac`, GitHub Actions, Python (C5, C6, C7–C10)                           |

### Model selection, the decisions behind the dropdown

There is no deployment object. The Standard harness picks a **primary model** from a curated list that defaults to "GPT Chat Latest", a moving pointer to the current GPT chat snapshot; GA options on 22 Oct 2026 include GPT-5.5 Chat, Claude Sonnet 4.6 and Claude Opus 4.6 to 4.8 (K1). The GitHub harness list adds GPT-6 Astra, Claude Sonnet 5, Claude Fable 5 / 5.1 and Opus 5 (K2). Three decisions matter: whether to pin a model or follow "GPT Chat Latest" through the retirement wave (GPT-5.3 / 5.4 on 15 Oct, GPT-5.5 Chat on 31 Oct, GPT-4.1 and the GPT-5 family on 12 Nov 2026, all remapped to GPT Chat Latest); whether the tenant admin has accepted external-provider terms for Anthropic, Mistral or xAI (K3); and whether a Prompt tool should run on your own Foundry chat-completions deployment, which is the only bring-your-own-model door and excludes the GPT-5 family and Responses-API endpoints (K4). There is no fine-tuning feature and no BYO model for the orchestrator. `../labs-setup/01-models/` reads these settings back from the agent definition so you can see what a portal click changed.

### Agent objects in Dataverse

An agent is a `bot` row; topics, knowledge references, tools, triggers and settings are `botcomponent` rows; a solution carries them together with connection references and environment variables (C3, C6). Three facts shape every pipeline:

- **Harness is a property of the agent** (A1). Standard-harness agents carry topics; GitHub-harness agents carry instructions, skills, hooks and workflows. The code-first tools cover the Standard harness fully; Direct-to-Engine does not yet officially support the GitHub harness (C8).
- **Not everything is ALM-portable.** Uploaded files, OneDrive and SharePoint uploads, and connector-ingested knowledge (Salesforce, ServiceNow) do not re-ingest on import; the SharePoint connector reference and Dataverse tables do (C4). Reattach knowledge per environment and say so in the runbook.
- **Connections are per environment.** Connection references resolve to connections owned by a maker or a service account in each environment; the tool's credentials mode (end-user vs maker) is set on the tool, not the connection (D1).

### Automation surfaces

`pac copilot` verbs (C1):

| Verb                                        | What it does                                                                                                                                         | When                           |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| `init`                                      | Scaffold a local agent folder, or bootstrap an agent in an environment with `--environment`; `--authoring-mode cli-copilot` for CLI-driven authoring | New agent                      |
| `clone`                                     | Pull an existing agent's definition into a local folder as YAML                                                                                      | Bring a portal agent under Git |
| `pull` / `push`                             | Three-way merge between local, last-synced and environment; a conflict stops `push`; `push` carries knowledge files, flows and connection references | Daily loop                     |
| `pack`                                      | Build the solution locally without authentication, "safe to run in a build pipeline"                                                                 | CI build                       |
| `publish`                                   | Publish the agent across its channels                                                                                                                | Release                        |
| `create` / `extract-template`               | Create from, or extract to, a YAML template                                                                                                          | Templates                      |
| `extract-translation` / `merge-translation` | Localisation round-trip                                                                                                                              | Multi-language                 |
| `list`, `status`, `delete`, `quarantine`    | Inventory and admin actions                                                                                                                          | Operations                     |
| `mcp --run`                                 | Run a local MCP server that exposes `pac` to a coding agent                                                                                          | Dev loop (C07)                 |
| `model list` / `predict`                    | AI Builder model helpers                                                                                                                             | Prompts                        |

The **VS Code extension** (GA Jan 2026) clones the whole agent as YAML with IntelliSense and sync/apply, and is pitched for editing with coding agents (C2). The **Power Platform API** `copilotstudio` namespace exposes bots, the evaluation test sets and runs (`.../environments/{env}/bots/{bot}/api/makerevaluation/testsets|testruns?api-version=2024-10-01`, preview) and the quarantine action (`botQuarantine/SetAsQuarantined`) (C6, I3, F5). The **Dataverse Web API** reads `bot`, `botcomponent` and `ConversationTranscript` (G4). At runtime a client talks **Direct-to-Engine** through the Agents SDK client with a delegated `CopilotStudio.Copilots.Invoke` token (C7–C9) or **Direct Line** through the token endpoint (C10). Release automation is **Power Platform Pipelines** or `pac solution import` from GitHub Actions with Entra federated credentials, and **Git integration** for environments that have it (C5).

Minimal Direct-to-Engine shape (C9, from the installed package):

```python
settings = ConnectionSettings(environment_id=ENV, agent_identifier=SCHEMA, cloud=PowerPlatformCloud.PROD)
client = CopilotClient(settings, token)            # token: MSAL device-code, scope CopilotStudio.Copilots.Invoke
async for a in client.start_conversation(): ...   # yields Activity objects
async for a in client.ask_question("My card was charged twice."): print(a.text)
```

## 4. Study sequence

### Step 1 — Map tenant, environment, agent and identifiers

Record `TENANT_ID`, `ENVIRONMENT_ID`, `ENVIRONMENT_URL`, the agent's schema name (Settings → Advanced → Metadata) and its `bot` id. Proof: `../labs-setup/00-setup/scripts/verify.sh` prints OK.

### Step 2 — Choose the client and authenticate

Device-code sign-in through the public-client app for Python; `pac auth create --deviceCode` for the CLI; Authenticate with Microsoft for end users in Teams. No secrets in files. Proof: a two-turn Direct-to-Engine conversation (`../C03-Creating-Agents-in-Copilot-Studio/labs/01-ticket-agent-two-ways/`).

### Step 3 — Bring the agent under Git

`pac copilot clone`, commit the YAML, change the instructions in a branch, `pac copilot push`, `publish`. Proof: the diff in Git and the new answer in the test pane.

### Step 4 — Govern the tools

Add the ticket MCP server through the wizard, then through a custom connector with `x-ms-agentic-protocol: mcp-streamable-1.0`; see the DLP classification and the allow-list (`../C04-Tools-Identity-MCP-and-Connected-Agents/labs/02-mcp-tool/`).

### Step 5 — Automate release with a gate

`pac copilot pack` in CI → `pac solution import` to test → evaluation test set through the REST API with a pass-rate threshold (`../C05-Evaluation-Observability-and-Safety/labs/01-evaluation/`) → import to production → `pac copilot publish`. Rollback: import the previous solution version and publish. Governance evidence from `../C09-Governance-and-Agent-365/labs/01-inventory-and-quarantine/`.

## 5. Production concerns to understand

| Concern           | What to study                                                                                                                                  | Question you should be able to answer                                  |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Identity          | Entra Agent ID per agent, connector scopes on publish, end-user vs maker credentials, auth modes (E1, E5, D1)                                  | Whose token reaches the ticket server, and who could change that?      |
| Policy reach      | DLP virtual connectors, ACP, environment group rules (F1, F2)                                                                                  | Which control stops a new HTTP tool, and when does the maker find out? |
| Publish semantics | Publish is agent-wide; new content reaches new sessions after about 30 min of inactivity or "start over" (L1)                                  | Why does a user still see the old answer ten minutes after publish?    |
| Limits            | 128 tools per agent, 25–30 recommended; 500 knowledge objects; 25-source generative filter; evaluation sets ≤100 / ≤20 cases (D1, J1, I2)      | What breaks first as the agent grows?                                  |
| Observability     | Transcripts 30 days by default in Dataverse; env-level OpenTelemetry export needs a Managed Environment; agent-level App Insights (G4, H2, H3) | Can I trace a failed tool call without storing content I should not?   |
| Models            | Retirement dates and the "GPT Chat Latest" pointer; external-provider consent (K1, K3)                                                         | What changes on 12 Nov 2026 if I did nothing?                          |
| Cost              | Credits table below; enforcement at 100 % for flows and 125 % for agents; per-agent caps (K6)                                                  | How much is one conversation, and what happens when the pack runs out? |
| Harness           | Standard vs GitHub harness: billing, channels, code-first support (A1, L2, C8)                                                                 | Which harness does the bank's pipeline support today?                  |

Copilot Credits (renamed from messages on 1 Sep 2025; K5, K6, K7):

| Item                                                                                   | Credits                                                                                                  |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Classic answer                                                                         | 1                                                                                                        |
| Generative answer                                                                      | 2                                                                                                        |
| Agent action (tool call, trigger, deep reasoning, topic transition, computer-use step) | 5 (computer use 5–15 per step by model)                                                                  |
| Tenant graph grounding                                                                 | 10                                                                                                       |
| Agent-flow actions                                                                     | 13 per 100                                                                                               |
| AI tools (prompts)                                                                     | basic 1 / standard 15 / premium 100 per 10 responses                                                     |
| Content processing                                                                     | 8 per page                                                                                               |
| Voice                                                                                  | 10 / 35 / 75 per minute                                                                                  |
| Prepaid pack                                                                           | 25,000 credits for about USD 200 per month; PAYG per credit (USD 0.01 reported by third parties, verify) |
| Microsoft 365 Copilot licensed users (B2E)                                             | no charge for most items                                                                                 |

Cost of one session, as an interview answer: a support conversation with two generative answers (4), one MCP tool call (5) and one refund-approval flow action (0.13), tenant grounding off, costs about 9 credits, roughly USD 0.07 at pack price. A thousand such conversations a day consume a pack in under three days; the environment's agents are disabled at 125 % of the pack, so the cap is the control, not the invoice.

## 6. Completion checklist

- [ ] Explain the three layers and classify a new operation by surface and permission.
- [ ] Run `verify.sh` and `../labs-setup/01-models/read_primary_model.py`; explain the primary model and the retirement pointer.
- [ ] Clone the ticket agent to YAML, change one instruction in a branch, push and publish; show the diff.
- [ ] Hold a two-turn Direct-to-Engine conversation from Python with a device-code token.
- [ ] Pack the solution without a tenant connection and import it to a second environment; reattach knowledge.
- [ ] Run an evaluation test set through the REST API and show a failing threshold blocking the import.
- [ ] Name which identity each step used: maker, service account, end user, agent identity.
- [ ] Estimate the credits of one conversation and state the two enforcement thresholds.

A useful final sentence: "The agent is rows in Dataverse inside a solution; I edit it as YAML in Git, build with `pac copilot pack`, import through a pipeline, gate on the evaluation API, publish with `pac copilot publish`, and call it from code through Direct-to-Engine with a delegated token."

## 7. Same thing on Foundry and AgentCore

| Copilot Studio                                                  | Foundry (F02)                                                | AgentCore (B02)                                        |
| --------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------ |
| Model dropdown, "GPT Chat Latest" pointer, no deployment object | Model deployment (`GlobalStandard`, `DataZoneStandard`, PTU) | Inference profile + service tier, no deployment object |
| `bot` / `botcomponent` rows in a solution                       | Agent versions in the project                                | Runtime versions + named endpoints                     |
| `pac copilot` + VS Code YAML + solution zip                     | `azd` + `azure.yaml` + Bicep                                 | AgentCore CLI 1.0 + `agentcore.json` + CDK app         |
| Power Platform API `copilotstudio` + Dataverse Web API          | `azure-ai-projects` project client                           | `bedrock-agentcore-control` / `bedrock-agentcore`      |
| Direct-to-Engine (`CopilotClient`) / Direct Line                | OpenAI-compatible `responses` client                         | `invoke_agent_runtime`                                 |
| Entra Agent ID by blueprint, no BYO app                         | Agent identity (Entra, visible)                              | Workload identity + execution role                     |
| Power Platform Pipelines / Git integration, OIDC `azure/login`  | GitHub Actions with federated credentials                    | GitHub OIDC with `configure-aws-credentials`           |
| Evaluation REST API as the gate                                 | `azd ai agent eval run` / evals API                          | Strands Evals + on-demand evaluation                   |
| Credits with 100 % / 125 % enforcement                          | Token quota (TPM)                                            | Per-second consumption, no cut-off                     |
| GitHub harness replaces topics with hooks and skills            | Declarative workflows retiring 1 Dec 2026                    | Classic Bedrock Agents in maintenance mode             |

## 8. Reference reading

1. `pac copilot` reference (C1): https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/copilot
2. Copilot Studio VS Code extension (C2): https://learn.microsoft.com/en-us/microsoft-copilot-studio/visual-studio-code-extension-overview
3. Solutions in Copilot Studio (C3): https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-solutions-overview
4. Quotas and ALM limits (C4): https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-quotas
5. Power Platform API, `copilotstudio` namespace (C6): https://learn.microsoft.com/en-us/rest/api/power-platform/copilotstudio/bots
6. Integrate with the Agents SDK, Direct-to-Engine (C7, C8): https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-integrate-web-or-native-app-m365-agents-sdk
7. Evaluation REST API (I3): https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-agent-evaluation-rest-api
8. Primary model selection and retirements (K1): https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-select-agent-model
9. Billing and credits (K5, K6): https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management
10. Harnesses overview (A1): https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview

Local ground truth: the `microsoft-agents-*` 1.9.0 signatures inspected in `../labs-setup/.venv` on 25 Oct 2026 (C9). Pages checked on **25 Oct 2026**. Not verified: the PAYG per-credit rate, Git-integration fidelity for `botcomponent` rows, whether a portal click is still needed before a first export in a pipeline, and the test-set case limits.
