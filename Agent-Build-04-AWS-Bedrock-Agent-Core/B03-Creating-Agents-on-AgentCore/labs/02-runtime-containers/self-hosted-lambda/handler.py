"""Way 6: the same Strands agent on your own compute (Lambda), Bedrock as the model backend.
Nothing from AgentCore Runtime is used; in B04 lab 06 this function URL becomes a Gateway HTTP
target so it gets inbound auth, Policy and observability from the Gateway side.
Proves: ephemeral at scale is just hosting; what you lose is session isolation and the
per-session microVM, which you now re-implement with your own state store."""
import json
import os

from strands import Agent, tool
from strands.models import BedrockModel


@tool
def get_ticket(ticket_id: str) -> dict:
    """Return one support ticket by id."""
    return {"T-1001": {"customer": "Ayşe", "issue": "charged twice", "amount_gbp": 4.50}}.get(ticket_id, {"error": "no such ticket"})


_agent = None


def lambda_handler(event, _context):
    global _agent
    body = json.loads(event.get("body") or "{}")
    prompt = body.get("prompt")
    if not isinstance(prompt, str):
        return {"statusCode": 400, "body": json.dumps({"error": "prompt must be a string"})}
    if _agent is None:
        _agent = Agent(model=BedrockModel(model_id=os.environ.get("BEDROCK_MODEL_ID", "global.anthropic.claude-haiku-5-5")),
                       system_prompt="UK card-team ticket assistant. Refunds above 250 GBP need a human.", tools=[get_ticket])
    return {"statusCode": 200, "headers": {"content-type": "application/json"},
            "body": json.dumps({"result": str(_agent(prompt))})}
