# Landing zones for production Foundry agents

[Capability builds and exact checklist targets](capability-builds.md#build-contract)

Updated curriculum guidance — 30 October 2026. Scores are **unassessed**; retained labs are **not newly runtime-verified**. See the [depth and preservation contract](../reference/curriculum-mapping.md).

## Applied networking study path

A landing zone assigns ownership and controls; a private endpoint supplies a private destination for a supported service. Neither alone proves the entire request stays on an approved path. For the ticket agent, trace the caller to gateway, agent to model, agent to Search, and tool to its business backend independently. Identify who resolves each name, which identity reaches the endpoint, and what leaves the approved boundary.

Start with a table of source, destination, DNS name, resolved address, transport, authentication, egress policy and evidence. A DNS failure and an RBAC denial require different remedies: establish name resolution and reachability before changing roles. A private endpoint does not grant data-plane access. Avoid disabling security controls merely to make a smoke test pass.

Compare a minimal sandbox with the regulated-client target. Explain what an enterprise platform team owns: address space, hub DNS/firewall, subscription policy and shared logs. Your workload owns resource configuration and its access requirements. Treat managed-network and customer-network options as service-specific alternatives; the historical skeleton below is not an assertion that all Foundry generations share one topology.

Learner exercise: annotate the existing deployment Bicep, then design a parameterised private endpoint/DNS addition and review its what-if output before an explicitly authorised deployment. Submit an ownership matrix, per-hop path table and a troubleshooting runbook. Diagnose public DNS resolution, blocked egress, wrong identity and unavailable regional capability separately. Completion requires explaining residency of inference, storage, logs and recovery—not just selecting a region.

References: local `documentation/INDEX.md` Foundry networking collection; [baseline architecture](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-chat), [landing-zone variant](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone). Source capabilities must be checked for the chosen deployment.

## Retained chapter material

The following material is preserved with its original scope and dates. Historical module-number references refer to the [migration mapping](../reference/curriculum-mapping.md#repository-preservation-and-migration-rules); current navigation uses folder links.

# Landing zones for production Foundry agents

Status: skeleton, 25 Oct 2026. Headings fixed; each `###` carries a one-line scope note to be replaced by prose. Suggested home: S01 Production AI App Architecture, deployment topologies chapter, or the opening of S_AF03.01. Running scenario: the support-ticket agent and its MCP server, deployed for a UK bank.

## Opening

### The aim
One paragraph: a Foundry agent in production is three layers of ownership stacked on one another. The enterprise landing zone (platform team), the AI landing zone spoke (shared AI platform), and your workload inside it. Most "production" failures are a layer-boundary mistake, not an agent mistake.

### What we are trying to avoid
One-line scenes: the agent that works in the Basic setup and fails the review board because its MCP server has public ingress; the project created by clicking that nobody can rebuild; the model deployment in a region the data-residency policy forbids; the Private DNS zone missing so every private endpoint resolves to the public IP; the subnet too small so the agent runtime stops scaling at 25 sessions.

### Has this happened?
Two or three real incidents of public-ingress or misconfigured-network AI services, fetched and dated on the writing day. Candidates to look up: exposed Azure OpenAI keys in public repos; the 2025 MCP server exposure scans (Knostic, Trend Micro); a bank's cloud-config fine. Not from memory.

### What the chapter covers
The three tiers, who owns what, the Foundry-specific constraints a landing zone has to accommodate, the policy baseline a regulated client applies, and how the Standard-setup sample maps onto a client's hub-and-spoke.

### What you have at the end
A one-page ownership matrix, a hub-and-spoke diagram with Foundry placed in it, the checklist you hand a platform team, and the three-line setup answer for interviews.

## 1. Three tiers of ownership

### The enterprise landing zone
Cloud Adoption Framework scaffold the client already has: management groups, subscription vending, hub-and-spoke or Virtual WAN, central Firewall and DNS, Entra and RBAC model, Azure Policy baseline, central Log Analytics. You inherit it.

### The AI landing zone spoke
The CAF AI-adoption pattern: a spoke subscription for Foundry with private endpoints on every dependency, the agent subnet, egress through the hub firewall, APIM as AI gateway, App Insights feeding the central workspace, Defender for Cloud and Purview. Shared by several workloads.

### Your workload
Foundry project, model deployments, agents and toolboxes, your MCP server on Container Apps, your pipeline. The Standard-setup Foundry sample is this tier with the hub assumed away.

Mermaid `flowchart TB`: hub (firewall, DNS, Log Analytics) → AI spoke (Foundry account, private endpoints, agent subnet, APIM, App Insights) → workload (project, agent, toolbox, MCP container). One sentence: notice that nothing in the workload tier has a public IP.

### Who decides what
Table: decision / platform team / AI platform team / you. Rows: subscription and management group; hub networking and firewall rules; Private DNS zones; Azure Policy set; Foundry account and network posture; agent subnet sizing; model deployments and quota; identities and RBAC; APIM policies; agent and toolbox definitions; observability dashboards.

**Interview line.** Study check with answer. Rule to keep: *you own the spoke's contents, not the hub.*

## 2. Why the landing zone matters for Foundry specifically

### Basic versus Standard setup
Basic: Microsoft-managed storage, public endpoints, no private MCP. Standard: bring your own Storage, Cosmos, AI Search, VNet injection, private MCP, Azure Functions tool. Table of what each allows; the rule that private data means Standard.

### The agent subnet
Delegated to `Microsoft.App/environments`, /24 recommended, /27 minimum, not shareable, name limit; the data proxy and hosted-agent micro-VMs live here; capacity falls under load (deep-dive page figures, cite). *Where it goes wrong:* the /27 that stops scaling.

### Private DNS and private endpoints
The zones Foundry needs (account, project, Storage, Cosmos, Search, Key Vault, Container Apps environment); who creates them (platform team, hub-linked); the symptom when one is missing.

### Egress and the firewall
Foundry outbound FQDN allow-list from the private-networking page; the MCP server's own egress; third-party MCP servers as a data-boundary decision, not a network one.

### Identity
Project managed identity, agent identities as Entra service principals, Foundry role rename (Azure AI User → Foundry User), Foundry Agent Consumer for toolbox callers, no key-based connections. Cross-link to the MCP auth chapter.

### Model and tool availability by region
Tool-by-region matrix and model regions constrain the spoke's region; data-residency policy constrains it the other way. *Micro-example:* code interpreter absent in the chosen region.

**Interview line.** Study check with answer. Rule to keep: *the landing zone has to know Foundry's shape before the first agent exists.*

## 3. The policy baseline a regulated client applies

### Azure Policy set
Table: policy / effect / why the risk team wants it. Rows: allowed regions; public network access disabled; local authentication disabled; private endpoints required; diagnostic settings required; required tags; allowed model deployments or SKUs; customer-managed keys where mandated.

### Governance hooks
Defender for Cloud AI posture, Purview for data classification and the Purview middleware, APIM request logging with redaction, Azure Policy compliance as review-board evidence. Cross-link to the governance chapter (S07) and the security chapter (S08).

### Where policy is enforced
*Policy is enforced in code, never only in the prompt* restated at infrastructure level: the firewall, Policy, RBAC and APIM enforce; the agent's instructions only describe.

**Interview line.** Study check with answer. Rule to keep.

## 4. Infrastructure as code for the three tiers

### What goes where
Table: object / tool / lives in. Bicep or Terraform for ARM resources; Projects SDK, `azd ai` or REST for agents, toolboxes, connections, skills, evaluations; Agent Framework or LangGraph for the loop; azd or a pipeline for containers. The one-sentence version: *IaC for resources, SDK for definitions, Framework for the loop.*

### The Foundry samples as a starting point
`infrastructure-setup-bicep` folder: basic, Standard, `11-private-network-basic-vnet`, `19-private-network-agent-tools`. What each provisions; what a bank's platform team would strip out (the hub pieces) and what they would add (policy, tags, central logging).

### Pipeline shape
Dev → test → prod; `what-if` or `terraform plan` gated by approval; OIDC federated credentials, no secrets; agent definitions applied by an SDK step; eval gate before promoting a toolbox or agent version; rollback by version. Mermaid `flowchart LR`.

### Reading IaC without authoring it
The architect's bar: open the Bicep, name every block, change a parameter or role assignment, run `what-if`, review the PR. Not: write modules from scratch.

**Interview line.** Study check with answer. Rule to keep: *nothing in production was clicked.*

## 5. Placing the ticket agent in a client's estate

### Walkthrough table
One request from the user to the refund: step / what happens / which tier owns the control / what evidence proves it. Hub firewall allows the Foundry FQDNs; APIM validates the Entra token; the agent runtime in the subnet calls the MCP server over internal ingress; the agent identity's token reaches the server; the refund is written by the backend; App Insights trace lands in the central workspace.

### What to hand the platform team
Checklist: subnet request with size and delegation; Private DNS zones; firewall FQDNs; policy exemptions needed, if any; identities and roles; regions; quota.

### When not to
Small internal pilot with no private data: Basic setup in a sandbox subscription, with a written path to Standard. Say so in the ADR.

## 6. In N lines

Numbered summary, to be written last.

## 7. What you should be able to explain

Bulleted list of spoken answers: the three tiers; Basic versus Standard; the subnet; the policy set; what goes in Bicep versus the SDK; what you hand the platform team.

## 8. What this is not

Not a landing-zone build guide; not a Bicep tutorial; not the MCP authentication chapter; not the governance pack. Where each lives.

## 9. Scope and versions

Foundry docs read 23–25 Oct 2026 (private networking page dated 2026-08-27, network isolation page 2026-09-29, networking deep dive 2026-09-08, MCP how-to 2026-10-08). CAF and Architecture Center pages: not yet fetched; verify before citing.

## 10. Further reading

Platform guidance
- Cloud Adoption Framework, AI adoption scenario: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/ai/ (not fetched, verify)
- Azure Landing Zones: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/ (not fetched, verify)
- Baseline Azure AI Foundry chat reference architecture: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-azure-ai-foundry-chat (not fetched, verify)

Foundry networking and setup (fetched 23 Oct 2026)
- Set up private networking for Foundry Agent Service: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/virtual-networks
- Configure network isolation for Foundry (agent tools matrix): https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link
- Deep dive into Foundry Agent Service networking: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/agents-networking-deep-dive
- Network isolation for a toolbox: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/toolbox-network-isolation
- Agent identity concepts: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/agent-identity
- Quotas, limits, regions: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions

Code to read
- Foundry samples, Bicep infrastructure: https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep
- OpenAI end-to-end baseline (Bicep for the reference architecture): https://github.com/Azure-Samples/openai-end-to-end-baseline (not fetched, verify)
- Azure Verified Modules: https://github.com/Azure/bicep-registry-modules

Learning
- Fundamentals of Bicep: https://learn.microsoft.com/en-us/training/paths/bicep-deploy
- Bicep documentation: https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/
- Terraform on Azure (for later): https://developer.hashicorp.com/terraform/tutorials/azure-get-started ; azapi provider: https://registry.terraform.io/providers/Azure/azapi/latest/docs

Status: skeleton, 25 Oct 2026. Nothing deployed; design proposal.
