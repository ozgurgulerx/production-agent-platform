"""08 — Several MCP servers behind one governed endpoint: a Foundry **toolbox**.

In 2025 this folder attached connector-backed Logic Apps MCP servers one by one. The current
pattern is a toolbox: a versioned, promotable bundle of tools (MCP servers, web search, code
interpreter, A2A...) exposed as ONE MCP endpoint, with credentials injected from project
connections and guardrails applied once. Agents consume the toolbox as a single `mcp` tool.
Tool search (`toolbox_search`, GA Sept 2026) keeps the agent's context small once you pass ~10 tools.

# %% [markdown]
## Servers used
# Two public, no-auth MCP servers stand in for your ServiceNow / Salesforce Logic Apps servers so the
# flow runs anywhere; set `SERVICENOW_MCP_URL` / `SALESFORCE_MCP_URL` (+ `*_CONNECTION_NAME`) to use real ones.
"""
# %% config
import os
import sys
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    MCPTool,
    MCPToolboxTool,
    PromptAgentDefinition,
    ToolSearchToolboxTool,
    WebSearchToolboxTool,
)
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from dotenv import find_dotenv, load_dotenv
from openai.types.responses.response_input_param import McpApprovalResponse

load_dotenv(find_dotenv(usecwd=False) or find_dotenv(usecwd=True))  # .env at the track root (walks up)
PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"].rstrip("/")
MODEL = os.environ.get("FOUNDRY_MODEL", "gpt-5-mini")
TOOLBOX_NAME = "ticket-tools"
AGENT_NAME = "ticket-agent-toolbox"
project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())

def mcp_server(label: str, url_env: str, default_url: str, conn_env: str) -> MCPToolboxTool:
    kwargs = {"server_label": label, "server_url": os.environ.get(url_env) or default_url, "require_approval": "never"}
    if os.environ.get(conn_env):
        kwargs["project_connection_id"] = os.environ[conn_env]     # credential lives on the connection, not here
    return MCPToolboxTool(**kwargs)

# %% create a toolbox version
tools = [
    mcp_server("servicenow", "SERVICENOW_MCP_URL", "https://learn.microsoft.com/api/mcp", "SERVICENOW_CONNECTION_NAME"),
    mcp_server("salesforce", "SALESFORCE_MCP_URL", "https://gitmcp.io/Azure/azure-rest-api-specs", "SALESFORCE_CONNECTION_NAME"),
    WebSearchToolboxTool(),
    ToolSearchToolboxTool(),      # exposes tool_search + call_tool meta-tools instead of the full list
]
toolbox = project.toolboxes.create_version(name=TOOLBOX_NAME, description="Ticketing back-ends behind one endpoint", tools=tools)
print(f"toolbox {toolbox.name} v{toolbox.version}")
TOOLBOX_MCP_URL = f"{PROJECT_ENDPOINT}/toolboxes/{TOOLBOX_NAME}/mcp?api-version=v1"          # serves the DEFAULT version
TOOLBOX_PINNED_URL = f"{PROJECT_ENDPOINT}/toolboxes/{TOOLBOX_NAME}/versions/{toolbox.version}/mcp?api-version=v1"
print("consumer endpoint:", TOOLBOX_MCP_URL)

# %% attach the toolbox to a prompt agent as ONE mcp tool
# The toolbox does not enforce require_approval; the consuming agent does. Keep "always" for writes.
definition = PromptAgentDefinition(
    model=MODEL,
    instructions="You are the support-ticket assistant. Discover tools with tool_search before answering operational questions. Be brief.",
    tools=[MCPTool(server_label="ticket_tools", server_url=TOOLBOX_MCP_URL, require_approval="never")],
)
try:
    project.agents.get(agent_name=AGENT_NAME); print("reusing", AGENT_NAME)
except ResourceNotFoundError:
    v = project.agents.create_version(agent_name=AGENT_NAME, definition=definition); print("created", v.name, "v", v.version)

# %% call it
openai = project.get_openai_client(agent_name=AGENT_NAME)
response = openai.responses.create(input="Which tools do you have for ticketing, and what is the mcp tool's default approval mode per Microsoft Learn?")
for _ in range(4):
    approvals = [i for i in response.output if i.type == "mcp_approval_request"]
    if not approvals:
        break
    response = openai.responses.create(
        input=[McpApprovalResponse(type="mcp_approval_response", approve=True, approval_request_id=i.id) for i in approvals],
        previous_response_id=response.id,
    )
calls = [i for i in response.output if i.type == "mcp_call"]
print("mcp calls:", [(c.name) for c in calls])
print("answer:", response.output_text[:600])

# %% versioning: a new toolbox version does not touch the agent
toolbox_v2 = project.toolboxes.create_version(name=TOOLBOX_NAME, description="v2: web search removed", tools=[t for t in tools if not isinstance(t, WebSearchToolboxTool)])
print(f"toolbox v{toolbox_v2.version} created; default version is promoted separately (portal or `azd ai toolbox`), the agent keeps pointing at /mcp")
print("versions:", [v.version for v in project.toolboxes.list_versions(name=TOOLBOX_NAME)])

# %% cleanup
if "--keep" not in sys.argv:
    project.agents.delete(agent_name=AGENT_NAME)
    project.toolboxes.delete(name=TOOLBOX_NAME)
    print("deleted agent and toolbox")
