"""G04 lab 06: ticket-agent consuming ticket-agent-workflow over A2A (experimental in ADK, map C7).
Status: scaffold only, functionality unverified."""
import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "..", "..", "..", ".env"))

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
TICKET_MCP_URL = os.environ.get("TICKET_MCP_URL", "")
WORKFLOW_CARD = os.environ.get("WORKFLOW_AGENT_CARD", "http://localhost:8001/.well-known/agent-card.json")

ticketing = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url=f"{TICKET_MCP_URL}/mcp", timeout=30),
    tool_filter=["lookup_ticket"],
)

ticket_workflow = RemoteA2aAgent(
    name="ticket_workflow",
    description="Triage, policy check and reply draft for one ticket. Use for anything beyond a status lookup.",
    agent_card=WORKFLOW_CARD,
    # use_legacy=True only against a 0.3 server (map C7); TODO(learner): config=A2aRemoteAgentConfig(...) for timeouts/headers
)

root_agent = LlmAgent(
    name="ticket_agent",
    model=GEMINI_MODEL,
    instruction=(
        "Answer status questions yourself with lookup_ticket. For triage, refund-policy questions or reply drafting, "
        "transfer to ticket_workflow and relay its answer with its citation."
    ),
    tools=[ticketing],
    sub_agents=[ticket_workflow],
)
