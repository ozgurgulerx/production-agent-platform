"""G04 lab 05: the lab 03 agent with the Toolbox URL swapped for the Agent Gateway URL (map F7).
Status: scaffold only, functionality unverified."""
import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "..", "..", "..", ".env"))

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
GATEWAY_MCP_URL = os.environ.get("GATEWAY_MCP_URL", os.environ.get("TICKET_MCP_URL", ""))  # gateway when set, else direct

ticketing = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url=f"{GATEWAY_MCP_URL}/mcp", timeout=30),
    # no tool_filter on purpose: the deny must come from the gateway, not from the client (chapter §4, §6)
)

root_agent = LlmAgent(
    name="ticket_agent",
    model=GEMINI_MODEL,
    instruction="Look tickets up with the ticketing tools. If a tool is denied, say which one and by what.",
    tools=[ticketing],
)
