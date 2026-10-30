"""The ticket agent as an AgentCore Runtime HTTP app. Proves the container contract:
POST /invocations and GET /ping on 8080, session id from the request context, nothing else.
Same file is zipped by 02-runtime-code-deploy.py and copied into 02-runtime-containers/.
"""
from __future__ import annotations

import os

from bedrock_agentcore import BedrockAgentCoreApp, RequestContext
from strands import Agent, tool
from strands.models import BedrockModel

TICKETS = {
    "T-1001": {"customer": "Ayşe", "issue": "charged twice for a coffee", "amount_gbp": 4.50, "status": "open"},
    "T-1002": {"customer": "Mert", "issue": "card declined abroad", "amount_gbp": 0, "status": "open"},
    "T-1003": {"customer": "Priya", "issue": "disputed hotel charge", "amount_gbp": 480.00, "status": "open"},
}
POLICIES = {"refund": "Refunds up to 250 GBP may be issued by the agent; above that a human must approve."}
INSTRUCTIONS = (
    "You are the support-ticket assistant for a UK bank's card team. Answer briefly. "
    "Use the tools for ticket facts; never invent a ticket. Refunds above 250 GBP need a human."
)


@tool
def get_ticket(ticket_id: str) -> dict:
    """Return one support ticket by id, or an error if it does not exist."""
    return TICKETS.get(ticket_id, {"error": f"no ticket {ticket_id}"})


@tool
def list_tickets(status: str = "open") -> list[dict]:
    """List tickets with the given status."""
    return [{"id": k, **v} for k, v in TICKETS.items() if v["status"] == status]


@tool
def get_policy(name: str) -> str:
    """Return the text of a named policy (e.g. 'refund')."""
    return POLICIES.get(name, "no such policy")


@tool
def issue_refund(ticket_id: str, amount_gbp: float) -> dict:
    """Issue a refund against a ticket. Amounts above 250 GBP are refused and escalated."""
    if amount_gbp > 250:
        return {"status": "refused", "reason": "above 250 GBP, needs human approval", "ticket_id": ticket_id}
    return {"status": "issued", "ticket_id": ticket_id, "amount_gbp": amount_gbp}


def build_agent() -> Agent:
    model = BedrockModel(model_id=os.environ.get("BEDROCK_MODEL_ID", "global.anthropic.claude-haiku-5-5"))
    return Agent(model=model, system_prompt=INSTRUCTIONS, tools=[get_ticket, list_tickets, get_policy, issue_refund])


app = BedrockAgentCoreApp()
_agents: dict[str, Agent] = {}  # one Strands agent per runtime session (the microVM is per session anyway)


@app.entrypoint
def invoke(payload: dict, context: RequestContext) -> dict:
    prompt = payload.get("prompt")
    if not isinstance(prompt, str):  # SDK security guidance: never trust a non-string prompt (toolUse injection)
        return {"error": "payload.prompt must be a string"}
    agent = _agents.setdefault(context.session_id or "default", build_agent())
    result = agent(prompt)
    return {"result": str(result), "session_id": context.session_id}


if __name__ == "__main__":
    app.run()  # 0.0.0.0:8080; /ping answers Healthy
