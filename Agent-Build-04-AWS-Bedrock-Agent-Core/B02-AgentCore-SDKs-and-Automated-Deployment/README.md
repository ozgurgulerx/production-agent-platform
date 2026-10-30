# B02 — AgentCore SDKs and automated deployment

Learn how to move from an AWS account to a repeatable, keyless deployment of an agent on Amazon Bedrock AgentCore. The central skill is knowing **what you are deploying, which API plane or tool owns it, and how you verify the result**.

> _IaC for accounts and network; the control plane for AgentCore objects; the framework for the loop._

This stage covers platform setup, SDK boundaries and release automation. Agent design belongs in [B03 — Creating agents on AgentCore](../B03-Creating-Agents-on-AgentCore/README.md); tools, identity and MCP in [B04](../B04-AgentCore-Tooling-Identity-and-MCP/README.md). It is the mirror of the Foundry F02 chapter. Facts are dated in [`../reference/reading-map-agentcore-2026-10-25.md`](../reference/reading-map-agentcore-2026-10-25.md); letters such as C2 or L8 refer to it. Nothing here has run against AWS yet (25 Oct 2026).

## 1. Learning outcomes and study depth

By the end of B02, you should be able to:

- Distinguish account and network provisioning, AgentCore control-plane operations, data-plane invocations, model inference, and application code deployment.
- Select the right client, endpoint, identity and permission scope for an operation.
- Read and adapt the AgentCore CLI's generated CDK app, including the resources it creates and the role it proposes.
- Explain and exercise the difference between provisioning infrastructure and releasing a new runtime version.
- Describe a release pipeline with an evaluation gate, explicit endpoint promotion, rollback by version, and teardown.
- Diagnose a failed request using its authentication, authorisation, endpoint, network and quota context.

| Depth                           | Topics                                                                                                                                  | Expected ability                                                                 |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Practice now**                | boto3 `bedrock-agentcore-control` and `bedrock-agentcore`, Strands Agents, `bedrock-agentcore` SDK, SSO profiles, the AgentCore CLI 1.0 | Run a small example, adapt configuration, explain each step.                     |
| **Understand and demonstrate**  | CI/CD with OIDC, execution roles, resource policies, versions and endpoints, Strands Evals gate, telemetry                              | Trace a release from source to a verified endpoint and name the failure points.  |
| **Read and recognise**          | CDK constructs behind the CLI, VPC mode and PrivateLink, SCPs, Control Tower                                                            | Explain their purpose and when a platform team would require them.               |
| **Defer deeper implementation** | Custom CDK or Terraform modules, full private topology, Runtime Instances, Payments                                                     | Study when a workload needs them; they are not prerequisites for the first call. |

The core automation path here is **the AgentCore CLI (Node) plus boto3 scripts**. CDK literacy is useful; authoring a CDK platform is outside this stage's scope.

## 2. Prerequisites

Before the practical work, be comfortable with Python environments and JSON, HTTP and the difference between authentication and authorisation, Git and YAML, and AWS accounts, Regions, IAM roles and policies.

Tooling, as of 25 Oct 2026 (C1–C5):

- An AWS account with IAM Identity Center; `aws configure sso` and `aws sso login --profile <name>`. No access keys in files, ever.
- `aws` CLI v2.
- Node.js 20.12 or newer and `npm install -g @aws/agentcore` (CLI 1.0.0, 22 Oct 2026).
- Python 3.13 in `../labs-setup/.venv` with the pinned requirements.
- Docker with buildx only for container runtimes (B03 lab 02); code deploy needs no Docker.
- If `pip show bedrock-agentcore-starter-toolkit` finds anything: uninstall it. It is deprecated and shadows the new `agentcore` binary.

Use a disposable account or a sandbox OU with a known cost and a teardown habit: `agentcore remove all --yes && agentcore deploy --yes`, or the `--cleanup` flag every lab script carries.

## 3. Understand the three deployment layers

Treat these as ownership boundaries, not a claim that each tool can operate on one layer only.

| Layer                            | What belongs here                                                                                                                                     | Main tools                                                                                                         | What to learn                                                                               |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| **Account, network and models**  | Account and OU, VPC, PrivateLink endpoints, KMS, IAM roles, Bedrock model access, guardrails, prompt routers, Transaction Search                      | Control Tower, CDK / CloudFormation / Terraform, `aws` CLI, `bedrock` API                                          | Resource ARNs, desired state, role trust, which Region offers which feature.                |
| **AgentCore objects**            | Runtimes and versions, endpoints, Harnesses, Gateways and targets, Policy engines, Memories, Identity providers, evaluation configs, Registry records | boto3 `bedrock-agentcore-control`, the AgentCore CLI (`agentcore add … && agentcore deploy`), CloudFormation types | Control plane vs data plane, immutable versions, `DEFAULT` endpoint, protocol per runtime.  |
| **Application code and runtime** | Agent code (Strands, LangGraph, any), container images or code zips, MCP servers, Lambda tools                                                        | `agentcore deploy`, ECR, zip to S3, CI/CD                                                                          | Build artefacts, the Runtime contract, execution identity, health checks, release versions. |

