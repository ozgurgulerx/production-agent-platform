# G01 — Landing zones for production agents on Gemini Enterprise Agent Platform

Status: skeleton, 25 Oct 2026. Headings fixed; each `###` carries a scope note to be replaced by prose. Facts are cited by letter from [`../reference/reading-map-gcp-agents-2026-10-25.md`](../reference/reading-map-gcp-agents-2026-10-25.md); anything not in the map is marked unverified. Foundry counterpart: `Agent-Build-02-Microsoft-Foundry/F02-Landing-Zones-and-Networking`. Running scenario: the support-ticket agent (`ticket-agent`) and its ticketing MCP server (MCP Toolbox on Cloud Run), deployed for a UK bank into `europe-west2`. Labs for this chapter: none; the `terraform/` folder is a scaffold to read, not apply. Shared environment: [`../labs-setup/`](../labs-setup/).

## Opening

### The aim

One paragraph: an agent in production on Google Cloud is three layers of ownership stacked on one another. The organisation and its folders (platform team), the environment projects inside a VPC Service Controls perimeter (shared AI platform team), and your workload inside one project (you). Agent Runtime (ex-Agent Engine; the API resource is still `ReasoningEngine`, A5) has a shape the landing zone has to know before the first agent exists: it builds and runs a container you do not host, it has no internet egress inside a perimeter (I2), and its network path is a Private Service Connect interface you can only set at create time (I3). Most "production" failures are a layer-boundary mistake, not an agent mistake.

### What we are trying to avoid

One-line scenes: the agent that works in the sandbox project and fails the review board because the Toolbox MCP server on Cloud Run has public ingress; the project created by clicking that nobody can rebuild; `gemini-3.5-flash` on the `global` endpoint when the data-residency policy says `eu` (A9, F6); the Runtime project that was not in the perimeter before the first deploy, so the deploy fails or, worse, succeeds outside it (I2); the `/28` network attachment that cannot be changed without recreating every agent (I3); the CMEK key ring in another region (F5); Data Access audit logs never switched on, so the first incident has no "who asked what" trail (F8).

### Has this happened?

Two or three real incidents of public-ingress or misconfigured-network AI services, fetched and dated on the writing day. Candidates to look up: the 2025 MCP server exposure scans; GCP service-account key leaks in public repositories; a bank's cloud-configuration fine. Not from memory; not in the map, so unverified until fetched.

### What the chapter covers

The three tiers and who owns what; region and endpoint choice; the VPC-SC perimeter and the no-egress rule; the PSC interface; CMEK; the org-policy baseline; IAM for agents and the two service agents; audit logging; and the infrastructure-as-code skeleton for an Agent Runtime deployment.

### What you have at the end

A one-page ownership matrix, a perimeter diagram with Agent Runtime placed in it, the checklist you hand a platform team, a `terraform/` scaffold that names every resource an agent needs, and the three-line setup answer for interviews.

---

## 1. Three tiers of ownership

### The organisation and folders

The enterprise GenAI blueprint (I1, dated 2024-03-28, old but still the reference architecture) puts folders `common`, `development`, `non-production` and `production` under the org; org policies come from the Security Command Center "secure AI, extended" posture; Terraform is `GoogleCloudPlatform/terraform-google-enterprise-genai`. The platform team owns this tier. You inherit it.

### The environment projects inside the perimeter

One VPC-SC perimeter around each environment's projects, one PSC endpoint per Shared VPC (I1). The AI platform team owns the perimeter, the Shared VPC, the restricted-VIP path, the KMS key rings and the floor settings (F2). Shared by several workloads.

### Your workload project

Agent Runtime resources (`reasoningEngines`), Sessions and Memory Bank, the Toolbox MCP server on Cloud Run, the Agent Search data store, your pipeline. Everything in this tier is created by code: `adk deploy agent_engine`, `agentplatform.Client().runtimes`, or `google_vertex_ai_reasoning_engine` (C2, A5, I8).

Mermaid `flowchart TB`: org (org policies, floor settings) → folder `production` → VPC-SC perimeter (restricted VIP, PSC, KMS) → project (Agent Runtime, Sessions, Memory Bank, Cloud Run Toolbox, Agent Search). One sentence: notice that the perimeter, not a VPC, is the boundary around a managed service.

### Who decides what

Table: decision / platform team / AI platform team / you. Rows: org and folder layout; org-policy set (`vertexai.allowedModels`, `gcp.restrictEndpointUsage`); perimeter membership and ingress rules; Shared VPC and the network attachment; KMS keys; Model Armor floor settings; project and region; IAM on the project; agent definitions and revisions; Toolbox `tools.yaml`; observability dashboards.

**Interview line.** Study check with answer. Rule to keep: _you own the project's contents, not the perimeter._

## 2. Region and endpoint choice

### Regional, multi-regional, global

Agent Runtime is supported in 24 regions including `europe-west2`; Sessions and Memory Bank also on the multi-regions `us` and `eu` and on `global` (A9, GA 17 Jun 2026 per A2). Table: endpoint / what runs there / residency statement / CMEK. The rule: a UK bank picks `europe-west2` for the Runtime and `eu` at most for Sessions and Memory Bank.

