"""G04 lab 04: factory that builds one ticket-agent per credential type. auth_matrix.py drives it.
Map D3 (McpToolset auth_scheme/auth_credential), D5 (schemes, AuthCredentialTypes, helpers).
Status: scaffold only, functionality unverified."""
import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.auth import AuthCredentialTypes
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "..", "..", "..", ".env"))

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
TICKET_MCP_URL = os.environ.get("TICKET_MCP_URL", "")

ROWS = ["none", "API_KEY", "HTTP", "SERVICE_ACCOUNT", "OAUTH2", "OPEN_ID_CONNECT"]


def credential_pair(row: str, target: str):
    """Return (auth_scheme, auth_credential) for a matrix row, or (None, None) for the anonymous row (map D5)."""
    if row == "none":
        return None, None
    # TODO(learner):
    #   API_KEY          -> token_to_scheme_credential("apikey", "header", "x-api-key", os.environ["APIGEE_API_KEY"])
    #   HTTP             -> token_to_scheme_credential("oauth2Token", "header", "Authorization", <ID token for target>)
    #   SERVICE_ACCOUNT  -> service_account_scheme_credential(ServiceAccount(use_default_credential=True,
    #                       use_id_token=True, audience=target))   # audience = service URL, not /mcp
    #   OAUTH2           -> OAuth2 scheme with Google's auth/token URLs + AuthCredential(OAUTH2, client_id/secret)
    #   OPEN_ID_CONNECT  -> OpenIdConnectWithConfig(...) + AuthCredential(OPEN_ID_CONNECT, client_id/secret)
    raise NotImplementedError(f"TODO(learner): credential pair for {row}")


def make_agent(row: str, target: str = TICKET_MCP_URL) -> LlmAgent:
    scheme, cred = credential_pair(row, target)
    toolset = McpToolset(
        connection_params=StreamableHTTPConnectionParams(url=f"{target}/mcp", timeout=30),
        tool_filter=["lookup_ticket", "my_open_tickets"],
        auth_scheme=scheme,
        auth_credential=cred,
    )
    return LlmAgent(
        name=f"ticket_agent_{row.lower()}",
        model=GEMINI_MODEL,
        instruction="Look up the ticket the user names with the ticketing tools and report status and amount.",
        tools=[toolset],
    )


# adk web needs a root_agent; the anonymous row is the safe default to show.
root_agent = make_agent("none")
