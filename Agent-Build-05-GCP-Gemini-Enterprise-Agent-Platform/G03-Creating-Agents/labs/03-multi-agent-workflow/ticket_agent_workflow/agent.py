"""ticket-agent-workflow: triage -> lookup -> reply as ONE root_agent (SequentialAgent, map B2).

State hand-off: `output_key` on one agent becomes `{placeholder}` in the next instruction (B2).
Deployed with the same `adk deploy agent_engine` command as lab 02; one ReasoningEngine, one identity (C2, C5).
"""

from __future__ import annotations

import os

from dotenv import find_dotenv, load_dotenv
from google.adk.agents import Agent, SequentialAgent

load_dotenv(find_dotenv(usecwd=True))
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")


def get_ticket(ticket_id: str) -> dict:
    """Look up a support ticket by id. Stand-in for the MCP Toolbox tool (G04)."""
    # TODO(learner): same fixed table as lab 01, or import it from there once you have factored it out.
    raise NotImplementedError


def check_refund_policy(amount_gbp: float, reason: str) -> dict:
    """Return inside_policy and the policy_doc that applies."""
    # TODO(learner): same rule as lab 01.
    raise NotImplementedError


triage = Agent(
    name="triage",
    model=MODEL,
    output_key="category",
    instruction="Classify the customer's message as one of: billing, card, other. Reply with the single word only.",
)

lookup = Agent(
    name="lookup",
    model=MODEL,
    output_key="facts",
    tools=[get_ticket, check_refund_policy],
    instruction=(
        "Category: {category}. Use get_ticket for any ticket number mentioned and check_refund_policy for any "
        "refund asked for. Return a short bullet list of facts including inside_policy and policy_doc. Do not write "
        "the customer reply."
    ),
)

reply = Agent(
    name="reply",
    model=MODEL,
    instruction=(
        "Facts: {facts}. Write the reply to the customer for a UK bank's card team. If inside_policy is false, "
        "refuse the refund politely and cite policy_doc by name. Keep it under 120 words."
    ),
)

root_agent = SequentialAgent(
    name="ticket_agent_workflow",
    description="Triage, look up, and answer a card-support ticket in three fixed steps.",
    sub_agents=[triage, lookup, reply],
)