**Important distinctions:**

- Bedrock has **no deployment object for foundation models**. You pick a model, an inference profile and a service tier at request time (L4, L5). The Foundry habit of "deploy the model first" becomes "enable access once, then choose a profile id".
- The AgentCore **control plane** (`bedrock-agentcore-control`: `CreateAgentRuntime`, `CreateAgentRuntimeEndpoint`, `CreateHarness`, `CreateGateway`, `CreateGatewayTarget`, `CreatePolicyEngine`, `CreatePolicy`, `CreateMemory`, `CreateOauth2CredentialProvider`, `CreateOnlineEvaluationConfig`, `CreateRegistry` …) creates and versions objects. The **data plane** (`bedrock-agentcore`: `InvokeAgentRuntime`, `InvokeHarness`, `Evaluate`, `StartBatchEvaluation`, `CreateEvent`, `RetrieveMemoryRecords`, `GetResourceOauth2Token`, `StopRuntimeSession` …) uses them. A third client, `agent-registry`, only discovers records. The split was read from boto3 1.43.118 on 25 Oct 2026 (C10).
- The AgentCore CLI orchestrates across layers through a thin CDK app; it is not a different resource model from CloudFormation (C3).
- A Runtime runs your code in a microVM AWS operates. Runtime **Instances** run it on EC2 capacity in your account (A9). A self-hosted agent on Lambda or ECS runs where you operate it and can still be a Gateway target (D2).

### Model selection, the decisions behind `BEDROCK_MODEL_ID`

Three choices the console hides. Which **model**: the catalogue is wide (Nova 2, Claude 5.x and 4.x, GPT-6 and gpt-oss, Llama 4, Mistral, Qwen3, DeepSeek; L3); pick the smallest that clears the B05 evaluation threshold. Which **inference profile**: no prefix keeps inference in one Region and is not offered for new Claude models; `eu.` or `us.` keeps it in a geography; `global.` routes anywhere for availability (L4). The UK bank scenario uses `eu.` and accepts less quota headroom. Which **service tier**: `priority` at +75 %, `default`, `flex` at −50 %, `reserved`, and batch at about −50 %, supported per model (L5). Intelligent Prompt Routing exists for older families at USD 1 per 1,000 requests and is not available for Nova 2 Lite or Claude 5.5 (L6); on AgentCore the newer answer is a Gateway inference target with fallback and a circuit breaker (D8). A second endpoint, `bedrock-mantle`, serves OpenAI- and Anthropic-native APIs (L4).

Runnable: [`../labs-setup/01-models/`](../labs-setup/01-models/) checks access for the ids in `.env` and makes one Converse call signed with SigV4 from the SSO profile. No key appears anywhere; the `api_key=` sample from older books is the habit to unlearn.

### Connect to AgentCore: console, SDK, CLI and REST

Four ways to reach the same control plane:

| Path          | What it is                                                                                                                                                               | When                                                                    |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| Console       | Click-ops over the same APIs                                                                                                                                             | Reading state, never for production changes                             |
| boto3         | `boto3.Session(profile_name=…).client("bedrock-agentcore-control")`                                                                                                      | The labs; explicit, shape-exact, scriptable                             |
| AgentCore CLI | `agentcore add runtime … && agentcore deploy` writing `agentcore/agentcore.json` and synthesising CDK                                                                    | Teams that want one project file and a pipeline-friendly deploy         |
| REST          | SigV4-signed HTTPS to `bedrock-agentcore-control.<region>.amazonaws.com`; data plane at `bedrock-agentcore.<region>.amazonaws.com/runtimes/<urlencoded-arn>/invocations` | OAuth-inbound runtimes must be called this way with a bearer token (B5) |

**Creating a runtime and talking to it are separate operations.** `create_agent_runtime` returns an ARN and a version; `invoke_agent_runtime` (SigV4) or a raw HTTPS POST (JWT) sends the payload with a `runtimeSessionId` of at least 33 characters (B4, B5). Older examples use the Python starter toolkit's `agentcore launch`; match examples to the package versions you install.

### The SDK packages

