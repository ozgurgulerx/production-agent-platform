"""Versions, the agent endpoint, and what "publish" means now.

- Every create_version is immutable. The endpoint serves ONE version at 100 % traffic;
  which one is chosen by the version selector (default: latest). No traffic splitting.
- Creating the agent already gave it a stable endpoint and its own Entra identity. The
  old "Agent Applications" publishing path is legacy. "Publish" now means distributing
  to Microsoft 365 Copilot / Teams (publish_to_microsoft365), which needs Bot Service rights.

Run:  python 07-versions-and-publish.py
Proof: two versions exist; the endpoint is pinned to v1 then back to latest; the M365
       publish defaults are printed (publishing itself is left as a commented call).
"""
from azure.ai.projects.models import (
    AgentEndpointConfig,
    FixedRatioVersionSelectionRule,
    PromptAgentDefinition,
    VersionSelector,
)

from _common import MODEL, SUPPORT_INSTRUCTIONS, delete_agent, get_or_create, project_client

AGENT_NAME = "ticket-agent-prompt"
project = project_client()
get_or_create(project, AGENT_NAME, PromptAgentDefinition(model=MODEL, instructions=SUPPORT_INSTRUCTIONS))

# A second version with a visible behavioural change.
v2 = project.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(model=MODEL, instructions=SUPPORT_INSTRUCTIONS + " Always end with 'v2'."),
    description="adds the v2 marker",
)
print("created version", v2.version)
versions = sorted(int(v.version) for v in project.agents.list_versions(agent_name=AGENT_NAME))
print("versions:", versions)

openai = project.get_openai_client(agent_name=AGENT_NAME)
print("latest answers:", openai.responses.create(input="Say hello.").output_text.strip()[:60])

# Pin the endpoint to version 1 (rollback), then back to the newest. 100 % is the only ratio allowed.
def route_to(version: int) -> None:
    project.agents.update_details(
        agent_name=AGENT_NAME,
        agent_endpoint=AgentEndpointConfig(
            version_selector=VersionSelector(
                version_selection_rules=[FixedRatioVersionSelectionRule(agent_version=str(version), traffic_percentage=100)]
            )
        ),
    )
    print(f"endpoint now routes 100% to v{version}")

route_to(versions[0])
print("after rollback:", openai.responses.create(input="Say hello.").output_text.strip()[:60])
route_to(versions[-1])
print("after roll-forward:", openai.responses.create(input="Say hello.").output_text.strip()[:60])

# Identity and endpoint come with the agent; nothing to "publish" for a stable URL.
details = project.agents.get(agent_name=AGENT_NAME)
print("agent endpoint:", getattr(details, "agent_endpoint", None))
print("identity:", getattr(details, "identity", None) or getattr(details, "instance_identity", None))

# Distribution to Copilot / Teams. Needs Microsoft.BotService/* write rights; left as a dry run.
defaults = project.agents.get_microsoft365_publish_defaults(agent_name=AGENT_NAME)
print("m365 publish defaults:", defaults)
# project.agents.publish_to_microsoft365(agent_name=AGENT_NAME, publish_scope="Shared", agent_display_name="Ticket agent")

delete_agent(project, AGENT_NAME)
