"""Multi-agent inside ONE Runtime: a Strands Graph (triage -> refund specialist) served by
BedrockAgentCoreApp. Proves that multi-agent is an implementation detail of the container; the
Runtime sees one /invocations endpoint, one session, one trace tree."""
from __future__ import annotations

import os

from bedrock_agentcore import BedrockAgentCoreApp, RequestContext
from strands import Agent, tool
from strands.models import BedrockModel
from strands.multiagent import GraphBuilder

MODEL = os.environ.get("BEDROCK_MODEL_ID", "global.anthropic.claude-haiku-5-5")
TICKETS = {"T-1001": {"customer": "Ayşe", "issue": "charged twice", "amount_gbp": 4.50},
           "T-1003": {"customer": "Priya", "issue": "disputed hotel charge", "amount_gbp": 480.00}}


@tool
def get_ticket(ticket_id: str) -> dict:
    """Return one support ticket by id."""
    return TICKETS.get(ticket_id, {"error": "no such ticket"})


@tool
def issue_refund(ticket_id: str, amount_gbp: float) -> dict:
    """Issue a refund; above 250 GBP it is refused and escalated."""
    if amount_gbp > 250:
        return {"status": "refused", "reason": "needs human approval"}
    return {"status": "issued", "ticket_id": ticket_id, "amount_gbp": amount_gbp}


def build_graph():
    triage = Agent(name="triage", model=BedrockModel(model_id=MODEL), tools=[get_ticket],
                   system_prompt="Read the ticket. Say in one line whether this is a REFUND case or an INFO case and why.")
    refunds = Agent(name="refund_specialist", model=BedrockModel(model_id=MODEL), tools=[get_ticket, issue_refund],
                    system_prompt="You handle refunds for a UK card team. Use issue_refund; respect its refusal.")
    info = Agent(name="info_desk", model=BedrockModel(model_id=MODEL), tools=[get_ticket],
                 system_prompt="Answer the customer's question from the ticket in two sentences.")
    b = GraphBuilder()
    b.add_node(triage, "triage"); b.add_node(refunds, "refunds"); b.add_node(info, "info")
    b.add_edge("triage", "refunds", condition=lambda state: "REFUND" in str(state.results["triage"].result).upper())
    b.add_edge("triage", "info", condition=lambda state: "REFUND" not in str(state.results["triage"].result).upper())
    b.set_entry_point("triage")
    return b.build()


app = BedrockAgentCoreApp()
_graphs: dict[str, object] = {}


@app.entrypoint
def invoke(payload: dict, context: RequestContext) -> dict:
    prompt = payload.get("prompt")
    if not isinstance(prompt, str):
        return {"error": "payload.prompt must be a string"}
    g = _graphs.setdefault(context.session_id or "default", build_graph())
    result = g(prompt)
    last = list(result.results.values())[-1]
    return {"result": str(last.result), "path": [n.node_id for n in result.execution_order], "status": str(result.status)}


if __name__ == "__main__":
    app.run()
