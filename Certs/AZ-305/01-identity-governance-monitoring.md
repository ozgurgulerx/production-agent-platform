# Domain 1: Design identity, governance, and monitoring solutions (25–30%)

## 1.1 Design solutions for logging and monitoring

- [ ] Recommend a logging solution
  - Know how to: Log Analytics workspace design (single vs per-region/per-tenant), table plans (Analytics, Basic, Auxiliary), retention and archive, diagnostic settings, Activity log vs resource logs vs Entra logs.
  - Read: Azure Monitor overview https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview · Workspace design https://learn.microsoft.com/en-us/azure/azure-monitor/logs/workspace-design · Table plans https://learn.microsoft.com/en-us/azure/azure-monitor/logs/data-platform-logs · Diagnostic settings https://learn.microsoft.com/en-us/azure/azure-monitor/platform/diagnostic-settings
- [ ] Recommend a solution for routing logs
  - Know how to: diagnostic settings to workspace / storage / Event Hubs / partner; data collection rules and transformations; Azure Monitor Agent; cross-tenant and SIEM (Sentinel) routing.
  - Read: Data collection rules https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/data-collection-rule-overview · Stream to Event Hubs https://learn.microsoft.com/en-us/azure/azure-monitor/platform/stream-monitoring-data-event-hubs · Microsoft Sentinel data connectors https://learn.microsoft.com/en-us/azure/sentinel/connect-data-sources
- [ ] Recommend a monitoring solution
  - Know how to: Application Insights (workspace-based, OpenTelemetry), VM insights, Container insights, Network Watcher, alerts and action groups, workbooks, Azure Monitor baseline alerts, Service Health, Advisor.
  - Read: Application Insights overview https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview · Alerts overview https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview · Azure Monitor Baseline Alerts https://azure.github.io/azure-monitor-baseline-alerts/ · Well-Architected operational excellence https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/

## 1.2 Design authentication and authorization solutions

- [ ] Recommend an authentication solution
  - Know how to: Entra ID vs Entra External ID (B2B, customers), hybrid identity (cloud sync, PHS, PTA, federation), MFA and passwordless, Conditional Access, Entra Domain Services for legacy Kerberos/LDAP.
  - Read: Hybrid identity options https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/choose-ad-authn · Conditional Access https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview · External ID https://learn.microsoft.com/en-us/entra/external-id/external-identities-overview · Entra Domain Services https://learn.microsoft.com/en-us/entra/identity/domain-services/overview
- [ ] Recommend an identity management solution
  - Know how to: users, groups (dynamic), administrative units, service principals vs managed identities (system vs user-assigned), workload identity federation, app registrations.
  - Read: Managed identities https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview · Workload identity federation https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation · Administrative units https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/administrative-units
- [ ] Recommend a solution for authorizing access to Azure resources
  - Know how to: Azure RBAC scope inheritance, custom roles, deny assignments, ABAC conditions, PIM for just-in-time roles, Entra roles vs Azure roles.
  - Read: Azure RBAC overview https://learn.microsoft.com/en-us/azure/role-based-access-control/overview · Custom roles https://learn.microsoft.com/en-us/azure/role-based-access-control/custom-roles · ABAC conditions https://learn.microsoft.com/en-us/azure/role-based-access-control/conditions-overview · PIM https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-configure
- [ ] Recommend a solution for authorizing access to on-premises resources
  - Know how to: Entra application proxy, Kerberos constrained delegation, Entra Domain Services, Arc-enabled servers with RBAC, Global Secure Access (private access).
  - Read: Application proxy https://learn.microsoft.com/en-us/entra/identity/app-proxy/overview-what-is-app-proxy · Global Secure Access private access https://learn.microsoft.com/en-us/entra/global-secure-access/concept-private-access · Azure Arc servers https://learn.microsoft.com/en-us/azure/azure-arc/servers/overview
- [ ] Recommend a solution to manage secrets, certificates, and keys
  - Know how to: Key Vault tiers, soft delete and purge protection, RBAC vs access policies, Managed HSM vs Dedicated HSM, customer-managed keys, App Configuration for settings, certificate auto-rotation.
  - Read: Key Vault overview https://learn.microsoft.com/en-us/azure/key-vault/general/overview · Managed HSM https://learn.microsoft.com/en-us/azure/key-vault/managed-hsm/overview · Key management in Azure https://learn.microsoft.com/en-us/azure/security/fundamentals/key-management · App Configuration https://learn.microsoft.com/en-us/azure/azure-app-configuration/overview

## 1.3 Design governance

- [ ] Recommend a structure for management groups, subscriptions, and resource groups, and a strategy for resource tagging
  - Know how to: management group hierarchy (platform, landing zones, sandbox, decommissioned), subscription democratisation, resource group as lifecycle boundary, tag inheritance via policy, naming conventions.
  - Read: Azure landing zone design areas https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-areas · Resource organization https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org · Tagging strategy https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-tagging · Naming https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming
- [ ] Recommend a solution for managing compliance
  - Know how to: Azure Policy effects (deny, audit, deployIfNotExists, modify), initiatives, exemptions, regulatory compliance in Defender for Cloud, Blueprints retired in favour of template specs + deployment stacks, Purview for data governance.
  - Read: Azure Policy overview https://learn.microsoft.com/en-us/azure/governance/policy/overview · Policy effects https://learn.microsoft.com/en-us/azure/governance/policy/concepts/effect-basics · Defender for Cloud regulatory compliance https://learn.microsoft.com/en-us/azure/defender-for-cloud/regulatory-compliance-dashboard · Deployment stacks https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deployment-stacks
- [ ] Recommend a solution for identity governance
  - Know how to: Entra ID Governance: entitlement management (access packages), access reviews, lifecycle workflows, PIM for groups, Permissions Management.
  - Read: Entra ID Governance overview https://learn.microsoft.com/en-us/entra/id-governance/identity-governance-overview · Entitlement management https://learn.microsoft.com/en-us/entra/id-governance/entitlement-management-overview · Access reviews https://learn.microsoft.com/en-us/entra/id-governance/access-reviews-overview
