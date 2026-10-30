"""11 — Agent-to-agent with the A2A tool (protocol 1.0, GA). Replaces "Connected Agents".

Two directions:
1. **Foundry agent -> any A2A agent.** A `RemoteA2A` connection holds the target URL and auth; the
   `a2a` tool references the connection; the calling agent delegates. The target can be another Foundry
   agent (`.../agents/<name>/endpoint/protocols/a2a`, audience https://ai.azure.com), the self-hosted
   agent from 02, or a third party.
2. **Logic Apps -> Foundry agent.** A Logic Apps Standard workflow can call the same A2A or Responses
   endpoint with its managed identity (Foundry User on the project). The workflow definition is in
   `logic-app/` and only needs the agent name.

# %% [markdown]
## Create the connection once (azd)
# ```bash
# azd ai project set "$FOUNDRY_PROJECT_ENDPOINT"
# # target = another Foundry agent (needs incoming A2A enabled on it):
# azd ai connection create specialist-a2a --kind remote-a2a \
#    --target "$FOUNDRY_PROJECT_ENDPOINT/agents/ticket-agent-workflow/endpoint/protocols/a2a" \
#    --auth-type user-entra-token --audience https://ai.azure.com
# # or target = the self-hosted agent from 02 (anonymous or custom-keys):
# azd ai connection create specialist-a2a --kind remote-a2a --target "$SELF_HOSTED_URL" --auth-type none
# ```
"""
# %% config
import os
import sys
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import A2AProtocolVersion, A2ATool, PromptAgentDefinition
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=False) or find_dotenv(usecwd=True))  # .env at the track root (walks up)
PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"].rstrip("/")
MODEL = os.environ.get("FOUNDRY_MODEL", "gpt-5-mini")
A2A_CONNECTION_NAME = os.environ.get("A2A_CONNECTION_NAME", "specialist-a2a")
CALLER = "ticket-agent-a2a-caller"
project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())

# %% the a2a tool (v1.0 GA; a2a_preview is protocol 0.3)
try:
    conn = project.connections.get(A2A_CONNECTION_NAME)
except ResourceNotFoundError:
    raise SystemExit(f"Create the connection first: azd ai connection create {A2A_CONNECTION_NAME} --kind remote-a2a ...")
tool = A2ATool(a2a_version=A2AProtocolVersion.V1_0, project_connection_id=conn.id)
try:
    project.agents.get(agent_name=CALLER)
except ResourceNotFoundError:
    project.agents.create_version(agent_name=CALLER, definition=PromptAgentDefinition(
        model=MODEL,
        instructions="You are the front-desk agent. For anything about a specific ticket, delegate to the specialist agent via A2A and relay its answer verbatim.",
        tools=[tool]))

# %% delegate
openai = project.get_openai_client(agent_name=CALLER)
r = openai.responses.create(input="Ask the specialist what should happen with ticket 8841 (duplicate charge, £42.10).", tool_choice="required")
for item in r.output:
    if item.type not in ("message",):
        print("output item:", item.type, getattr(item, "name", ""), str(getattr(item, "error", "") or "")[:120])
print("answer:", r.output_text)
# Limits today: text only; no streaming when the target is a Foundry agent.

# %% cleanup
if "--keep" not in sys.argv:
    project.agents.delete(agent_name=CALLER)
