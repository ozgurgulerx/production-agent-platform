"""SDK twin of `azd deploy` for way 6 (container image): build, push to ACR, create the hosted
version from the image, poll until active, invoke, clean up.

Prereqs: Docker running; `az acr login --name $ACR_NAME`; the project's managed identity has
Container Registry Repository Reader on the ACR (azd sets this up for you; here you do it once:
az role assignment create --assignee <project MI principalId> --role "Container Registry Repository Reader" --scope <acr id>).
Run: python deploy_with_sdk.py [--keep] [--skip-build]
"""
import os
import subprocess
import sys
import time
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AgentEndpointProtocol,
    ContainerConfiguration,
    HostedAgentDefinition,
    ProtocolVersionRecord,
)
from azure.identity import DefaultAzureCredential
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=False) or find_dotenv(usecwd=True))  # .env at the track root (walks up)
AGENT_NAME = "ticket-agent-hosted-sdk"
ACR = os.environ["ACR_NAME"]
IMAGE = f"{ACR}.azurecr.io/foundry-demo/ticket-agent-hosted:{int(time.time())}"
SRC = Path(__file__).parent / "src" / "ticket-agent-hosted"

if "--skip-build" not in sys.argv:
    subprocess.run(["docker", "build", "--platform", "linux/amd64", "-t", IMAGE, str(SRC)], check=True)
    subprocess.run(["az", "acr", "login", "--name", ACR], check=True)
    subprocess.run(["docker", "push", IMAGE], check=True)

project = AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"], credential=DefaultAzureCredential())
version = project.agents.create_version(
    agent_name=AGENT_NAME,
    definition=HostedAgentDefinition(
        protocol_versions=[ProtocolVersionRecord(protocol=AgentEndpointProtocol.RESPONSES, version="2.0.0")],
        cpu="1",
        memory="2Gi",
        container_configuration=ContainerConfiguration(image=IMAGE),
        environment_variables={"AZURE_AI_MODEL_DEPLOYMENT_NAME": os.environ.get("FOUNDRY_MODEL", "gpt-5-mini")},
    ),
)
print(f"created {version.name} v{version.version} from {IMAGE}")

deadline = time.time() + 15 * 60
while time.time() < deadline:
    v = project.agents.get_version(agent_name=AGENT_NAME, agent_version=version.version)
    print("  status:", v.status)
    if v.status == "active":
        break
    if v.status == "failed":
        raise SystemExit("provisioning failed: check image platform (linux/amd64), ACR pull role, and container logs")
    time.sleep(15)

openai = project.get_openai_client(agent_name=AGENT_NAME)
print("answer:", openai.responses.create(input="Is ticket 8841 still open?").output_text)

if "--keep" not in sys.argv:
    project.agents.delete(agent_name=AGENT_NAME, force=True)
    print("deleted", AGENT_NAME)