### The CMEK constraint

CMEK is not available with `global` or multi-regional endpoints (A9); Sessions and Memory Bank CMEK is unsupported on `global` (F5). So "CMEK mandated" decides the endpoint question before anyone argues latency.

### Gemini Enterprise app location must match

If the agent is registered into a Gemini Enterprise app, the app location `global`/`us`/`eu` must match the Runtime's region prefix (C8). Decide this with the region, not after.

**Interview line.** Study check with answer. Rule to keep: _CMEK and residency pick the endpoint; latency only breaks ties._

## 3. The VPC Service Controls perimeter and the no-egress rule

### What goes in the perimeter

Add `aiplatform.googleapis.com`, which includes Agent Runtime, to the perimeter's restricted services; reach the restricted VIP through Private Google Access or PSC; Runtime projects must join the perimeter before any agent is deployed (I2). The security controls matrix (F4) says VPC-SC, CMEK and data residency are supported for Runtime, Evals, Sessions, Memory Bank and Code Execution, not for Example Store, and not for preview models.

### Ingress for the Runtime service agent

The perimeter needs an ingress rule for `service-PROJECT_NUMBER@gcp-sa-aiplatform-re.iam.gserviceaccount.com` (F4). The dedicated Agent Runtime VPC-SC page could not be fetched on 25 Oct 2026 (map Gaps), so the exact rule shape is unverified.

### No internet egress

Inside the perimeter Agent Runtime has no internet egress; outbound calls go through a proxy VM with Cloud NAT (I2). _Where it goes wrong:_ the ticket agent's Toolbox URL is a public Cloud Run URL and the first production call times out. The fix is the PSC interface (§4) and a Toolbox reachable on the attached network, not an egress exception.

**Interview line.** Study check with answer. Rule to keep: _a managed runtime in a perimeter has no internet; design the tool path before the agent._

## 4. The PSC interface

### The network attachment

A network attachment in your project, `/28` minimum, with DNS peering configs; set on the agent as `psc_interface_config{network_attachment, dns_peering_configs[domain, target_project, target_network]}` (I3, I7). It cannot be changed without recreating the agent (I3), which also means a new Agent Identity principal (D10).

### Sizing

Size the subnet for every agent and revision that will attach, not for one; unverified beyond the `/28` minimum, so the platform team sets it.

**Interview line.** Study check with answer. Rule to keep: _the attachment is a create-time decision; ask for it before the first deploy._

## 5. Customer-managed encryption keys

### Coverage

CMEK covers Runtime source, images, instances and sandboxes via `encryptionSpec.kmsKeyName`; the key ring must be in the same region (F5). In the SDK the config key is `encryption_spec` (I7).

### The IAM side

Grant `roles/cloudkms.cryptoKeyEncrypterDecrypter` to `service-PROJECT_NUMBER@gcp-sa-aiplatform.iam.gserviceaccount.com` (I4). Note this is the `aiplatform` service agent, not the `aiplatform-re` one in §3.

**Interview line.** Study check with answer. Rule to keep: _same region as the key ring, and the platform service agent holds the key role._

## 6. The org-policy baseline

### Model access

`constraints/vertexai.allowedModels` with values like `publishers/google/models/gemini-3.5-flash:predict` (actions predict|deploy|tune, at most 500 values); `vertexai.allowedPartnerModelFeatures` for partner models; `gcp.restrictEndpointUsage` to block the `global` endpoint (F6).

### Where policy is enforced

Table: control / enforced by / evidence. Rows: allowed models (org policy); endpoint (org policy); prompt and response screening (Model Armor floor setting, `INSPECT_AND_BLOCK`, F2); tool reach (perimeter and PSC); who can deploy (IAM). The agent's instructions describe behaviour; the layers above enforce it.

**Interview line.** Study check with answer. Rule to keep: _policy is enforced in org policy, IAM and the perimeter, never only in the prompt._

## 7. IAM for agents and the two service agents

### Roles the set-up page names

`roles/aiplatform.user`, `roles/aiplatform.reasoningEngineServiceAgent`, `roles/aiplatform.agentDefaultAccess`, `roles/aiplatform.agentContextEditor`, `roles/iam.serviceAccountUser`, `roles/iam.serviceAccountTokenCreator`, `roles/storage.admin`, `roles/artifactregistry.reader`; APIs `aiplatform`, `storage`, `logging`, `monitoring`, `telemetry`, `cloudtrace`, `cloudresourcemanager` (I6).

### The two service agents

Table: service agent / what it does / roles it needs. `service-PROJECT_NUMBER@gcp-sa-aiplatform-re.iam.gserviceaccount.com` (Runtime; `reasoningEngineServiceAgent`, `artifactregistry.reader` for custom images, perimeter ingress; I6, I8, F4). `service-PROJECT_NUMBER@gcp-sa-aiplatform.iam.gserviceaccount.com` (platform; `cloudkms.cryptoKeyEncrypterDecrypter` for CMEK, `modelarmor.user` for floor settings; I4, F2).

