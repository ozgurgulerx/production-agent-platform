"""07 — A remote MCP server as a Foundry tool (Logic Apps Standard is one way to host it).

There is no "Logic Apps tool" in Foundry Agent Service. What exists is the `mcp` tool: Foundry
calls any Streamable-HTTP MCP server you point it at. Logic Apps Standard can expose a workflow
as such a server (`/api/mcpservers/<name>/mcp`); so can Azure Functions, Container Apps, APIM.
This script attaches one MCP server to a prompt agent with the CURRENT SDK types and drives the
approval loop that Foundry requires by default.

# %% [markdown]
## Set-up
# `LOGIC_APP_MCP_URL` in .env selects your server. Empty = the public Microsoft Learn MCP server,
# which needs no auth, so the whole loop can be exercised before any Logic App exists.
"""
# %% imports and config
import json
import os
import sys
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MCPTool, PromptAgentDefinition
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from dotenv import find_dotenv, load_dotenv
from openai.types.responses.response_input_param import McpApprovalResponse

load_dotenv(find_dotenv(usecwd=False) or find_dotenv(usecwd=True))  # .env at the track root (walks up)
PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
MODEL = os.environ.get("FOUNDRY_MODEL", "gpt-5-mini")
MCP_URL = os.environ.get("LOGIC_APP_MCP_URL") or "https://learn.microsoft.com/api/mcp"
MCP_CONNECTION = os.environ.get("MCP_CONNECTION_NAME")   # project connection holding the server's credential, if any
AGENT_NAME = "ticket-agent-mcp"
project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())

# %% the mcp tool, current shape
# require_approval defaults to "always": every tool call pauses as an mcp_approval_request item
# until the caller answers. {"never": {"tool_names": [...]}} whitelists read-only tools.
tool = MCPTool(
    server_label="ticketing",
    server_url=MCP_URL,
    require_approval="always",
    **({"project_connection_id": MCP_CONNECTION} if MCP_CONNECTION else {}),
)
definition = PromptAgentDefinition(
    model=MODEL,
    instructions="You are the support-ticket assistant. Use the ticketing MCP tools when they help. Be brief.",
    tools=[tool],
)
try:
    project.agents.get(agent_name=AGENT_NAME)
    print("reusing", AGENT_NAME)
except ResourceNotFoundError:
    v = project.agents.create_version(agent_name=AGENT_NAME, definition=definition)
    print("created", v.name, "v", v.version)

# %% the approval loop
openai = project.get_openai_client(agent_name=AGENT_NAME)
conversation = openai.conversations.create()
question = os.environ.get("MCP_QUESTION", "Search the docs: what does Foundry's mcp tool `require_approval` default to?")
response = openai.responses.create(conversation=conversation.id, input=question, tool_choice="required")

for _ in range(6):   # bounded: each iteration answers all pending approvals, then resumes by previous_response_id
    approvals = [item for item in response.output if item.type == "mcp_approval_request"]
    if not approvals:
        break
    answers = []
    for item in approvals:
        print(f"approval requested: {item.server_label}.{item.name}({item.arguments})")
        approve = True     # policy hook: inspect item.arguments here (this is where a refund limit would live)
        answers.append(McpApprovalResponse(type="mcp_approval_response", approve=approve, approval_request_id=item.id))
    response = openai.responses.create(conversation=conversation.id, input=answers, previous_response_id=response.id)

for item in response.output:
    if item.type == "mcp_call":
        print(f"mcp_call {item.name}: error={getattr(item, 'error', None)} output={str(getattr(item, 'output', ''))[:160]!r}")
    if item.type == "mcp_list_tools":
        print("server advertised", len(item.tools), "tools")
print("\nanswer:", response.output_text)

# %% cleanup
if "--keep" not in sys.argv:
    project.agents.delete(agent_name=AGENT_NAME)
    print("deleted", AGENT_NAME)