| Package                    | Version (25 Oct 2026)                                                                                        | Role                                                                                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `bedrock-agentcore`        | 1.25.0; extras `strands-agents`, `a2a`, `ag-ui`, `langgraph`, `deepeval`, `ragas`, `autoevals`, `simulation` | `BedrockAgentCoreApp` (the Runtime contract), `serve_a2a`, `MemoryClient` / `MemorySessionManager`, `@requires_access_token`, `EvaluationClient` |
| `strands-agents`           | 1.62.0 (`[otel]` for tracing)                                                                                | The agent loop: `Agent`, `BedrockModel`, `MCPClient`, Graph / Swarm, hooks, `StrandsTelemetry`                                                   |
| `strands-agents-tools`     | 0.8.10                                                                                                       | Prebuilt tools                                                                                                                                   |
| `strands-agents-evals`     | 1.7.0                                                                                                        | `Case` / `Experiment` and the judge evaluators for local and CI evaluation                                                                       |
| `boto3`                    | 1.43.118                                                                                                     | Control plane, data plane, `agent-registry`, `bedrock`, `bedrock-runtime`                                                                        |
| `aws-opentelemetry-distro` | ≥0.18.0                                                                                                      | `opentelemetry-instrument` for ADOT spans into CloudWatch                                                                                        |

### How the SDK and the framework fit together

> **The control plane creates objects; the framework runs the loop; the `bedrock-agentcore` SDK is the contract between your loop and the Runtime.**

| Lifecycle      | Responsibilities                                                                                                        | Example                                                                                             |
| -------------- | ----------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **Deployment** | Provision account and network, create AgentCore objects, deploy code                                                    | CDK provisions the VPC; a boto3 step calls `create_agent_runtime`; `agentcore deploy` ships the zip |
| **Runtime**    | Serve `/invocations` and `/ping` on 8080, call models and tools with the execution role, hold OAuth tokens in the vault | `BedrockAgentCoreApp` wraps a Strands `Agent`; `MCPClient` reaches the Gateway with a bearer        |

The Runtime contract (B1, B6, B8, B9): HTTP on 8080 with `POST /invocations` and `GET /ping` returning `Healthy` or `HealthyBusy`; MCP servers on 8000 at `/mcp`; A2A on 9000 with the agent card; `platformVersion` `V1` (default) or `V2` (snapshot restore, faster cold start, five Regions, B3); sessions idle out at 15 minutes and end at 8 hours on microVMs, 14 days on Instances (B4); every update creates an immutable version and the `DEFAULT` endpoint follows the latest unless you pin a custom endpoint (B7).

**Compare two agent paths:**

- **Harness:** publish the definition (model, system prompt, tools, skills) with `CreateHarness`; AgentCore runs a Strands-powered loop you do not ship. No container, no zip. GA Jun 2026 (A6). The Foundry prompt agent's cousin.
- **Agent whose loop you own:** write the loop in Strands or another framework, package it as a zip or an ARM64 image, create a Runtime. Code deploy versus container versus Instances decides who builds and where it runs; it does not change the contract.

**Study check:** draw the deployment path and the request path for a Harness and for a code-deploy Runtime. Mark where the definition lives, where the loop executes and which identity makes each call. The loop itself is B03.

## 4. Study sequence

### Step 1 — Map accounts, Regions, profiles and ARNs

**Study:** account → Region → model access → inference profile; AgentCore ARNs (`arn:aws:bedrock-agentcore:<region>:<account>:runtime/<id>`) versus data-plane URLs; profile ids versus model ids.

**Practice:** run `../labs-setup/01-models/model_access.py` and annotate which values identify the account, which select the profile and which configure the client.

**Ready to continue when:** you can explain why enabling a model, choosing a profile and sending a request are separate decisions, and why there is no deployment to wait for.

### Step 2 — Choose the client and authenticate

**Study:** `boto3.Session(profile_name=AWS_PROFILE)` from SSO versus the execution role inside the Runtime versus a Cognito JWT for inbound calls (E2); the per-lab `_common.py` pattern (`control()`, `data()`, `write_env()`); what `BedrockAgentCoreApp` injects into `context`.

**Practice:** `../B03-Creating-Agents-on-AgentCore/labs/01-ways-to-build/03-ephemeral-strands.py` makes one agent call with no AgentCore object at all; then `02-runtime-code-deploy.py` creates the first Runtime and writes its ARN to `.env`.

**Ready to continue when:** you can tell apart a credential failure (expired SSO), a permission failure (execution role missing `bedrock:InvokeModel`), a wrong endpoint or qualifier, and throttling (B12), from the error body rather than the status code alone.

### Step 3 — Provision reproducibly

