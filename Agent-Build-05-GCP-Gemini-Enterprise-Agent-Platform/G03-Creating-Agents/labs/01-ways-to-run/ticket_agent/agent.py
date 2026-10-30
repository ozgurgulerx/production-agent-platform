"""ticket-agent: the one definition every way in G03 runs.

`root_agent` is what `adk run`, `adk web`, `adk api_server`, `adk deploy cloud_run` and `adk deploy agent_engine`
all import (B1, B6). Two local stand-in tools stand in for the ticketing MCP server until G04 lab 02 replaces
them with `McpToolset` at `TICKET_MCP_URL` (D3). Model id comes from .env, never hard-coded.
"""

from __future__ import annotations

import os

from dotenv import find_dotenv, load_dotenv
from google.adk.agents import Agent

load_dotenv(find_dotenv(usecwd=True))  # .env at the track root (walks up)

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")

SUPPORT_INSTRUCTIONS = """You are the support-ticket assistant for a UK bank's card team.
Answer briefly. Look tickets up with get_ticket before answering about them.
Before promising any refund call check_refund_policy. If the result says the refund is outside policy,
refuse politely and cite the policy document named in the result. Never invent ticket data."""


def get_ticket(ticket_id: str) -> dict:
    """Look up a support ticket by id and return its status, amount and customer notes.

    Stand-in for the MCP Toolbox tool of the same purpose (G04). Return a dict with a `status` key (D1).
    """
    # TODO(learner): return a small fixed table of tickets (e.g. 1042 double charge £42.10, 1043 lost card)
    # and {"status": "not_found"} for anything else.
    raise NotImplementedError


def check_refund_policy(amount_gbp: float, reason: str) -> dict:
    """Decide whether a refund is inside policy and name the policy document that applies.

    Return {"status": "ok", "inside_policy": bool, "policy_doc": "..."}.
    """
    # TODO(learner): encode one rule the agent must respect, e.g. duplicate charges under £100 are inside
    # policy (doc "REF-POL-07 §2"), goodwill refunds over £50 are outside policy (doc "REF-POL-07 §4").
    raise NotImplementedError


root_agent = Agent(
    name="ticket_agent",
    model=MODEL,
    description="Answers customer card-support tickets, refuses refunds outside policy, cites policy documents.",
    instruction=SUPPORT_INSTRUCTIONS,
    tools=[
        get_ticket,
        check_refund_policy,
    ],  # plain functions are auto-wrapped in FunctionTool (D1)
)
