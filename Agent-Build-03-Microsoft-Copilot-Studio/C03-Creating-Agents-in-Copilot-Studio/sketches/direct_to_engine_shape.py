"""Shape only (untested): the Direct-to-Engine loop with the Agents SDK Copilot Studio client 1.9.0 (C8, C9).

Token: a delegated token for scope `https://api.powerplatform.com/CopilotStudio.Copilots.Invoke`
(device code through a public-client app). Standard-harness agents only today (C8).
"""
import asyncio

from microsoft_agents.copilotstudio.client import AgentType, ConnectionSettings, CopilotClient, PowerPlatformCloud


async def main(token: str, environment_id: str, schema_name: str) -> None:
    settings = ConnectionSettings(environment_id=environment_id, agent_identifier=schema_name,
                                  cloud=PowerPlatformCloud.PROD, copilot_agent_type=AgentType.PUBLISHED)
    client = CopilotClient(settings, token)
    async for activity in client.start_conversation():          # welcome message(s), sets the conversation id
        if activity.type == "message":
            print("agent:", activity.text)
    for question in ["What does ticket T-2041 say?", "Refund 400 GBP on it."]:
        async for activity in client.ask_question(question):
            if activity.type == "message":
                print("agent:", activity.text)
                for cit in (activity.entities or []):           # citations arrive as entities / attachments  # verify
                    print("  cite:", getattr(cit, "name", cit))


if __name__ == "__main__":
    asyncio.run(main(token="<device-code token>", environment_id="<env guid>", schema_name="cr1ab_ticketAgent"))
