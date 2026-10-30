# F03 capability builds — Identity and permission boundaries

## Build contract

Status: **planned; functionality unverified**. Build one capability at a time using the existing module and labs. Record environment/dependency versions, permitted assistance, positive and negative results, and trace/test evidence. The learner writes code and tests; these contracts do not supply hidden implementations. Verify dated API and availability claims before execution.

### Developer, workload and agent principals

- [ ] Build: Implement an Entra-authenticated client and identify the principal used locally and in runtime. Explain app registration vs service principal, system/user-assigned identity and agent identity. Use scoped RBAC instead of copying developer credentials.
- [ ] Verify: Demonstrate allowed operation, wrong audience, missing role and expired credential; retain safe correlation IDs without bearer tokens.

### Delegation and consent

- [ ] Build: Compare OBO/delegated access with application permissions for the same downstream task. Record scopes, audience, consent owner, token exchange and per-call authorization. Explain OIDC/OAuth/SAML, PKCE, client credentials, CA and PIM scope.
- [ ] Verify: Use two synthetic users to prove access isolation and revocation; route durable approvals to F06 and M365-specific licensing/access to F11.

### Federation and data-plane roles

- [ ] Build: Configure a bounded CI federated identity exercise and produce principal-resource-role matrix for model, Search, Storage and Key Vault. Implement token acquisition through maintained SDKs.
- [ ] Verify: Test a valid token for the wrong resource and insufficient data-plane role. Explain why control-plane Contributor does not establish every data-plane entitlement.

## Exact checklist targets

Each ID below is a distinct occurrence in the [full coverage matrix](../reference/production-build-coverage.md). Source wording is retained, including historical names and unfinished placeholders; it is not a fresh API guarantee. Compound items may require several small builds. Mark complete only after recording evidence.

- [ ] **CB062** — Foundry Model Endpoints - keyless authantication with Microsoft Entra ID...~[link](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/endpoints?tabs=python)~
- [ ] **CB064** — RBAC integration - who can call which model deployments
- [ ] **CB090** — Entra ID
- [ ] **CB091** — user identity
- [ ] **CB092** — app registrations
- [ ] **CB093** — managed identities
- [ ] **CB094** — agent identity
- [ ] **CB101** — Agent identity and access [link](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/identity-access-overview)
- [ ] **CB102** — Azure RBAC permission bundles for Microsoft Foundry -
- [ ] **CB103** — Foundry User, Foundry Owner, Foundry Account Owner, and Foundry Project Manager
- [ ] **CB106** — OIDC vs OAuth 2.0 vs SAML in one line each; when SAML still appears (legacy enterprise SSO, federation), why OIDC for apps and agents.
- [ ] **CB107** — Entra ID: app registrations, service principals, managed identities (system vs user-assigned), workload identity federation (GitHub Actions → Azure without secrets), on-behalf-of flow, client credentials, PKCE for public clients, token audiences and scopes, Conditional Access, Privileged Identity Management.
- [ ] **CB108** — Agent identity design: the agent has its own identity; tools are called with the user's delegated token (OBO) or the agent's identity with scoped RBAC; per-call authorisation; consent and admin consent for tool scopes; token lifetime and revocation; Entra Agent ID concepts.
- [ ] **CB110** — Zero Trust planes: identity (strong auth, CA), device (compliance), network (private endpoints, no public ingress, NSG/ASG, Azure Firewall egress allow-list), application (APIM policies, WAF on Front Door / App Gateway), data (classification, Purview, CMK, RBAC on indexes), visibility (Sentinel, Defender).
- [ ] **CB111** — RBAC on data planes: Azure OpenAI roles, AI Search roles, Storage data roles, Key Vault RBAC vs access policies; security-trimmed retrieval (filter on group claims / ACLs in the index).
- [ ] **CB112** — OIDC vs OAuth 2.0 vs SAML in one line each; when SAML still appears (legacy enterprise SSO, federation), why OIDC for apps and agents.
- [ ] **CB113** — Entra ID: app registrations, service principals, managed identities (system vs user-assigned), workload identity federation (GitHub Actions → Azure without secrets), on-behalf-of flow, client credentials, PKCE for public clients, token audiences and scopes, Conditional Access, Privileged Identity Management.
- [ ] **CB114** — Agent identity design: the agent has its own identity; tools are called with the user's delegated token (OBO) or the agent's identity with scoped RBAC; per-call authorisation; consent and admin consent for tool scopes; token lifetime and revocation; Entra Agent ID concepts.
- [ ] **CB116** — Zero Trust planes: identity (strong auth, CA), device (compliance), network (private endpoints, no public ingress, NSG/ASG, Azure Firewall egress allow-list), application (APIM policies, WAF on Front Door / App Gateway), data (classification, Purview, CMK, RBAC on indexes), visibility (Sentinel, Defender).
- [ ] **CB117** — RBAC on data planes: Azure OpenAI roles, AI Search roles, Storage data roles, Key Vault RBAC vs access policies; security-trimmed retrieval (filter on group claims / ACLs in the index).
- [ ] **CB118** — `DefaultAzureCredential`, `ManagedIdentityCredential` (system and user-assigned, client_id), `AzureCliCredential`, `ClientSecretCredential` only for tests, `OnBehalfOfCredential`, `WorkloadIdentityCredential` for AKS and GitHub Actions federation; `get_token(scope)` and the scope strings you must know: `https://cognitiveservices.azure.com/.default`, `https://search.azure.com/.default`, `https://ai.azure.com/.default`, `https://graph.microsoft.com/.default`, `https://vault.azure.net/.default`.
- [ ] **CB119** — `get_bearer_token_provider(credential, scope)` to feed the OpenAI client without keys.
- [ ] **CB120** — Exercise: an httpx client that calls Azure OpenAI with a managed identity token, refreshes it, retries 429/5xx with jitter, and never logs the token. 25 minutes, tests with a fake token provider.
- [ ] **CB153** — Entra identity + least-privilege RBAC; test denied access.

## Completion evidence

- [ ] Store the artifact path, reproducible command, observed outcome, limitations and next gap in the existing study log.
- [ ] Preserve current labs; link to shared concepts rather than importing another stage’s implementation.
- [ ] Do not label a sample, empty test collection or planned experiment as verified functionality.
