"""Hosted agent, Responses protocol. The platform injects FOUNDRY_PROJECT_ENDPOINT,
AZURE_AI_MODEL_DEPLOYMENT_NAME (from azure.yaml env) and APPLICATIONINSIGHTS_CONNECTION_STRING.
Listens on :8088, serves POST /responses and GET /readiness. Multi-turn history is handled by
the host via previous_response_id, so the agent does not store on the service (store=False).
"""
import os

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

TICKETS = {"8841": {"status": "open", "issue": "duplicate charge", "amount_gbp": 42.10}}


@tool(approval_mode="never_require")
def get_ticket(ticket_id: str) -> dict:
    """Look up a support ticket by id."""
    return TICKETS.get(ticket_id, {"error": "not found"})


def main() -> None:
    model = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME") or os.getenv("FOUNDRY_MODEL")
    if not model:
        raise RuntimeError("Set AZURE_AI_MODEL_DEPLOYMENT_NAME (or FOUNDRY_MODEL).")
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=model,
        credential=DefaultAzureCredential(),
    )
    agent = Agent(
        client=client,
        name="ticket-agent-hosted-code",
        instructions=(
            "You are the support-ticket assistant for a UK bank's card team. Answer briefly. "
            "Use get_ticket when a ticket id is mentioned. Say when you cannot do something."
        ),
        tools=[get_ticket],
        default_options={"store": False},
    )
    ResponsesHostServer(agent).run()


if __name__ == "__main__":
    main()
