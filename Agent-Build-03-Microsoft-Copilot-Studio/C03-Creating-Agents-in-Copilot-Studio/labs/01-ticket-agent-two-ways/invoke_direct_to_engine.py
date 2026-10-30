"""Call the published ticket agent from code through Direct-to-Engine (Agents SDK Copilot Studio client 1.9.0).

Proves: a delegated `CopilotStudio.Copilots.Invoke` token is enough; the agent's schema name is the identifier; the
conversation is a stream of Activities; a refund over 250 GBP is refused by the agent, not by the client (C8, C9).
Standard-harness agents only today.
"""
import asyncio

from microsoft_agents.copilotstudio.client import AgentType, ConnectionSettings, CopilotClient, PowerPlatformCloud

from _common import AGENT_SCHEMA_NAME, ENVIRONMENT_ID, device_code_token, need

SCOPE = "https://api.powerplatform.com/CopilotStudio.Copilots.Invoke"
TURNS = ["What does ticket T-2041 say?", "Refund 400 GBP on it, the customer is upset.", "And 120 GBP instead?"]


def print_activity(a) -> None:
    if a.type == "message" and a.text:
        print(f"agent: {a.text}")
        for att in a.attachments or []:
            print(f"  attachment: {att.content_type}")
        if a.suggested_actions and a.suggested_actions.actions:
            print("  suggested:", [x.title for x in a.suggested_actions.actions])
        for ent in a.entities or []:                       # citations surface as entities on some channels  # verify
            if getattr(ent, "type", "") == "https://schema.org/Message":
                print("  citation entity present")


async def main() -> None:
    need("ENVIRONMENT_ID", "AGENT_SCHEMA_NAME")
    token = device_code_token([SCOPE])
    cloud = PowerPlatformCloud.PROD
    settings = ConnectionSettings(environment_id=ENVIRONMENT_ID, agent_identifier=AGENT_SCHEMA_NAME,
                                  cloud=cloud, copilot_agent_type=AgentType.PUBLISHED)
    client = CopilotClient(settings, token)
    async for a in client.start_conversation():
        print_activity(a)
    for q in TURNS:
        print(f"\nyou: {q}")
        async for a in client.ask_question(q):
            print_activity(a)
    print("\nexpected: turn 2 refused (over 250 GBP), turn 3 proceeds through issue_refund.")


if __name__ == "__main__":
    asyncio.run(main())
