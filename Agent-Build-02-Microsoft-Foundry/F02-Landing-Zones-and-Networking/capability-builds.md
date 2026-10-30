# F02 capability builds — Infrastructure, Terraform and networking

## Build contract

Status: **planned; functionality unverified**. Build one capability at a time using the existing module and labs. Record environment/dependency versions, permitted assistance, positive and negative results, and trace/test evidence. The learner writes code and tests; these contracts do not supply hidden implementations. Verify dated API and availability claims before execution.

### Author reproducible infrastructure

- [ ] Build: Use an isolated lab resource group. Author Terraform azurerm/azapi for account/project, selected model, identity, Search/Storage, diagnostics and network dependencies; inspect plan before apply and demonstrate destroy/recreate. Retain a Bicep equivalent or comparison for C17. Current build intent includes hands-on Terraform; the original awareness-only source text remains provenance.
- [ ] Verify: Show a no-op second plan, drift detection, failed configuration validation and scoped teardown. Do not use production resources to learn state recovery; explain backend state, locking, imports and secret handling.

### Private connectivity and DNS

- [ ] Build: Record source/destination/DNS/address/port/auth for every PaaS hop. Configure private endpoints and required private DNS, control egress, and separate ingress privacy from outbound restrictions.
- [ ] Verify: Demonstrate private resolution and successful allowed traffic, then denied public traffic and a DNS failure diagnosed without broadening roles.

### Landing-zone policy and residency

- [ ] Build: Separate enterprise-owned hub/policy resources from workload-owned resources. Assign applicable region/public-access/diagnostic policies and document exemptions. Verify service-specific model/tool region availability.
- [ ] Verify: Attempt one policy-denied deployment and inspect the result; show intended resource and inference residency separately. Connect F10 governance evidence to actual F02 policy assignments.

## Exact checklist targets

Each ID below is a distinct occurrence in the [full coverage matrix](../reference/production-build-coverage.md). Source wording is retained, including historical names and unfinished placeholders; it is not a fresh API guarantee. Compound items may require several small builds. Mark complete only after recording evidence.

- [ ] **CB006** — Bicep for the reference architecture: Foundry resource and project, model deployments, AI Search, Storage, Key Vault, Cosmos, Container Apps environment and app with managed identity, role assignments (`Microsoft.Authorization/roleAssignments` with role definition ids), private endpoints and private DNS zones, APIM with policies, Log Analytics and App Insights, Azure Policy assignments; `az deployment group what-if`; parameter files per environment. Terraform (azurerm / azapi) is off the study plan but you must read it, since many clients mandate it (Uniting People, Full Stack Engineer ads).
- [ ] **CB007** — Exercise: deploy A3's infrastructure from Bicep with no portal clicks; destroy and redeploy.
- [ ] **CB065** — Data residency requirements
- [ ] **CB154** — Private inbound endpoint + isolated outbound networking.
- [ ] **CB190** — Hub-spoke, Azure Virtual Network Manager, private endpoints and Private DNS zones for OpenAI, Search, Storage, Key Vault, Cosmos, Container Apps; Azure Firewall egress with FQDN rules; Front Door + WAF; no public endpoints on PaaS; ExpressRoute/VPN for on-prem; managed VNet for Foundry hub/projects; Container Apps environment VNet integration; AKS private cluster.
- [ ] **CB191** — Landing-zone accelerators (ALZ, AI landing zone), policy as code (Azure Policy initiatives for AI: deny public network access, require CMK), management groups, subscription vending.
- [ ] **CB192** — Data residency: UK South / UK West pairing, EU Data Boundary, where Global Standard routes inference.
- [ ] **CB223** — Reconcile Terraform hands-on scope with Source B C17's awareness-only wording; retain Bicep too.

- [ ] **TOP-TERRAFORM** — Author, plan, apply, inspect drift and destroy a scoped Terraform deployment; retain Bicep comparison.

## Completion evidence

- [ ] Store the artifact path, reproducible command, observed outcome, limitations and next gap in the existing study log.
- [ ] Preserve current labs; link to shared concepts rather than importing another stage’s implementation.
- [ ] Do not label a sample, empty test collection or planned experiment as verified functionality.
