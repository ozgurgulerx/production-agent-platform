"""Way 2b — A server-managed prompt agent driven from Agent Framework with `FoundryAgent`.

`FoundryChatClient` = your code owns the definition (way 4).
`FoundryAgent`      = the definition lives in Foundry (a prompt or hosted agent); Agent
Framework is only the client. This replaces the removed `AzureAIAgentClient`.

It also shows `to_prompt_agent()`: build the agent locally with Agent Framework, then
export the definition to Foundry so the same agent exists as a versioned prompt agent.

Run:  python 05-foundry-agent-af.py   (creates ticket-agent-prompt if 02 did not keep it)
"""
import asyncio

from agent_framework import Agent
from agent_framework.foundry import FoundryAgent, FoundryChatClient, to_prompt_agent
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential

from _common import MODEL, PROJECT_ENDPOINT, SUPPORT_INSTRUCTIONS, delete_agent, get_or_create, project_client

AGENT_NAME = "ticket-agent-prompt"
EXPORTED_NAME = "ticket-agent-exported"


async def main() -> None:
    project = project_client()
    get_or_create(project, AGENT_NAME, PromptAgentDefinition(model=MODEL, instructions=SUPPORT_INSTRUCTIONS))

    # 1. Drive the Foundry-managed agent from Agent Framework. No instructions here: Foundry has them.
    agent = FoundryAgent(project_endpoint=PROJECT_ENDPOINT, agent_name=AGENT_NAME, credential=DefaultAzureCredential())
    result = await agent.run("Explain in one line what you are.")
    print("[FoundryAgent]", result.text)

    # 2. Build locally, export to Foundry. to_prompt_agent() turns an Agent Framework Agent
    #    into a PromptAgentDefinition you can create_version with.
    local = Agent(
        client=FoundryChatClient(project_endpoint=PROJECT_ENDPOINT, model=MODEL, credential=DefaultAzureCredential()),
        instructions=SUPPORT_INSTRUCTIONS + " You were authored in Agent Framework and exported.",
        name=EXPORTED_NAME,
    )
    definition = to_prompt_agent(local)
    print("[to_prompt_agent] exported definition model:", definition.model)
    get_or_create(project, EXPORTED_NAME, definition)
    exported = project.get_openai_client(agent_name=EXPORTED_NAME).responses.create(input="Where were you authored?")
    print("[exported agent]", exported.output_text)
    delete_agent(project, EXPORTED_NAME)


if __name__ == "__main__":
    asyncio.run(main())
