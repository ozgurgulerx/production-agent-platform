"""SDK twin of `azd deploy` for way 5: zip src/, upload, remote build, poll until active, invoke, clean up.
Run from this folder: python deploy_with_sdk.py [--keep]
"""
import hashlib
import io
import os
import sys
import time
import zipfile
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    CodeConfiguration,
    CodeDependencyResolution,
    HostedAgentDefinition,
    ProtocolVersionRecord,
)
from azure.identity import DefaultAzureCredential
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=False) or find_dotenv(usecwd=True))  # .env at the track root (walks up)
AGENT_NAME = "ticket-agent-hosted-code-sdk"
SRC = Path(__file__).parent / "src" / "ticket-agent-hosted-code"

project = AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"], credential=DefaultAzureCredential())

# main.py and requirements.txt must sit at the zip root, or provisioning fails.
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
    for f in SRC.iterdir():
        if f.is_file() and f.suffix in (".py", ".txt", ".toml"):
            z.write(f, arcname=f.name)
code = buf.getvalue()
sha = hashlib.sha256(code).hexdigest()

version = project.agents.create_version_from_code(
    agent_name=AGENT_NAME,
    definition=HostedAgentDefinition(
        cpu="0.5",
        memory="1Gi",
        code_configuration=CodeConfiguration(
            runtime="python_3_13",
            entry_point=["python", "main.py"],
            dependency_resolution=CodeDependencyResolution.REMOTE_BUILD,
        ),
        protocol_versions=[ProtocolVersionRecord(protocol="responses", version="2.0.0")],
        environment_variables={"AZURE_AI_MODEL_DEPLOYMENT_NAME": os.environ.get("FOUNDRY_MODEL", "gpt-5-mini")},
    ),
    code=io.BytesIO(code),
    code_zip_sha256=sha,
)
print(f"created {version.name} v{version.version}, status={version.status}")

deadline = time.time() + 15 * 60
while time.time() < deadline:
    v = project.agents.get_version(agent_name=AGENT_NAME, agent_version=version.version)
    print("  status:", v.status)
    if v.status == "active":
        break
    if v.status == "failed":
        raise SystemExit("provisioning failed; check `azd ai agent monitor` or the portal logs")
    time.sleep(15)

openai = project.get_openai_client(agent_name=AGENT_NAME)
print("answer:", openai.responses.create(input="What is the status of ticket 8841?").output_text)

if "--keep" not in sys.argv:
    project.agents.delete(agent_name=AGENT_NAME, force=True)
    print("deleted", AGENT_NAME)