**Study:** the CDK app the AgentCore CLI synthesises (`agentcore create --template agent-python-strands`, then read `agentcore/agentcore.json`, `aws-targets.json`, the generated stack); the execution role it proposes; how `agentcore deploy` maps to a CloudFormation change set (C3).

**Practice:** scaffold a project in a scratch folder, read the synthesised template, change the network mode to VPC and the role statements, read the diff. Compare with the boto3 twin in B03 lab 01. Do not deploy from the scratch folder.

**Ready to continue when:** you can explain what a second `agentcore deploy` changes (a new runtime version, not a new runtime) and which resources `remove all` deletes and which it leaves (log groups, S3 objects; verify).

### Step 4 — Understand the CLI lifecycle

| Command                                                     | Purpose to understand                                                                 |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `agentcore create`                                          | Scaffold a project from a template (Python Strands, container, …)                     |
| `agentcore add runtime / harness / memory / gateway / tool` | Add an object to `agentcore.json`                                                     |
| `agentcore deploy`                                          | Synthesise and deploy the CDK app; a repeat creates a new runtime version             |
| `agentcore dev` / `invoke --local`                          | Run the Runtime contract locally with hot reload; Agent Inspector in the browser (C4) |
| `agentcore invoke --runtime` (or `--harness`, `--gateway`) | Call a deployed object with a session |
| `agentcore status / logs / traces`                          | Read state, logs and spans                                                            |
| `agentcore eval …`                                          | Evaluation commands (format not verified; the labs use boto3)                         |
| `agentcore migrate`                                         | Import a Classic Bedrock Agent (A12)                                                  |
| `agentcore remove all --yes && agentcore deploy --yes`      | Teardown                                                                              |

**Practice:** trace B03 lab 01 from zip to a streamed answer. Identify where the build happens, how a new version is created, and which identity calls the model.

**Ready to continue when:** you can distinguish an infrastructure change from a code-only release and verify both the version and a real request.

### Step 5 — Automate release and promotion

**Study:** GitHub Actions with `aws-actions/configure-aws-credentials` and an OIDC role, no stored keys; environment-specific `aws-targets.json`; approval gates; evidence.

Design the release in this order:

1. Validate code, `agentcore.json` and the synthesised template.
2. Review the CloudFormation diff and apply approved changes with the pipeline role.
3. Deploy the candidate; record the source revision, the artefact (zip hash or image digest) and the runtime version.
4. Smoke-invoke the candidate through a custom endpoint pinned to that version, not `DEFAULT`.
5. Run Strands Evals locally against the cases file and an on-demand AgentCore evaluation on the smoke session (B05 lab 02); fail the job under threshold.
6. Promote by `update_agent_runtime_endpoint` on the stable endpoint; keep the previous version as the rollback target (B7).

**Practice:** explain how a failed evaluation prevents promotion and how the stable endpoint is repointed back. Note that `DEFAULT` always follows the latest version, so production callers should use a named endpoint.

**Ready to continue when:** you can trace a release with no console step and name the pipeline identity separately from the execution role.

## 5. Production concerns to understand

| Concern              | What to study                                                                                                                                  | Question you should be able to answer                              |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Identity and secrets | Execution-role trust with `SourceAccount` / `SourceArn`, resource policies, the token vault, `BedrockAgentCoreFullAccess` warning (F9)         | Who provisions, who runs the agent, what can each identity reach?  |
| Networking           | PUBLIC vs VPC mode, PrivateLink control plane, VPC egress, `aws:VpceOrgID` (F10)                                                               | Does the runtime reach models and tools through the intended path? |
| Observability        | Transaction Search, ADOT, per-agent log group, GenAI Observability (H1)                                                                        | Can I trace a failed request without logging content I should not? |
| Cost and capacity    | The table below; quotas 1,000 TPS data plane, 25 TPS new sessions, 5,000 active sessions (B12); idle 15 min, max 8 h; V1 vs V2 cold start (B3) | What limits throughput and how will I notice spend?                |
| Governance           | SCPs, Cedar on the Gateway, Registry approval, CloudTrail (B09)                                                                                | Can I identify and reproduce the configuration serving a release?  |
| Recovery             | Named endpoints and version pinning, session storage mounts, teardown scope                                                                    | What does rollback restore, and what needs a separate plan?        |

Per-second consumption pricing (L8, fetched 25 Oct 2026):

