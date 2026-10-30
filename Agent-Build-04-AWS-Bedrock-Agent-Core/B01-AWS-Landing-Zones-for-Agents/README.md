# Landing zones for production AgentCore agents

Status: skeleton, 25 Oct 2026. Headings fixed; each `###` carries a one-line scope note to be replaced by prose. Mirror of `../../Agent-Build-02-Microsoft-Foundry/F02-Landing-Zones-and-Networking/`. Running scenario: the UK support-ticket agent and its MCP server, deployed for a UK bank, on AWS. Facts come from the reading map [`../reference/reading-map-agentcore-2026-10-25.md`](../reference/reading-map-agentcore-2026-10-25.md); letters such as F9 or D2 refer to it. Nothing deployed.

## Opening

### The aim

One paragraph: an AgentCore agent in production is three layers of ownership stacked on one another. The enterprise landing zone (Control Tower or the Landing Zone Accelerator, owned by the platform team), the AI platform account or accounts (shared AI team), and your workload inside them. **Most "production" failures are a layer-boundary mistake, not an agent mistake**: the runtime that is public because nobody asked for VPC mode, the model enabled in a Region the residency rule forbids, the execution role that carries `BedrockAgentCoreFullAccess`.

> _You own the resources in the AI account, not the organisation around it._

### What we are trying to avoid

One-line scenes: the Runtime created with `networkMode: PUBLIC` that passes the demo and fails the review board because its MCP server has no private path; the Gateway created by clicking in a sandbox account that nobody can rebuild; the `global.` inference profile that sends UK card data through another geography; the account with `BedrockAgentCoreFullAccess` on the execution role, which includes `GetWorkloadAccessTokenForUserId` and can mint a token for any user id (F9); the Policy engine attached in `us-west-2` while the gateway runs in a Region Policy does not cover.

### Has this happened?

Two or three dated incidents to fetch on the writing day: exposed cloud credentials in public repositories; the 2025 MCP server exposure scans; a regulated firm's cloud-configuration fine. Not from memory.

### What the chapter covers

The three tiers, who owns what, the AgentCore-specific constraints a landing zone must accommodate (Regions, VPC, PrivateLink, identity), the policy baseline a regulated client applies, and how the AgentCore CLI's CDK app maps onto a client's multi-account estate.

### What you have at the end

A one-page ownership matrix, an account diagram with AgentCore placed in it, the checklist you hand a platform team, and the three-line setup answer for interviews.

## 1. Three tiers of ownership

### The enterprise landing zone

What the client already has from Control Tower or the Landing Zone Accelerator: Organizations with OUs (Security, Infrastructure, Workloads, Sandbox), service control policies, account vending, IAM Identity Center for people, a network account with Transit Gateway or Cloud WAN, a log-archive account with the organisation CloudTrail, Security Hub and Config aggregators, central KMS conventions. You inherit it.

### The AI platform account(s)

The shared tier: Bedrock model access and the Anthropic use-case form submitted once per account (L7); AgentCore Runtime, Gateway and Memory in VPC mode with PrivateLink endpoints for the control plane (F10, Mar 2026) and VPC egress to private identity providers (Apr 2026); CloudWatch Transaction Search enabled once so GenAI Observability and Evaluations can find spans (H1); the AWS Agent Registry shared across the organisation with RAM, approval workflows on (A8); customer-managed KMS keys on the Identity token vault and the Registry; guardrails and prompt routers owned centrally. Shared by several workloads.

### Your workload

Runtimes (code zip or container), a Gateway with its targets and Cedar policy engine, Lambda tools, Memory, online evaluation configs, and the pipeline. The AgentCore CLI's thin CDK app (`agentcore deploy`, C3) is this tier; it assumes the account and network exist.

Mermaid `flowchart TB`: org (SCPs, Identity Center, network account with Transit Gateway, log archive with CloudTrail) → AI account (PrivateLink endpoints, VPC with private subnets, Transaction Search, Registry, KMS) → workload (Runtime in VPC mode, Gateway, Policy engine, Lambda tools, Memory). One sentence: notice that nothing in the workload tier has a public IP; callers reach the Runtime through the AgentCore data-plane endpoint with SigV4 or a JWT, never through an address you own.

### Who decides what

Table: decision / platform team / AI platform team / you. Rows: OU placement and SCPs; account vending and Identity Center permission sets; network account, Transit Gateway, private subnets and endpoints; organisation CloudTrail and Config rules; Bedrock model access and allowlisted models and Regions; Transaction Search and log retention; Registry and approval workflow; KMS keys; Runtime network mode and execution roles; Gateway targets and Cedar policies; agent code and versions; evaluation configs and dashboards.

