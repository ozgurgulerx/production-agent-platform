"""09 — Who is the MCP server talking to? The six connection auth types, and APIM in front.

Authentication for an MCP tool never lives on the tool. It lives on a **project connection**
(`--kind remote-tool`), referenced by `project_connection_id`. Six auth types exist:

| auth type                  | caller identity the server sees        | user context kept |
|----------------------------|----------------------------------------|-------------------|
| none                       | anonymous                              | no  |
| custom-keys                | a static header you stored             | no  |
| project-managed-identity   | the project's managed identity         | no  |
| agentic-identity           | the agent's own Entra identity         | no  |
| user-entra-token           | the calling user's token (same tenant) | yes |
| oauth2 (identity passthrough, managed or custom app) | the user, after a one-time consent | yes |

API Management sits in front of the server to rate-limit, log and validate tokens; it is not
the identity boundary. The server still authorises.

# %% [markdown]
## 1. Create the connections (azd). Run once per server; names are reused below.
# ```bash
# azd ai project set "$FOUNDRY_PROJECT_ENDPOINT"
# azd ai connection create mcp-anon      --kind remote-tool --target "$APIM_MCP_URL" --auth-type none
# azd ai connection create mcp-key       --kind remote-tool --target "$APIM_MCP_URL" --auth-type custom-keys --custom-key "Ocp-Apim-Subscription-Key=<key>"
# azd ai connection create mcp-proj-mi   --kind remote-tool --target "$APIM_MCP_URL" --auth-type project-managed-identity --audience "api://<apim-app-id>"
# azd ai connection create mcp-agent-id  --kind remote-tool --target "$APIM_MCP_URL" --auth-type agentic-identity        --audience "api://<apim-app-id>"
# azd ai connection create mcp-user      --kind remote-tool --target "$APIM_MCP_URL" --auth-type user-entra-token        --audience "api://<apim-app-id>"
# azd ai connection create mcp-oauth     --kind remote-tool --target "$APIM_MCP_URL" --auth-type oauth2 \
#     --client-id <id> --client-secret <secret> --auth-url <authorize> --token-url <token> --refresh-url <token> --scopes "api://<app>/.default offline_access"
# ```
# APIM side: `validate-azure-ad-token` (audience = the app id above) for the Entra types, `rate-limit-by-key`,
# `check-header` for the key type. Governance policy for MCP tools: Learn `agents/how-to/tools/governance`.
"""
# %% config
import os
import sys
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MCPTool, PromptAgentDefinition
from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from dotenv import find_dotenv, load_dotenv
from openai.types.responses.response_input_param import McpApprovalResponse

load_dotenv(find_dotenv(usecwd=False) or find_dotenv(usecwd=True))  # .env at the track root (walks up)
PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"].rstrip("/")
MODEL = os.environ.get("FOUNDRY_MODEL", "gpt-5-mini")
MCP_URL = os.environ.get("APIM_MCP_URL") or "https://learn.microsoft.com/api/mcp"
project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())

CONNECTIONS = {   # auth type -> connection name created with azd above; missing ones are skipped
    "none": "mcp-anon", "custom-keys": "mcp-key", "project-managed-identity": "mcp-proj-mi",
    "agentic-identity": "mcp-agent-id", "user-entra-token": "mcp-user", "oauth2": "mcp-oauth",
}
existing = {c.name: c for c in project.connections.list()}
print("connections present:", sorted(n for n in CONNECTIONS.values() if n in existing))

# %% one agent per auth type; identical except project_connection_id
def run_with(auth_type: str, conn_name: str) -> None:
    agent_name = f"ticket-agent-auth-{auth_type}"
    tool = MCPTool(server_label="apim_mcp", server_url=MCP_URL, require_approval="never",
                   **({"project_connection_id": conn_name} if conn_name else {}))
    try:
        project.agents.get(agent_name=agent_name)
    except ResourceNotFoundError:
        project.agents.create_version(agent_name=agent_name, definition=PromptAgentDefinition(
            model=MODEL, instructions="Use the MCP tools. Answer in one line.", tools=[tool]))
    openai = project.get_openai_client(agent_name=agent_name)
    try:
        r = openai.responses.create(input="List the first three tools you can call.", tool_choice="required")
        for _ in range(3):
            consent = [i for i in r.output if i.type == "oauth_consent_request"]
            if consent:
                # OAuth identity passthrough: first use per (tool, project, user) returns a consent link.
                print(f"  [{auth_type}] CONSENT REQUIRED -> open: {consent[0].consent_link}")
                input("  press Enter after consenting... ")
                r = openai.responses.create(input="List the first three tools you can call.", previous_response_id=r.id, tool_choice="required")
                continue
            approvals = [i for i in r.output if i.type == "mcp_approval_request"]
            if approvals:
                r = openai.responses.create(previous_response_id=r.id, input=[McpApprovalResponse(
                    type="mcp_approval_response", approve=True, approval_request_id=a.id) for a in approvals])
                continue
            break
        errors = [getattr(i, "error", None) for i in r.output if i.type == "mcp_call" and getattr(i, "error", None)]
        print(f"  [{auth_type}] {'ERROR ' + str(errors[0])[:120] if errors else 'ok: ' + r.output_text[:100]}")
    except HttpResponseError as e:
        print(f"  [{auth_type}] HTTP {e.status_code}: {str(e)[:160]}")   # e.g. 'Cannot pass Microsoft token to untrusted MCP endpoint'
    finally:
        if "--keep" not in sys.argv:
            project.agents.delete(agent_name=agent_name)

for auth_type, conn_name in CONNECTIONS.items():
    if conn_name in existing:
        run_with(auth_type, conn_name)
    else:
        print(f"  [{auth_type}] skipped (create connection '{conn_name}' first)")
if not any(n in existing for n in CONNECTIONS.values()):
    print("no connections yet: calling the public server with no connection at all (equivalent to auth type none)")
    run_with("inline-none", None)

# %% [markdown]
## What to look for
# - `none` and `custom-keys`: works, but every user of the agent is the same principal to the server.
# - `project-managed-identity` vs `agentic-identity`: both app-only; the second is per-agent, so APIM logs and
#   Conditional Access can single out one agent (lab 01).
# - `user-entra-token` / `oauth2`: the server sees the user. The first `oauth2` call returns `oauth_consent_request`
#   with a `consent_link`; after consent the call resumes with `previous_response_id`. Scopes must include
#   `offline_access` or the token will not refresh. Cross-tenant is not supported.
# - A Microsoft-audience token can never be forwarded to a third-party server: Foundry answers
#   `Cannot pass Microsoft token to untrusted MCP endpoint`.
