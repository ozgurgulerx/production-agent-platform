"""ticket-agent with policy grounding: one built-in tool per agent, wrapped in AgentTool (B9, D1, D4).

Shape:
    ticket_agent (function tools: get_ticket, check_refund_policy, AgentTool(policy_agent))
        policy_agent (VertexAiSearchTool only)
Putting VertexAiSearchTool straight into ticket_agent.tools beside the function tools breaks at call time (D4).
"""

from __future__ import annotations

import os

from dotenv import find_dotenv, load_dotenv
from google.adk.agents import Agent
from google.adk.tools import VertexAiSearchTool
from google.adk.tools.agent_tool import AgentTool

load_dotenv(find_dotenv(usecwd=True))
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
DATASTORE = os.environ.get(
    "AGENT_SEARCH_DATASTORE", ""
)  # projects/P/locations/global/collections/default_collection/dataStores/ID (B9); empty until the data store exists


def get_ticket(ticket_id: str) -> dict:
    """Look up a support ticket by id. Stand-in for the MCP Toolbox tool (G04)."""
    # TODO(learner): same fixed table as lab 01
    raise NotImplementedError


def check_refund_policy(amount_gbp: float, reason: str) -> dict:
    """Return inside_policy and the policy_doc that applies."""
    # TODO(learner): same rule as lab 01
    raise NotImplementedError


policy_search = VertexAiSearchTool(data_store_id=DATASTORE)
# TODO(learner), optional: subclass VertexAiSearchTool and override _build_vertex_ai_search_config to add a
# per-user filter (B9), e.g. restrict to documents tagged with the customer's product.

policy_agent = Agent(
    name="policy_agent",
    model=MODEL,
    description="Searches the card team's policy documents and returns the relevant passage with its document id and section.",
    instruction="Search the policy documents for the question. Reply with the passage, the document id and the section. "
    "If nothing relevant is found, say so.",
    tools=[policy_search],  # the ONLY tool in this agent (D4)
)

root_agent = Agent(
    name="ticket_agent",
    model=MODEL,
    description="Answers card-support tickets, refuses refunds outside policy, cites policy documents.",
    instruction="You are the support-ticket assistant for a UK bank's card team. Look tickets up with get_ticket. "
    "Before any refund decision call check_refund_policy, then call policy_agent to fetch the exact policy "
    "passage and cite its document id and section in your answer. Never cite a document you did not retrieve.",
    tools=[get_ticket, check_refund_policy, AgentTool(agent=policy_agent)],
)
