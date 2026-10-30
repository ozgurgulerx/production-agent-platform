# Customer-managed keys and network (F9, F10, C11)

**CMK.** Power Platform customer-managed key on a Managed Environment covers agent definitions, snapshots, telemetry and conversation data in Dataverse. It does **not** cover Agent 365 audit telemetry; Customer Lockbox excludes Purview audit and Agent 365 events. Steps: Key Vault with soft delete and purge protection → enterprise policy (ARM resource `Microsoft.PowerPlatform/enterprisePolicies`, kind Encryption) → PPAC → environment → Manage encryption. Not done in the lab unless the tenant already has an enterprise policy; record the decision.

**IP firewall** (preview). Applies to web chat and the API only; Teams and M365 Copilot traffic is not filtered. PPAC → environment → Settings → Product → Privacy + Security → IP firewall. Add your office range, test from a phone network: web chat refused, Teams still works. Revert: disable.

**VNet.** VNet support for the HTTP and Application Insights connectors was announced in preview in May 2025 (F16); its current state was not verified on 25 Oct 2026. Entra network egress and ingress controls for agents arrive through Agent 365 (C11). Say to a reviewer: no private endpoint equivalent to Foundry's agent subnet or AgentCore's VPC mode exists for the Copilot Studio runtime itself.