| Item              | Price                                                                                           |
| ----------------- | ----------------------------------------------------------------------------------------------- |
| Runtime V1        | USD 0.0895 per vCPU-hour + 0.00945 per GB-hour of active CPU, 128 MB minimum                    |
| Runtime V2        | USD 0.1276 per vCPU-hour + 0.0169 per GB-hour, memory reclaimed after 120 s idle                |
| Runtime Instances | EC2 price + about 12 % management fee                                                           |
| Gateway           | USD 0.005 per 1,000 invocations; 0.025 per 1,000 searches; 0.02 per 100 tools indexed per month |
| Policy            | USD 0.000025 per authorisation                                                                  |
| Evaluations       | USD 0.0024 / 0.012 per 1,000 judge input / output tokens; custom USD 1.50 per 1,000             |
| Memory long-term  | USD 0.75 per 1,000 records per month; 0.50 per 1,000 retrievals                                 |
| Identity          | USD 0.010 per 1,000 tokens, free through Runtime and Gateway                                    |
| Observability     | CloudWatch rates                                                                                |

Cost of one session, as an interview answer: a 10-minute support conversation on 1 vCPU and 2 GB active for about 90 seconds of model wait costs roughly USD 0.003 of Runtime, plus model tokens, plus a fraction of a cent for a handful of Gateway calls and Policy decisions. Idle time on V1 is not billed; a session that is left Active with `HealthyBusy` is. Destroy runtimes at the end of a lab session.

ARM64 images only for container runtimes; code zips run on Python 3.10–3.14 or Node 22 (shape enum, C10).

## 6. Completion checklist

- [ ] Explain the three layers and classify a new operation by plane and permission.
- [ ] Run `model_access.py` and `smoke_test.py` and explain profile, tier and credential.
- [ ] Read the CDK app the CLI synthesises; explain its role, network mode and what a second deploy changes.
- [ ] Create a runtime with boto3 and with `agentcore deploy`; explain the difference in artefacts.
- [ ] Verify a version with a real invocation through a pinned endpoint, and find its spans.
- [ ] Show a failed Strands Evals experiment blocking promotion and repoint the endpoint back.
- [ ] Name the pipeline role and the execution role and remove what each does not need.
- [ ] Tear down and account for what remains (log groups, S3 objects, Registry records).

A useful final sentence: "I provision the account and network with CDK, create AgentCore objects through the control plane from a pipeline with OIDC, ship the loop as a zip or image to a Runtime, and promote a version only after an evaluation gate, by repointing a named endpoint."

## 7. Same thing on Foundry

| AWS                                                         | Foundry (F02)                                                 |
| ----------------------------------------------------------- | ------------------------------------------------------------- |
| Inference profile + service tier, no deployment object      | Model deployment (`GlobalStandard`, `DataZoneStandard`, PTU)  |
| `bedrock-agentcore-control` / `bedrock-agentcore`           | `azure-ai-projects` project client / OpenAI-compatible client |
| AgentCore CLI 1.0 + `agentcore.json` + CDK app              | `azd` + `azure.yaml` + Bicep                                  |
| `create_agent_runtime` versions + named endpoints           | `create_version` + agent endpoint with version selector       |
| Execution role trusted by `bedrock-agentcore.amazonaws.com` | Project managed identity / agent identity                     |
| GitHub OIDC with `configure-aws-credentials`                | Federated credentials with `azure/login`                      |
| Deprecated Python starter toolkit (`agentcore launch`)      | Deprecated `agent.yaml` and protocol `v1`                     |
| Classic Bedrock Agents in maintenance mode                  | Foundry declarative workflows retiring 1 Dec 2026             |
| Strands Evals + on-demand evaluation as the gate            | `azd ai agent eval run` / evals API as the gate               |

## 8. Reference reading

1. AgentCore release notes (A): https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html
2. Get started with the AgentCore CLI (C3): https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-cli.html
3. AgentCore CLI releases (C2): https://github.com/aws/agentcore-cli/releases
4. Runtime: how it works, sessions, versioning, invoke (B3, B4, B5, B7): https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html
5. `bedrock-agentcore` Python SDK (C6): https://github.com/aws/bedrock-agentcore-sdk-python
6. Strands Agents documentation (C8): https://strandsagents.com/latest/documentation/docs/
7. Model access, inference profiles, service tiers (L4, L5, L7): https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html
8. AgentCore pricing (L8): https://aws.amazon.com/bedrock/agentcore/pricing/
9. Deprecated starter toolkit, for the record (C1): https://github.com/aws/bedrock-agentcore-starter-toolkit

Local ground truth: the boto3 operation and shape dump regenerated from `../labs-setup/.venv` (C10). AWS pages checked on **25 Oct 2026**. Recheck versions, Region support and exact fields when doing the exercises; the `agentcore eval` command format and the CLI template's default role scope were not verified.
