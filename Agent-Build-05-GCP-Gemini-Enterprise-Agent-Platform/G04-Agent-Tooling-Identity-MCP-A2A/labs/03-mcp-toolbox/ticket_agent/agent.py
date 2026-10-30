"""G04 lab 03: ticket-agent against the Cloud Run Toolbox at TICKET_MCP_URL.
Streamable HTTP connection (map D3) with the agent's own ID token for the service URL (map D5, D8).
Status: scaffold only, functionality unverified."""
import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "..", "..", "..", ".env"))

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
TICKET_MCP_URL = os.environ.get("TICKET_MCP_URL", "")  # set by deploy.sh; empty means lab 03 step 3 has not run

INSTRUCTION = (
    "You are the support-ticket agent. Look tickets up with the ticketing tools; never guess ticket data. "
    "Refunds are decided by policy. Cite the policy document when you state a rule."
)


def id_token_headers() -> dict:
    """Mint an OIDC ID token for the Cloud Run URL as audience (the service URL, never the /mcp path) using
    the ambient identity: ADC locally, the Agent Identity principal on Agent Runtime (map D5, D10).
    Lab 04 replaces this header with ADK auth_scheme/auth_credential (service_account_scheme_credential, use_id_token)."""
    # TODO(learner): google.oauth2.id_token.fetch_id_token(google.auth.transport.requests.Request(), TICKET_MCP_URL)
    return {}


ticketing = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=f"{TICKET_MCP_URL}/mcp",
        headers=id_token_headers(),  # evaluated once at import; TODO(learner): refresh before expiry (1 h)
        timeout=30,
    ),
    tool_filter=["lookup_ticket", "my_open_tickets"],
)

root_agent = LlmAgent(
    name="ticket_agent",
    model=GEMINI_MODEL,
    description="Support-ticket agent with the Cloud Run ticketing MCP server.",
    instruction=INSTRUCTION,
    tools=[ticketing],
)
