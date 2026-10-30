"""ticket-agent for G05 lab 02. Identical behaviour to G03/G04; the model id is read from EVAL_MODEL so eval_harness.py
can run the same evalset against several models (gemini-3.5-flash, gemini-4-argon, a tuned endpoint in G06; map B10, G9).
"""
import os

from dotenv import find_dotenv, load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

load_dotenv(find_dotenv(usecwd=True))

MODEL = os.environ.get("EVAL_MODEL") or os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
TICKET_MCP_URL = os.environ.get("TICKET_MCP_URL", "")

INSTRUCTION = """You are the support ticket agent. Look tickets up with the ticketing tool before answering a question
about a specific ticket. Refunds are allowed only within 30 days of purchase; refuse anything outside that and say why.
Cite the policy document you relied on. Do not look up a ticket when the question is about policy only."""

tools = []
if TICKET_MCP_URL:
    tools.append(McpToolset(connection_params=StreamableHTTPConnectionParams(url=TICKET_MCP_URL), tool_filter=["lookup_ticket"]))

root_agent = LlmAgent(
    name="ticket_agent",
    model=MODEL,
    description="Answers customer support tickets, refuses refunds outside policy, cites policy documents.",
    instruction=INSTRUCTION,
    tools=tools,
)
