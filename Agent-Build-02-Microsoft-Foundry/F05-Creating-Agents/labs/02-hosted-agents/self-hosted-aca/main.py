"""Way 7 — the SAME agent and the SAME host server, but running on compute you operate
(Azure Container Apps here; AKS or a laptop work identically). Foundry still supplies the
model, the toolbox and the tracing backend; you supply ingress, identity, scaling and patching.

Because ResponsesHostServer speaks the Responses protocol, any OpenAI client can call it at
https://<your-host>/responses, and a Foundry agent can call it through an A2A/MCP connection.
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
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME") or os.environ["FOUNDRY_MODEL"],
        credential=DefaultAzureCredential(),   # on ACA: the container app's managed identity
    )
    agent = Agent(
        client=client,
        name="ticket-agent-self-hosted",
        instructions="You are the support-ticket assistant for a UK bank's card team. Answer briefly. "
                     "Mention that you are self-hosted if asked where you run.",
        tools=[get_ticket],
        default_options={"store": False},
    )
    ResponsesHostServer(agent).run(port=int(os.environ.get("PORT", "8088")))


if __name__ == "__main__":
    main()
