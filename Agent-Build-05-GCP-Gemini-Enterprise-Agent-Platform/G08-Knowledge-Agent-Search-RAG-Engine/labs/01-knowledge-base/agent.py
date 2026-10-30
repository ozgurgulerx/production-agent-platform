"""ticket-agent with a knowledge child agent. G08 lab 01. Scaffold; run with `adk run .` once provision_kb.py has filled .env.

Shape (map letters): LlmAgent (B1); VertexAiSearchTool alone in its agent (B9, D4); AgentTool to the parent (D1);
McpToolset for tickets defined synchronously here (D3). Models and resource paths from .env, never hard-coded.
"""
import os

from dotenv import find_dotenv, load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from google.adk.tools import VertexAiSearchTool
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

load_dotenv(find_dotenv(usecwd=True))

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")  # .env; default is the quickstart id (map C1)
DATASTORE = os.environ.get("AGENT_SEARCH_DATASTORE", "")  # written by provision_kb.py; empty until lab step 2 runs
TICKET_MCP_URL = os.environ.get("TICKET_MCP_URL")        # G04 lab 03; optional while running locally without it


class PolicySearchTool(VertexAiSearchTool):
    """Override point for per-user filters (B9). Leave as-is for the lab."""

    # TODO(learner): override _build_vertex_ai_search_config to add a filter when a user-scoped view is needed.


policy_knowledge = LlmAgent(
    name="policy_knowledge",
    model=MODEL,
    description="Answers questions about refund, card and escalation policy from the policy documents only.",
    instruction=(
        "Search the policy documents for the answer. Answer only from what you find. "
        "End every answer with a line 'Source: <document name>'. "
        "If the documents do not cover the question, say so and do not add a Source line."
    ),
    tools=[PolicySearchTool(data_store_id=DATASTORE)],   # the only tool in this agent (D4)
)

tools = [AgentTool(agent=policy_knowledge)]
if TICKET_MCP_URL:
    tools.append(
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(url=TICKET_MCP_URL),
            # TODO(learner): tool_filter and auth per G04 lab 03 / lab 04
        )
    )

root_agent = LlmAgent(
    name="ticket_agent",
    model=MODEL,
    description="Support-ticket agent: looks up tickets, answers policy questions with citations, refuses refunds outside policy.",
    instruction=(
        "You are the support ticket agent. For any policy question call policy_knowledge and pass its Source line through "
        "unchanged. Never promise a refund outside policy. "
        # TODO(learner): the refusal wording and the ticket lookup behaviour from G03 lab 01
    ),
    tools=tools,
)
