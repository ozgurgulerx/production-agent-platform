"""A2A across Runtimes: the refund specialist as an A2A server on port 9000 with an agent card.
Proves the trust-boundary pattern: another agent (or a Gateway HTTP target) talks JSON-RPC to
this one; it never sees the tools, only the card and the task."""
from __future__ import annotations

import os

from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from bedrock_agentcore.runtime.a2a import serve_a2a
from strands import Agent, tool
from strands.models import BedrockModel
from strands.multiagent.a2a import StrandsA2AExecutor

MODEL = os.environ.get("BEDROCK_MODEL_ID", "global.anthropic.claude-haiku-5-5")


@tool
def issue_refund(ticket_id: str, amount_gbp: float) -> dict:
    """Issue a refund; above 250 GBP it is refused and escalated."""
    return {"status": "refused", "reason": "needs human approval"} if amount_gbp > 250 else {"status": "issued", "ticket_id": ticket_id}


def make_agent(_context_id: str) -> Agent:
    return Agent(name="refund_specialist", model=BedrockModel(model_id=MODEL), tools=[issue_refund],
                 system_prompt="You handle refunds for a UK card team. Use issue_refund; respect its refusal.")


card = AgentCard(
    name="refund_specialist",
    description="Issues card refunds up to 250 GBP; escalates above.",
    url=os.environ.get("AGENTCORE_RUNTIME_URL", "http://localhost:9000/"),  # the Runtime URL once deployed (verify env var name)
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    skills=[AgentSkill(id="refund", name="refund", description="Refund a ticket amount", tags=["refund"])],
)

if __name__ == "__main__":
    serve_a2a(StrandsA2AExecutor(agent_factory=make_agent), card)  # port 9000 is the A2A contract
