"""Untested sketch. The F03 creation matrix as code: one definition per way, one call surface.
Runnable versions: ../labs/01-seven-ways and ../labs/02-hosted-agents. Requires azure-ai-projects>=2.3, agent-framework-foundry."""
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (CodeConfiguration, CodeDependencyResolution, ContainerConfiguration,
                                      HostedAgentDefinition, PromptAgentDefinition, ProtocolVersionRecord)
from azure.identity import DefaultAzureCredential

project = AIProjectClient(endpoint="https://<r>.services.ai.azure.com/api/projects/<p>", credential=DefaultAzureCredential())
INSTR = "You are the support-ticket assistant."

# way 2 — prompt agent; definition lives in Foundry
project.agents.create_version(agent_name="ticket-prompt", definition=PromptAgentDefinition(model="gpt-5-mini", instructions=INSTR))
# way 5 — hosted from zip; definition = your container built remotely
project.agents.create_version_from_code(agent_name="ticket-hosted-code", definition=HostedAgentDefinition(
    cpu="0.5", memory="1Gi", protocol_versions=[ProtocolVersionRecord(protocol="responses", version="2.0.0")],
    code_configuration=CodeConfiguration(runtime="python_3_13", entry_point=["python", "main.py"], dependency_resolution=CodeDependencyResolution.REMOTE_BUILD)),
    code=open("src.zip", "rb"))
# way 6 — hosted from image
project.agents.create_version(agent_name="ticket-hosted", definition=HostedAgentDefinition(
    cpu="1", memory="2Gi", protocol_versions=[ProtocolVersionRecord(protocol="responses", version="2.0.0")],
    container_configuration=ContainerConfiguration(image="<acr>.azurecr.io/ticket:1")))
# way 4 — ephemeral; definition lives in the request (no create call at all)
raw = project.get_openai_client()
raw.responses.create(model="gpt-5-mini", instructions=INSTR, input="hi")
# one surface for the rest
for name in ("ticket-prompt", "ticket-hosted-code", "ticket-hosted"):
    print(project.get_openai_client(agent_name=name).responses.create(input="hi").output_text)
