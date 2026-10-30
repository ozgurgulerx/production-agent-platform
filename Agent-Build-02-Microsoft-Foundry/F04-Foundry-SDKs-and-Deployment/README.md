# F04 — Foundry SDKs and Automated Deployment

[Capability builds and exact checklist targets](capability-builds.md#build-contract)

Updated curriculum guidance — 30 October 2026. Scores are **unassessed**; retained labs are **not newly runtime-verified**. See the [depth and preservation contract](../reference/curriculum-mapping.md).

## Deployment evidence and configuration boundaries

For each operation, record control plane versus data plane, client, endpoint, API generation, identity and permission. A valid token sent to the wrong audience is not fixed by adding subscription-wide roles. Keep project operations distinct from inference and resource provisioning. Use the existing deployment-layer explanations below as the starting point.

A release identifies code/container digest, dependency lock, agent and prompt versions, model deployment/version, index/schema version and configuration revision. Secrets are referenced rather than embedded. Separate the developer login, CI federated principal and runtime identity; each should receive only its operation's permissions. Explain startup configuration, secret rotation and the failure behaviour when a required setting is absent.

Learner exercise: write a release manifest for the existing ticket agent without inventing build results. Compare model deployment options for the workload's throughput, latency and residency requirements; record assumptions and pricing check dates. Explain a quota denial, model-name/deployment-name mismatch and failed federated login. Review a container's startup, health and readiness behaviour before selecting a hosting target.

Completion evidence: an operation/client matrix, reproducible declared environment, reviewed deployment change, secret-free configuration example and a rollback explanation. Do not upgrade packages as part of folder migration. See [compatibility notes](../reference/sdk-compatibility.md) and [SDK overview](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview).

## Retained chapter material

The following material is preserved with its original scope and dates. Historical module-number references refer to the [migration mapping](../reference/curriculum-mapping.md#repository-preservation-and-migration-rules); current navigation uses folder links.

# F00 — Foundry SDKs and Automated Deployment

Learn how to move from a Foundry project to a repeatable, authenticated deployment. The central skill is knowing **what you are deploying, which API or tool owns it, and how you verify the result**.

This stage covers platform setup, SDK boundaries, and release automation. Detailed agent design belongs in [F01 — Creating AI Agents in MS Foundry](../F05-Creating-Agents/README.md); tool integration belongs in [F02 — Foundry Agent Tooling](../F06-Agent-Tooling-MCP-and-Integration/README.md).

## 1. Learning outcomes and study depth

By the end of F00, you should be able to:

- Distinguish Azure resource provisioning, Foundry project operations, model inference, and application deployment.
- Select the appropriate SDK/client, endpoint, identity, and permission scope for an operation.
- Read and adapt a supplied Bicep deployment, including parameters, dependencies, outputs, and role assignments.
- Explain and exercise the difference between provisioning infrastructure and deploying application changes.
- Describe a release pipeline with evaluation, explicit promotion, rollback, and cleanup.
- Diagnose a failed request using its authentication, authorization, endpoint, network, and quota context.

| Depth | Topics | Expected ability |
|---|---|---|
| **Practice now** | Python Projects SDK, OpenAI-compatible client, Azure Identity, Bicep sample, Azure CLI, `azd` | Run a small example, adapt configuration, and explain each step. |
| **Understand and demonstrate** | CI/CD, federated authentication, managed identity, RBAC, versioning, evaluation gates, telemetry | Trace a release from source to a verified endpoint and identify failure points. |
| **Read and recognize** | Terraform providers and state, private networking, Azure Policy, enterprise landing zones | Explain their purpose and when a platform team would require them. |
| **Defer deeper implementation** | Custom Terraform modules, full private-network topology, APIM policy engineering, enterprise governance integration | Study when a specific deployment requires them; they are not prerequisites for the first SDK call. |

The core infrastructure path here is **Bicep + `azd`**. Terraform literacy is useful, but authoring a Terraform platform is outside this stage's core scope.

## 2. Prerequisites

Before starting the practical work, be comfortable with:

- Python environments, package installation, imports, environment variables, exceptions, and JSON.
- HTTP requests, endpoints, status codes, and the difference between authentication and authorization.
- Git commits and basic YAML structure.
- Azure subscriptions, resource groups, regions, Microsoft Entra identities, and role assignments.

For a cloud exercise, confirm subscription access, permission to provision the chosen resources, access to required role assignments, and model availability/quota in the chosen region. Use a disposable learning environment with a known cost and cleanup plan.

## 3. Understand the three deployment layers

Treat these as ownership boundaries, not a claim that each tool can operate on only one layer.

| Layer | What belongs here | Main tools | What to learn |
|---|---|---|---|
| **Azure infrastructure / control plane** | Foundry account and project, model deployments, identities, RBAC, networking, monitoring resources, and scenario-specific storage/search dependencies | ARM, Bicep, Terraform, Azure CLI | Resource IDs, desired state, dependencies, parameters, outputs, and deployment permissions. |
| **Foundry project operations / data plane** | Agent definitions and versions, inference requests, evaluations, files, and other supported project features | Projects SDK, OpenAI-compatible client, REST, supported `azd ai` commands | Client boundaries, project endpoints, API versions, request lifecycle, and versioned definitions. |
| **Application code and runtime** | Hosted-agent code, externally hosted agents, MCP servers, and functions | Runtime-specific deployment tools, container registry, `azd`, CI/CD | Build artifacts, configuration, runtime identity, health checks, and release versions. |

**Important distinctions:**

- The Projects SDK does not provision the Azure account/project in the ARM sense. Those resources must already exist before you connect to their project endpoint.
- Connections need operation-level classification: creating an account/project connection can be a control-plane operation, while discovering or using connections can be exposed through project APIs. Check the specific API rather than classifying everything called a “connection” as data plane.
- `azd` orchestrates work across layers. It is not an alternative resource model to ARM or Bicep.
- A hosted agent runs in Foundry's managed hosting environment. A self-hosted agent runs in infrastructure you operate, such as Container Apps or AKS. An MCP server can have its own deployment lifecycle.

Read the [Foundry SDK overview](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview) alongside the [Bicep resource quickstart](https://learn.microsoft.com/en-us/azure/foundry/how-to/create-resource-template) to see the boundary in concrete examples.

### Connect to a project: portal, SDK, and REST API

The **Foundry Projects SDK** lets Python code connect to an existing Foundry project and create agents through Agent Service, instead of creating them manually in the portal. Accessing the project means calling its cloud APIs; your Python script can still run locally on your Mac.

- The **project endpoint** identifies the project your code targets.
- **Credentials** authenticate the caller; Azure permissions determine which operations are allowed.
- **`AIProjectClient`** provides programmatic access to project operations.
- **`project.agents`** exposes agent management operations, including creating agent versions with a model, instructions, and tools.

The **REST API** is the HTTP interface you can call directly. The SDK provides Python methods that construct and send those requests for you. For example:

| Python SDK | Direct REST request |
|---|---|
| `project.agents.create_version(...)` | `POST {project_endpoint}/agents/{agent_name}/versions?api-version=v1` |
| Pass Python objects. | Send a JSON request body. |
| The SDK integrates with your credential and constructs the HTTP request. | Supply the access token, HTTP headers, URL, and request body yourself. |

Both approaches operate on agents in the target Foundry project. The portal, SDK, and direct REST calls are different ways to work with the service; their available features can differ. The SDK is a convenient starting point for Python, while REST makes the underlying request explicit.

**Creating an agent and talking to it are separate operations.** In the current API, use the project client for agent creation and versioning, and an OpenAI-compatible client for conversations and responses. Older examples can use different methods and API versions, so match examples to the SDK version you install.

Sources: [SDK quickstart](https://learn.microsoft.com/azure/ai-foundry/quickstarts/get-started-code?pivots=fdp-project&tabs=azure-ai-foundry), [AIProjectClient reference](https://learn.microsoft.com/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient), [Foundry REST reference](https://learn.microsoft.com/en-us/rest/api/microsoft-foundry/aiproject), and [agent migration guide](https://github.com/MicrosoftDocs/azure-ai-docs/blob/main/articles/foundry/agents/how-to/migrate.md).

### How the SDK and Agent Framework fit together

Use this short explanation first, then expand the relevant layer:

> **IaC for Azure resources; the SDK for project definitions; Agent Framework for the loop when you own the agent code.** The SDK also participates at runtime underneath the Framework's Foundry integration.

There are two lifecycles to study:

| Lifecycle | Responsibilities | Example |
|---|---|---|
| **Deployment** | Provision resources, publish supported project definitions, and deploy application artifacts. Keep definitions in source control and apply production changes through reviewed pipeline steps. | Bicep provisions a project; an SDK step creates an agent or toolbox version; `azd` deploys your hosted-agent code. |
| **Runtime** | Execute the agent loop, call models, and consume configured tools using the runtime identity. | Agent Framework's `FoundryChatClient` builds on the Foundry SDK; `FoundryToolbox` connects to an existing toolbox's MCP endpoint. |

The SDK and Framework therefore work together. Publishing definitions is one SDK use; accessing Foundry while the agent runs is another. `FoundryToolbox` consumes the toolbox—it does not create that toolbox simply by connecting to it. Its current hosting integration is beta, so check package compatibility before following an example. See the [SDK overview](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview) and [Agent Framework Toolbox guide](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/tools/foundry-toolbox).

**Compare two agent paths:**

- **Prompt agent:** publish the server-side definition, including instructions, model selection, and tools. Foundry manages execution; your application can call the Responses API with an `agent_reference`. No custom Agent Framework loop or agent container is required for this path. The definition still depends on configured models, tools, identities, and any application code that invokes it. See the [official prompt-agent example](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/file-search).
- **Agent whose loop you own:** write the orchestration in Agent Framework (or another framework), package and deploy that code to the chosen runtime, and use its Foundry integration for model/tool access. Foundry-hosted versus self-hosted determines who operates the runtime; it does not replace the distinction between your loop and the SDK calls it makes.

**Study check:** draw the deployment path and runtime request path separately for each agent type. Mark where the definition is created, where the loop executes, and which identity makes each call. Detailed loop implementation remains in F01.

## 4. Study sequence

### Step 1 — Map resources, endpoints, and names

**Study:** account/resource → project → model deployment; Azure resource IDs versus service endpoints; model names versus deployment names.

**Practice:** take one official sample and annotate which values identify infrastructure, which configure the client, and which select the deployed model. Identify the resource that must exist before each request can succeed.

**Ready to continue when:** you can explain why creating a project, deploying a model, and sending a model request are separate operations.

#### Model deployment, the decisions behind `FOUNDRY_MODEL`

A deployment is the only thing an agent can reference, and it carries three choices the portal's Deploy button hides. Which **model**: use the leaderboards (quality index, HarmBench safety, real cost per benchmark run, P90 latency) and the Compare page to separate `gpt-5.2` from `-chat` and `-codex`, then pick the smallest model that clears your F05 eval threshold. Which **deployment type**: `GlobalStandard` by default (served anywhere, highest quota, cheapest), `DataZoneStandard` when processing must stay in the EU or US zone, `Standard` for a single geography, the `ProvisionedManaged` family for reserved PTU throughput, `GlobalBatch` for 50 % off asynchronous jobs; data at rest never leaves the geography in any of them. Which **name**: agents, SDK calls and traces use the deployment name, so keeping it equal to the model name is the default and a second deployment (`gpt-5-mini-next`) is how you A/B a model upgrade without touching agent code. A fine-tuned model is deployed the same way, with an hourly hosting fee on the Standard tiers and a free 24-hour `DeveloperTier` for evaluation (F06). Model router is itself a deployment that picks among OpenAI, Anthropic, xAI, DeepSeek and Meta models per request in Balanced, Quality or Cost mode.

Runnable: [`../labs-setup/01-models/`](../labs-setup/01-models/) deploys the four deployments the F03–F05 labs assume, with `az cognitiveservices account deployment create` and the equivalent `deployments.bicep`, then proves each one with an Entra-only Responses call. No API key appears anywhere; the book-style `api_key=` sample is the one habit to unlearn here.

### Step 2 — Choose the SDK and authenticate

**Study:**

- `azure-ai-projects` and `AIProjectClient` for Foundry project integration.
- The configured OpenAI-compatible client for supported inference and related APIs; understand what `get_openai_client()` provides.
- How `FoundryChatClient` uses the SDK at runtime, how `FoundryToolbox` consumes an existing toolbox, and how a prompt agent can be invoked without a custom Framework loop.
- `azure-identity` and `DefaultAzureCredential`: how local developer credentials differ from a deployed workload's identity.
- Project endpoint versus model/API endpoint, token audience, and operation-specific RBAC requirements.
- SDK/API compatibility: use examples for the same Foundry generation and package version. Do not mix classic and current examples without checking migration guidance.

**Practice:** follow the current official Python SDK example, identify the credential it uses, make a small model request, and inspect the response. Record package versions and configuration names without recording credentials.

**Ready to continue when:** you can explain which client makes each call and distinguish a credential failure, insufficient permission, wrong endpoint/deployment, and quota or throttling failure. Use the service error details rather than treating an HTTP status alone as a diagnosis.

### Step 3 — Provision reproducibly with Bicep

**Study:** parameters, resources, modules, dependencies, outputs, managed identities, RBAC scope, and deployment previews. Learn which resources the selected basic or Standard setup actually needs.

**Practice:** read and adapt the [official Bicep sample](https://learn.microsoft.com/en-us/azure/foundry/how-to/create-resource-template). Before deployment, explain its resource list and review `what-if` output. Trace how its outputs become SDK configuration. Inspect the result of a repeat deployment.

**Ready to continue when:** you can explain how the same template supports separate environments, what a repeat deployment changes, and which resources need deliberate cleanup. A repeatable template does not imply every update is harmless.

#### Focused Bicep learning route: one course, one practice repository

For the **read-and-modify** level, complete the fundamentals, then apply them to a Foundry template. Keep the other resources as references rather than expanding the study plan.

1. **Learn the language:** complete [Fundamentals of Bicep](https://learn.microsoft.com/en-us/training/paths/fundamentals-bicep/). Cover resources, parameters, variables, outputs, modules, conditions, and loops. The current listing estimates **2 hours 16 minutes**; allow additional time to repeat exercises. Training content is free, but check each exercise's subscription requirements rather than assuming a free Azure sandbox is available.
2. **Read a real Foundry deployment:** use the [Foundry Bicep infrastructure samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep). Begin with the basic sample, then compare its resources and dependencies with a Standard setup. Follow the sample's deployment instructions to study `az deployment`, parameter files, outputs, and `what-if` in context.
3. **Inspect private-network examples when needed:** read [11-private-network-basic-vnet](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/11-private-network-basic-vnet) and [19-private-network-agent-tools](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/19-private-network-agent-tools) when preparing private MCP connectivity. Compare network paths, DNS, identities, and tool-hosting dependencies. These are topology-specific study targets, not prerequisites for every MCP exercise.
4. **Stop at the required depth:** explain the template, make a small configuration change, inspect the preview, and trace outputs into application configuration. Deeper authoring is optional until a concrete requirement needs it. No book is required for this route.

Keep the Bicep documentation and VS Code extension beside you while reading. Look up unfamiliar resource types—such as `Microsoft.CognitiveServices/accounts/projects`—in the ARM resource reference, selecting the API version used by the template.

#### Bicep reading bookmarks

All supplied URLs are retained below for later reading. Status notes reflect checks on **2026-10-25**; a fetch failure is not proof that a URL is permanently unavailable.

| Priority | Resource | URL / note |
|---|---|---|
| **Do first** | Fundamentals of Bicep — supplied bookmark | <https://learn.microsoft.com/en-us/training/paths/bicep-deploy> — could not fetch during this review; use the verified current path below. |
| **Do first** | Fundamentals of Bicep — verified current path | <https://learn.microsoft.com/en-us/training/paths/fundamentals-bicep/> |
| **Optional later** | Intermediate Bicep | <https://learn.microsoft.com/en-us/training/paths/intermediate-bicep> — currently redirects to Azure Resource Manager docs. Fundamentals already covers modules and conditions. |
| **Skip for F00** | Advanced Bicep | <https://learn.microsoft.com/en-us/training/paths/advanced-bicep> — currently redirects to Azure Resource Manager docs. |
| **Keep open** | Bicep documentation | <https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/> |
| **Look up by resource type** | ARM/Bicep resource reference | <https://learn.microsoft.com/en-us/azure/templates/> |
| **Practice target** | Foundry Bicep infrastructure | <https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep> |
| **Private-network study** | Basic VNet sample | <https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/11-private-network-basic-vnet> |
| **Private-network study** | Agent tools sample | <https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/19-private-network-agent-tools> |
| **Reference as needed** | Azure Verified Modules — Bicep registry modules | <https://github.com/Azure/bicep-registry-modules> |
| **Reference as needed** | Azure quickstart templates | <https://github.com/Azure/azure-quickstart-templates> |
| **Authoring aid** | Bicep VS Code extension — completion and validation | <https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep> |
| **Troubleshooting / releases** | Bicep repository | <https://github.com/Azure/bicep> |
| **Additional bookmark** | Learn Bicep documentation source | <https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/azure-resource-manager/bicep/learn-bicep.md> |

**Terraform, only if brought back into scope:** start with [HashiCorp's Azure tutorials](https://developer.hashicorp.com/terraform/tutorials/azure-get-started), then consult the [AzAPI provider documentation](https://registry.terraform.io/providers/Azure/azapi/latest/docs). Use a familiar Foundry sample as the comparison target, checking resource coverage, API versions, state, and deployment behavior instead of assuming a direct translation.

### Step 4 — Understand the `azd` deployment lifecycle

**Study:** environment configuration, `azure.yaml`, infrastructure templates, build artifacts, and the selected hosting model.

| Command | Purpose to understand |
|---|---|
| `azd provision` | Provision or update the template's Azure infrastructure. |
| `azd deploy` | Deploy application/agent changes using the configured services and hooks. |
| `azd up` | Run the combined provisioning and deployment workflow. |
| `azd down` | Tear down the environment's provisioned resources; inspect scope and retained data first. |

**Practice:** trace the [hosted-agent deployment guide](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/deploy-hosted-agent) from source to a callable endpoint. Identify where the build happens, how a new agent version is created, and which identity accesses models/tools. If following a self-hosted example, identify the runtime you must operate instead.

**Ready to continue when:** you can distinguish an infrastructure change from a code-only release and verify both the deployed version and an actual request. Command success alone does not prove the agent works.

### Step 5 — Automate release and promotion

**Study:** choose one CI/CD system first—GitHub Actions or Azure Pipelines. Learn federated authentication to Azure, environment-specific configuration, permissions, approval gates, and release evidence. See [the `azd` CI/CD guide](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/configure-devops-pipeline).

Design the release in this order:

1. Validate source, configuration, and infrastructure changes.
2. Review the infrastructure preview and apply approved changes with a deployment identity.
3. Build and deploy a candidate; record the source revision, artifact identity, agent version, and relevant configuration.
4. Run a smoke request and a small, predefined evaluation set against that candidate.
5. Promote only when checks pass; record the selected version and environment.
6. Verify the promoted endpoint and retain a known-good rollback target.

**Practice:** explain how a failed evaluation prevents promotion and how the previous release is restored. Hosted-agent endpoints can follow the latest version: configure version selection/routing so candidate deployment does not expose unvalidated behavior to production. Check the selected deployment tool's routing behavior.

**Ready to continue when:** you can trace a release without relying on undocumented portal changes, and distinguish the pipeline's deployment identity from the application's runtime identity. Federated Azure login avoids a stored Azure client secret; it does not eliminate every possible third-party secret.

## 5. Production concerns to understand

These are design questions to answer for the selected workload, not a requirement to deploy every service in the first exercise.

| Concern | What to study | Question you should be able to answer |
|---|---|---|
| Identity and secrets | Least-privilege RBAC, managed/workload identities, agent identities where supported, Key Vault for necessary secrets | Who provisions resources, who runs the agent, and what can each identity access? |
| Networking | Public/private access, Private Link, DNS, outbound access, setup-specific subnet requirements | Can the runtime reach models and tools through the intended network path? |
| Observability | Application Insights, Log Analytics, OpenTelemetry, request correlation, appropriate diagnostic settings | Can I trace a failed request without logging sensitive content unnecessarily? |
| Cost and capacity | Model availability, deployment capacity, token/rate limits, provisioned versus consumption pricing, budgets and tags | What limits throughput, and how will I detect unexpected spend? |
| Governance | Azure Policy, release manifests, evaluation evidence, approval records | Can I identify and reproduce the configuration serving a given release? |
| Recovery | Version selection, compatible configuration, state/data retention, resource teardown | What does rollback restore, and what data or infrastructure changes need a separate recovery plan? |

Choose networking, dependencies, and governance controls from actual requirements. Avoid assuming one Standard setup, subnet size, or service combination fits every private-data workload.

## 6. Completion checklist

This is a learning checklist, not a claim that deployment has already been implemented or verified. Produce the evidence yourself as you complete the exercises.

- [ ] Explain the three layers and classify a new operation by its API and permissions.
- [ ] Run a Python SDK request and explain its client, endpoint, model selection, and credential.
- [ ] Read and adapt a Bicep sample; explain its preview, outputs, and repeat-deployment behavior.
- [ ] Explain and exercise provisioning versus application deployment in one learning environment.
- [ ] Verify a deployed version with a real request and locate useful diagnostic evidence.
- [ ] Demonstrate a failed evaluation blocking promotion and describe or exercise rollback.
- [ ] Identify deployment versus runtime permissions and remove unnecessary access.
- [ ] Review cleanup scope and remove unneeded learning resources, accounting for retained data.

A useful final explanation is: “I provision Azure resources with infrastructure as code, use the appropriate project and inference clients for Foundry operations, and release application code through a pipeline that verifies a candidate before promotion.” Be able to support each part with your own evidence.

## 7. Reference reading

Read the first four alongside the study steps; use the rest when comparing tools or choosing a topology.

1. [Microsoft Foundry SDKs and endpoints](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview) — client selection, endpoint configuration, and current examples.
2. [Deploy a Foundry resource with Bicep](https://learn.microsoft.com/en-us/azure/foundry/how-to/create-resource-template) — resource/project provisioning and sample templates.
3. [Deploy a hosted agent](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/deploy-hosted-agent) — deployment methods, versions, and endpoint verification.
4. [`azd` CI/CD support](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/configure-devops-pipeline) — pipeline integration and authentication choices. Review setup side effects before running configuration commands.
5. [Foundry samples](https://github.com/microsoft-foundry/foundry-samples) — infrastructure and application examples; inspect the chosen sample's requirements.
6. [Comparing Terraform and Bicep](https://learn.microsoft.com/en-us/azure/developer/terraform/get-started/comparing-terraform-and-bicep) — provider, state, and infrastructure-target differences.

Local reference: `documentation/azure-foundry-2026-10-13.md` (repository-local, git-ignored snapshot). Current Microsoft documentation was checked on **2026-10-25**. Recheck versions, feature availability, region support, and exact API methods when doing the exercises.
