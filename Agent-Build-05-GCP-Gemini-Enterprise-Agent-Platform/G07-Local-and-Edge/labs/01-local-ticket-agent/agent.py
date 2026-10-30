"""ticket-agent-local: the G03 ticket agent on Gemma 4 through Ollama, with a local stdio MCP stub for tickets.

Map H8: pip install "litellm>=1.84"; from google.adk.models.lite_llm import LiteLlm; Agent(model=LiteLlm(model="ollama_chat/gemma4:e4b"));
OLLAMA_API_BASE=http://localhost:11434; use ollama_chat, not ollama (tool loops).
Map D3: McpToolset defined synchronously in agent.py; StdioConnectionParams(server_params=StdioServerParameters(command, args), timeout).
Run:  adk run .     (after ollama pull gemma4:e4b)
"""

import os
import sys
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

load_dotenv(
    find_dotenv(usecwd=True)
)  # .env at the track root (walks up); only OLLAMA_API_BASE and LOCAL_MODEL are read here
os.environ.setdefault("OLLAMA_API_BASE", "http://localhost:11434")  # map H8

LOCAL_MODEL = os.environ.get("LOCAL_MODEL", "ollama_chat/gemma4:e4b")
assert LOCAL_MODEL.startswith(
    "ollama_chat/"
), "use the ollama_chat prefix, not ollama (map H8)"

STUB = Path(__file__).with_name("ticket_mcp_stub.py")

INSTRUCTION = (
    "You are the UK card team's support assistant. Warm, brief, British English, no exclamation marks. "
    "Use the ticket tools to look tickets up; never invent amounts or dates. "
    "Refunds above 250 GBP need a second approver: refuse, say why in one clause, and say it has been flagged."
)

tickets = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(command=sys.executable, args=[str(STUB)]),
        timeout=30,
    ),
    tool_filter=["get_ticket", "list_tickets"],
)

root_agent = Agent(
    name="ticket_agent_local",
    model=LiteLlm(model=LOCAL_MODEL),
    description="Support ticket agent on Gemma 4 via Ollama; no cloud.",
    instruction=INSTRUCTION,
    tools=[tickets],
)