**Interview line.** Study check with answer. Rule to keep: _you own the AI account's contents, not the organisation._

## 2. Why the landing zone matters for AgentCore specifically

### Regions decide the design before the agent exists

Policy in 13 Regions (A3), Evaluations in 9 (A4), Harness and Guardrails-in-Policy in 7 (A6, F4), Runtime platform V2 in 5 (B3), GovCloud US-West since May 2026 (A15). The spoke's Region is the intersection of the features you need and the residency rule, chosen once. _Micro-example:_ a gateway in a Region without Policy has no deny-by-default layer and the refund cap lives only in code.

### Inference profiles versus residency

`global.` profiles may route anywhere; `eu.` keeps inference inside the geography; new Claude models offer no in-Region profile (L4). For the UK bank the default in `.env` changes from `global.` to `eu.` and the quota headroom shrinks; the chapter says this out loud (see `../labs-setup/01-models/`).

### Public, VPC and PrivateLink

Runtime and Memory have run in VPC mode since Sep 2025; control-plane PrivateLink for Gateway, Runtime, Memory and tools since Mar 2026; VPC egress for Identity, Gateway and Runtime since Apr 2026 (F10). The data plane is still an AWS endpoint; the condition key `aws:VpceOrgID` on resource policies restricts callers to your organisation's endpoints (F9). _Where it goes wrong:_ a Runtime in PUBLIC mode calling a Lambda tool over the internet because the VPC endpoints were never requested.

### Identity

Three identities per call: the caller (SigV4 role or JWT subject), the Runtime execution role (trusted by `bedrock-agentcore.amazonaws.com` with `aws:SourceAccount` and `aws:SourceArn`, F9), and the workload identity that holds OAuth tokens in the vault (E1). `RuntimeAuthorizerType` lets a resource policy insist on JWT. The warning that recurs in every chapter: `BedrockAgentCoreFullAccess` is for sandboxes. Cross-link to B04 §1–§3 and B09 §5.

### Model and feature availability by Region

Model cards list Regions and profiles (L3); Gateway semantic search is in 18 Regions (D3); Guardrails Standard tier needs a cross-Region guardrail profile (F6). _Micro-example:_ semantic tool search absent in the chosen Region, so the agent carries 60 tools in context.

**Interview line.** Study check with answer. Rule to keep: _the landing zone has to know AgentCore's Region map before the first runtime exists._

## 3. The policy baseline a regulated client applies

### Service control policies

Table: policy / effect / why the risk team wants it. Rows: deny `bedrock:InvokeModel*` outside allowlisted model ARNs and Regions; deny `bedrock-agentcore:GetWorkloadAccessTokenForUserId` to all but a break-glass role; deny Runtime and Gateway creation without required tags; deny public `networkMode` where a condition key exists (verify); deny disabling CloudTrail and Config; require KMS CMK on Memory and token vault (verify key availability). Sketches live in `../B09-AgentCore-Policy-and-Governance/sketches/scp_examples.json`.

### Governance hooks

Organisation CloudTrail with `InvokeAgentRuntime`, `CreatePolicy`, `UpdateGateway` events; Config rules for tags and VPC mode; Security Hub; the Agent Registry approval workflow as the record of who allowed which MCP server (A8); Cedar policy in `LOG_ONLY` before `ENFORCE` as review-board evidence (F1). Cross-link to B09 and to the governance (S07) and security (S08) chapters.

### Where policy is enforced

_Policy is enforced in code, never only in the prompt_ restated at infrastructure level: SCPs, IAM, VPC, the Gateway's Cedar engine and Guardrails enforce; the agent's instructions only describe.

**Interview line.** Study check with answer. Rule to keep.

## 4. Infrastructure as code for the three tiers

### What goes where

Table: object / tool / lives in. Control Tower or LZA for the organisation; CDK or CloudFormation or Terraform for accounts, VPCs, endpoints, roles and KMS; the AgentCore CLI's CDK app (`@aws/agentcore-cdk`, C3) or boto3 `bedrock-agentcore-control` for runtimes, gateways, policies, memories and evaluation configs; Strands or LangGraph for the loop; `agentcore deploy` or a pipeline for code and images. The one-sentence version: _IaC for accounts and network, the control plane for AgentCore objects, the framework for the loop._

### The AgentCore CLI project as a starting point

`agentcore create` scaffolds `agentcore/agentcore.json`, `aws-targets.json`, `.env.local` and, for a Harness, `harness.yaml` (C3). What a bank's platform team would strip out (public network mode, the broad execution role the template proposes) and what they would add (VPC mode, PrivateLink, tags, the central log group, a Cedar engine). Verify the template's default role scope before quoting it.

