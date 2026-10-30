# A3 least-privilege matrix

Companion to [F03 Section 6](README.md#6-least-privilege-on-the-data-planes). **Proposed, not applied.** Fill the blanks, apply each row with `az role assignment create --assignee-object-id <oid> --assignee-principal-type ServicePrincipal --role "<role>" --scope <scope>`, then record one permitted and one denied run per row that has a negative case. A row is done when its evidence column links to a redacted log line in the study log. Role names are from the vendor pages read 30 October 2026; verify before applying.

## Principals

| Principal | Kind | Object ID | Sponsor |
|---|---|---|---|
| Ayşe | User (support agent) | | |
| Mert | User (supervisor) | | |
| Ticket assistant web app | App registration, confidential client | | |
| Refund agent | Agent identity | | |
| Triage agent | Agent identity | | |
| Ticket MCP server | User-assigned managed identity (Container Apps) | | |
| Retrieval service | User-assigned managed identity | | |
| Indexer | Foundry account / Search service identity | | |
| CI deploy | Federated credential, subject `repo:ozgurgulerx/production-agent-platform:environment:prod` | n/a | |

## Assignments

| Principal | Resource | Role or permission | Scope | Why this and not more | Negative case to run | Evidence |
|---|---|---|---|---|---|---|
| Web app | Foundry project | `Foundry Agent Consumer` | Project | It only invokes agents; it never builds them | Call a management endpoint, expect `403` | |
| Refund agent | Ticket API (Entra app) | App role `Tickets.Read`, `Refunds.Execute` | API | Only this agent may refund | Triage agent calls `issue_refund`, expect `403` | |
| Triage agent | Ticket API (Entra app) | App role `Tickets.Read` | API | Reads to classify; no writes | Same call as above, from this agent | |
| Ayşe | Ticket API (Entra app) | Delegated `tickets.read` | API, admin-consented | Her job is reading tickets | `issue_refund` as Ayşe, expect `403 insufficient_scope` | |
| Mert | Ticket API (Entra app) | Delegated `tickets.read tickets.refund` | API, admin-consented | Supervisor approves refunds | Refund above policy limit, expect `policy_denied`, no effect | |
| Ticket MCP server | Graph | Delegated `Calendars.Read` via OBO | Tenant, admin-consented | Only to read the caller's own calendar | Redeem a Graph-audience token, expect `AADSTS50013` | |
| Retrieval service | AI Search index | `Search Index Data Reader` | Index | Query only; filters do the rest | Attempt an index write, expect `403` | |
| Indexer | Blob container | `Storage Blob Data Reader` | Container | Reads source documents | Write to the container, expect `403` | |
| Indexer | AI Search | `Search Index Data Contributor` or `Search Service Contributor` | Service or index | Loads documents / runs indexers; pick one and justify | Retrieval service attempts a write | |
| Refund agent, web app | Azure OpenAI | `Cognitive Services OpenAI User` | Resource | Inference only; keys disabled on the resource | Call with keys disabled and no role, expect `401` | |
| Ticket MCP server | Key Vault | `Key Vault Secrets User` | The one vendor secret | Reads `fx-rates` key; nothing else | Read a second secret, expect `403` | |
| CI deploy | Resource group | Environment-limited deployment role | RG | Deploys only this environment | Fork PR workflow, expect federated subject mismatch | |
| Audit reader | Log Analytics | `Log Analytics Reader` under PIM | Workspace | Time-bound, approved | Query without activation, expect denial | |

## Rules this matrix encodes

- One identity per agent; the project managed identity appears in no row.
- No principal holds a role on a resource it does not call.
- Every write permission has a named negative case from a principal that must not have it.
- Control-plane roles (`Contributor`, `Owner`) appear nowhere on data paths; `Cognitive Services Contributor` is explicitly excluded because it exposes keys and cannot infer.
- The secret count is one.

## Log

| Date | Row | Command | Outcome | Gap |
|---|---|---|---|---|
| | | | | |