### The agent's own identity

`identity_type=AGENT_IDENTITY` gives the agent a SPIFFE principal instead of a service account; default roles `agentContextEditor` and `agentDefaultAccess`; agent-to-agent calls need `roles/agentregistry.viewer` and `roles/aiplatform.user` (C5). Service accounts remain the fallback when unset. Detail in G04.

**Interview line.** Study check with answer. Rule to keep: _two service agents, one agent principal; know which role goes to which._

## 8. Audit logging

### What is on by default

Service `aiplatform.googleapis.com`: Admin Activity and System Event logs are always on; Data Access logs must be enabled; readers need `roles/logging.privateLogViewer` (F8). The review board wants Data Access on for the Runtime project from day one, and the central log sink is the platform team's.

**Interview line.** Study check with answer. Rule to keep: _Data Access logs are off until someone turns them on._

## 9. Infrastructure as code for the three tiers

### What goes where

Table: object / tool / lives in. Org policies, perimeter, KMS, network attachment: Terraform in the platform repo (I1). Agent Runtime resource: `google_vertex_ai_reasoning_engine` (provider ≥5.28.0; google-beta for `agent_gateway_config`, which needs `identity_type="AGENT_IDENTITY"`) with `spec.agent_framework`, `spec.package_spec{python_version, pickle_object_gcs_uri, requirements_gcs_uri}`, `spec.service_account`, `spec.deployment_spec{env, secret_env}`, `spec.container_spec.image_uri`, `spec.source_code_spec`; `depends_on` the `roles/artifactregistry.reader` binding to avoid IMAGE_PULL_BACKOFF (I8). Knowledge and guardrails: `google_discovery_engine_data_store`, `google_discovery_engine_search_engine`, `google_model_armor_template`, `google_model_armor_floorsetting` (I8). Agent code and revisions: `adk deploy agent_engine` or the SDK, in the workload pipeline (G02).

### The scaffold in `terraform/`

[`terraform/main.tf`](terraform/main.tf) and [`terraform/variables.tf`](terraform/variables.tf) name the APIs, the IAM bindings for the two service agents, the KMS key reference, the network attachment and one `google_vertex_ai_reasoning_engine` for `ticket-agent`, each block with a `TODO(learner)`. Read it, do not apply it; the pickle and requirements objects it points at do not exist until G03 lab 02.

### Reading IaC without authoring it

The architect's bar: open the Terraform, name every block, change a variable or IAM binding, run `terraform plan`, review the PR.

**Interview line.** Study check with answer. Rule to keep: _nothing in production was clicked._

## 10. Placing the ticket agent in a client's estate

### Walkthrough table

One request from the user to the ticket lookup: step / what happens / which tier owns the control / what evidence proves it. Org policy allows `gemini-3.5-flash:predict` in `europe-west2`; the Runtime's SPIFFE principal calls Toolbox over the PSC interface; Toolbox checks `roles/run.invoker` (D8); the Postgres query returns; the trace lands in Cloud Trace (E4); the Data Access log records the `:query` call.

### What to hand the platform team

Checklist: project in the perimeter; ingress rule for the `-re` service agent; network attachment with DNS peering; KMS key in region plus the key role; org-policy values; roles for your deployer identity; Data Access logs on; Model Armor floor setting.

### When not to

Small internal pilot with no private data: one project, no perimeter, `identity_type=AGENT_IDENTITY` still on, with a written path to the perimeter in the ADR.

## 11. In N lines

Numbered summary, to be written last.

## 12. What you should be able to explain

Three tiers; why CMEK picks the endpoint; what "no internet egress" means for tools; the PSC interface as a create-time choice; the two service agents and their roles; which audit logs are off by default; what is Terraform and what is `adk deploy`.
## 13. What this is not

Not a VPC-SC build guide; not a Terraform tutorial; not the identity chapter (G04 lab 01); not the governance chapter (G05, G09).
## 14. Scope and versions

Map read 25 Oct 2026: A9, F4, F5, F6, F8, I2, I3, I4, I6, I8 dated 2026-10-22; I1 dated 2024-03-28. Not fetched: the Agent Runtime VPC-SC page, pricing (A11). Terraform provider ≥5.28.0; nothing applied.
## 15. Further reading

- I1 Enterprise GenAI blueprint: https://docs.cloud.google.com/architecture/blueprints/genai-mlops-blueprint
- I2 VPC Service Controls: https://docs.cloud.google.com/vertex-ai/docs/general/vpc-service-controls
- I3 PSC interface for Agent Runtime: https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/private-service-connect-interface
- F4 Security controls matrix: https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale
- F5 CMEK: https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/general/cmek
- I4 CMEK IAM: https://docs.cloud.google.com/vertex-ai/docs/general/cmek
- F6 Org policies for model access: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/control-model-access
- I6 Agent Runtime set-up: https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/setup
- F8 Audit logging: https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/general/audit-logging
- I8 Terraform for Agent Runtime: https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/use-terraform
- A9 Supported locations: https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/agent-locations

Status: skeleton, 25 Oct 2026. Nothing deployed; design proposal.
