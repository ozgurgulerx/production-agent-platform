"""G04 lab 02: ticket-agent with the ticketing MCP server over stdio and a refund-policy before_tool_callback.
Map D3 (McpToolset, StdioConnectionParams, tool_filter), B4 (callbacks), D1 (dict with status).
Status: scaffold only, functionality unverified."""
import os
from typing import Any, Optional

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import BaseTool, ToolContext
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "..", "..", "..", ".env"))

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
TOOLS_YAML = os.path.join(HERE, "..", "03-mcp-toolbox", "tools.yaml")

INSTRUCTION = (
    "You are the support-ticket agent. Look tickets up with the ticketing tools; never guess ticket data. "
    "Refunds are decided by policy, not by you: if a refund is refused, explain the reason you were given. "
    "Cite the policy document when you state a rule."
)

# Declared synchronously at module level (map D3). Toolbox is started as a child process over stdio.
ticketing = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(command="toolbox", args=["--stdio", "--config", TOOLS_YAML]),
        timeout=30,
    ),
    tool_filter=["lookup_ticket", "my_open_tickets"],  # TODO(learner): shrink to ["lookup_ticket"] for the proof row
)


def refuse_refund_outside_policy(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
) -> Optional[dict]:
    """before_tool_callback (map B4). Return a dict to replace the tool call, None to allow it.
    Policy: refund only when amount <= 50 and the ticket is at most 30 days old."""
    if tool.name != "refund_ticket":
        return None
    # TODO(learner): read amount / opened_at from args or from state written by lookup_ticket;
    # return {"status": "refused", "reason": "...policy §2.1..."} when outside policy, else None.
    return {"status": "refused", "reason": "TODO(learner): policy check not implemented; refusing by default"}


root_agent = LlmAgent(
    name="ticket_agent",
    model=GEMINI_MODEL,
    description="Support-ticket agent with ticketing MCP tools.",
    instruction=INSTRUCTION,
    tools=[ticketing],
    before_tool_callback=refuse_refund_outside_policy,
)
