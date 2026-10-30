# 09 — MCP authentication matrix, with APIM AI Gateway in front


**Reference implementation for the `project-managed-identity` row:** the open-source [Azure Cosmos DB MCP ToolKit](https://github.com/AzureCosmosDB/MCPToolKit) (self-hosted on Container Apps via `azd up`, an Entra app registration whose client id is the connection **audience**, the project MI granted MCP Tool Executor, first-use approval in the agent). It is the fully worked version of what this lab's matrix does in one script.

## Goal
Show, with one agent per auth type, which identity an MCP server sees when Foundry calls it, and where API Management fits (rate limits, token validation, logging; not the authorisation boundary).

## Run
```bash
source ../.venv/bin/activate
python mcp_auth_matrix.py                 # with no connections: calls the public server anonymously
# create connections first for the full matrix (commands in the script header), then re-run
```

## The six connection auth types (`azd ai connection create ... --kind remote-tool --auth-type ...`)
`none` · `custom-keys` · `project-managed-identity` · `agentic-identity` · `user-entra-token` · `oauth2` (managed connector such as `foundrygithubmcp`, or your own app). Only the last two carry the user; `oauth2` returns an `oauth_consent_request` with `consent_link` on first use per tool per project per user, resumes with `previous_response_id`, needs `offline_access` in scopes, same tenant only, Foundry Agent Consumer role for callers. Microsoft-audience tokens are never forwarded to third-party servers (`Cannot pass Microsoft token to untrusted MCP endpoint`).

## APIM side (see `README-provisioning.md` for the policies)
`validate-azure-ad-token` with the app audience for the Entra types, `check-header` for keys, `rate-limit-by-key` per caller, `emit-token-metric`/diagnostics to the same Log Analytics as Foundry. New portal-created MCP tools can be routed through APIM at creation (governance page, preview).

## Proof (checklist)
- [ ] matrix printed: which auth types answered, which errored and why
- [ ] APIM analytics show one request per agent call with the expected caller (key, project MI, agent identity, or user)
- [ ] an `oauth2` connection shows the consent link once, then works

## Next
`../05-private-tool-catalog/` — register the gateway URL in the private tool catalog.
