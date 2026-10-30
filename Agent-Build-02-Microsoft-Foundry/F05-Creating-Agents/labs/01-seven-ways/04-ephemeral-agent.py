"""Way 4 — Ephemeral agent: the definition lives in your code, per request. No agent resource.

Two spellings of the same thing:
  (a) Agent Framework `FoundryChatClient` — what hosted agents use under the hood.
  (b) A plain OpenAI client pointed at {project_endpoint}/openai/v1 — proves there is
      nothing Foundry-specific in the wire format.
Both still get Foundry's runtime (conversations, hosted tools, tracing, identity).
Nothing is created in Foundry, so there is nothing to version, publish, or clean up.

Run:  python 04-ephemeral-agent.py
"""
import asyncio
import os

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

from _common import MODEL, PROJECT_ENDPOINT, SUPPORT_INSTRUCTIONS

TICKETS = {"8841": {"status": "open", "issue": "duplicate charge", "amount_gbp": 42.10}}


@tool(approval_mode="never_require")
def get_ticket(ticket_id: str) -> dict:
    """Look up a support ticket by id."""
    return TICKETS.get(ticket_id, {"error": "not found"})


async def with_agent_framework() -> None:
    client = FoundryChatClient(project_endpoint=PROJECT_ENDPOINT, model=MODEL, credential=DefaultAzureCredential())
    agent = Agent(client=client, instructions=SUPPORT_INSTRUCTIONS, tools=[get_ticket], name="ticket-agent-ephemeral")
    result = await agent.run("What is the status of ticket 8841 and how much is involved?")
    print("[agent-framework]", result.text)

    print("[agent-framework, streaming] ", end="", flush=True)
    async for chunk in agent.run("Summarise the ticket in five words.", stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print()

    # Reasoning-effort variant on the same client (replaces the old 02-af-standard-agent-resoning.py).
    reasoning_model = os.environ.get("FOUNDRY_REASONING_MODEL", MODEL)
    reasoning_agent = Agent(
        client=FoundryChatClient(project_endpoint=PROJECT_ENDPOINT, model=reasoning_model, credential=DefaultAzureCredential()),
        instructions="Think carefully, answer in one sentence.",
        default_options={"reasoning": {"effort": "low"}},
    )
    r = await reasoning_agent.run("A customer disputes a £42.10 charge made twice. What is the refund amount?")
    print("[agent-framework, reasoning]", r.text)


def with_raw_openai_client() -> None:
    token = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")
    oai = OpenAI(base_url=f"{PROJECT_ENDPOINT}/openai/v1", api_key=token)
    r = oai.responses.create(model=MODEL, instructions=SUPPORT_INSTRUCTIONS, input="Who are you and what can you do?")
    print("[raw openai client]", r.output_text)


if __name__ == "__main__":
    asyncio.run(with_agent_framework())
    with_raw_openai_client()
