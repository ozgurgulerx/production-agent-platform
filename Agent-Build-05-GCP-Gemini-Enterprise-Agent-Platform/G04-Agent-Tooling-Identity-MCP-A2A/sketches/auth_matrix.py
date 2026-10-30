"""Untested sketch. The five ADK credential types as data; auth is set on the tool, not on a project object.
Map D2, D3, D5, D8. Runnable form: ../labs/04-auth-matrix-apigee/auth_matrix.py."""
import os

# AuthCredentialTypes member : (principal the downstream sees, carries the user?)
CREDENTIAL_TYPES = {
    "API_KEY": ("a static key you stored", False),
    "HTTP": ("the bearer you supplied", None),            # depends on whose token it is
    "SERVICE_ACCOUNT": ("the agent's own principal, as an OIDC ID token when use_id_token is set", False),
    "OAUTH2": ("the calling user, after one consent", True),
    "OPEN_ID_CONNECT": ("the calling user's ID token (Toolbox authService google reads `sub`)", True),
}

from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.auth.auth_schemes import HTTPBearer  # also APIKey, OAuth2, OpenIdConnectWithConfig (D5)
# helpers on the same page (D5): token_to_scheme_credential, service_account_scheme_credential

TICKET_MCP_URL = os.environ["TICKET_MCP_URL"]  # Cloud Run URL from lab 03 (D8)


def ticketing_toolset(auth_scheme=None, auth_credential=None) -> McpToolset:
    """One toolset per matrix row. The audience for the SERVICE_ACCOUNT row is the Cloud Run URL,
    never the MCP path; Cloud Run checks roles/run.invoker before Toolbox sees the request (D8)."""
    return McpToolset(
        connection_params=StreamableHTTPConnectionParams(url=f"{TICKET_MCP_URL}/mcp"),
        tool_filter=["lookup_ticket"],      # client-side convenience, not a policy (section 6)
        auth_scheme=auth_scheme,
        auth_credential=auth_credential,
    )
# TODO(learner): build (scheme, credential) pairs for each row with token_to_scheme_credential /
# service_account_scheme_credential (use_id_token=True, audience=TICKET_MCP_URL) and record what the server saw.