### Pipeline shape

Dev → test → prod accounts; `cdk diff` gated by approval; GitHub OIDC through `aws-actions/configure-aws-credentials`, no stored keys; AgentCore objects applied by `agentcore deploy --yes` or a boto3 step; Strands Evals and an on-demand AgentCore evaluation as the gate before an endpoint is repointed; rollback by `update_agent_runtime_endpoint` to the previous version (B7). Mermaid `flowchart LR`.

### Reading IaC without authoring it

The architect's bar: open the CDK app or template, name every construct, change a parameter or role statement, read the diff, review the pull request. Not: write constructs from scratch.

**Interview line.** Study check with answer. Rule to keep: _nothing in production was clicked._

## 5. Placing the ticket agent in a client's estate

### Walkthrough table

One request from the user to the refund: step / what happens / which tier owns the control / what evidence proves it. Identity Center or Cognito issues the token; the data-plane endpoint checks the JWT authoriser; the Runtime in VPC mode calls the Gateway; the Cedar engine permits `issue_refund` under 250 GBP; the Lambda tool writes the refund; the span lands in the per-agent log group and the online evaluation samples it.

### What to hand the platform team

Checklist: Region and the feature intersection behind it; account and OU; private subnets, security groups and the PrivateLink endpoints; Transaction Search; model allowlist and the Anthropic use-case form; permission sets and the execution-role trust pattern; KMS keys; Registry sharing; quotas (B12).

### When not to

Small internal pilot with no customer data: a sandbox account, PUBLIC network mode, `global.` profile, with a written path to the AI account. Say so in the ADR.

## 6. In N lines

Numbered summary, to be written last.

## 7. What you should be able to explain

Bulleted list of spoken answers: the three tiers; why the Region is chosen first; VPC mode versus PrivateLink versus the data-plane endpoint; the SCP set; what goes in CDK versus the control plane; what you hand the platform team.

## 8. What this is not

Not a Control Tower build guide; not a CDK tutorial; not the identity chapter (B04); not the governance pack (B09). Where each lives.

## 9. Scope and versions

AgentCore and Bedrock pages read 25 Oct 2026 (reading map A, D, E, F9–F11, L). Control Tower, Landing Zone Accelerator and the Well-Architected Agentic AI Lens: not yet fetched; verify before citing.

## 10. Same thing on Foundry

| AWS                                                           | Foundry (F01)                                                |
| ------------------------------------------------------------- | ------------------------------------------------------------ |
| Control Tower / Landing Zone Accelerator, Organizations, SCPs | CAF enterprise landing zone, management groups, Azure Policy |
| AI platform account(s)                                        | AI landing zone spoke subscription                           |
| IAM Identity Center permission sets                           | Entra groups and RBAC                                        |
| VPC mode + PrivateLink endpoints + `aws:VpceOrgID`            | VNet injection, private endpoints, Private DNS zones         |
| Execution role with `SourceAccount` / `SourceArn` trust       | Project managed identity and agent identities                |
| Inference profile (`eu.` vs `global.`)                        | `DataZoneStandard` vs `GlobalStandard` deployment type       |
| Cedar engine on the Gateway                                   | APIM policies and `require_approval`                         |
| Organisation CloudTrail + Config                              | Diagnostic settings + Azure Policy compliance                |
| Agent Registry approval workflow                              | API Center private catalog                                   |

## 11. Further reading

Platform guidance

- AWS Well-Architected, Agentic AI Lens: https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/ (one page fetched, F8; rest verify)
- AWS Control Tower: https://docs.aws.amazon.com/controltower/ (not fetched, verify)
- Landing Zone Accelerator on AWS: https://aws.amazon.com/solutions/implementations/landing-zone-accelerator-on-aws/ (not fetched, verify)

AgentCore networking, identity and permissions (fetched 25 Oct 2026)

- Runtime permissions and execution role (F9): https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-permissions.html
- Runtime inbound auth (E2): https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-oauth.html
- Policy (F1, F2): https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html
- Gateway core concepts (D1): https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-core-concepts.html
- Quotas (D7, B12): https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html
- Model access (L7): https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html

Code to read

- AgentCore CLI and its CDK app (C2, C3): https://github.com/aws/agentcore-cli
- AgentCore samples: https://github.com/awslabs/agentcore-samples
- B09 sketches: `../B09-AgentCore-Policy-and-Governance/sketches/`

Status: skeleton, 25 Oct 2026. Nothing deployed; design proposal.
