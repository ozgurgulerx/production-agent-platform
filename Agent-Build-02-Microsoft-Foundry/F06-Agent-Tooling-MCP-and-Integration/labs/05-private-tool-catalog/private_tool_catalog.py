"""10 — Register the APIM-fronted MCP server in the organisation's private tool catalog (API Center),
then consume it from Foundry.

Foundry's **private tool catalog (preview)** is Azure API Center: an MCP server registered there (with
the gateway URL from APIM) appears under Build > Tools for every project the Data Reader role allows.
This script does the registration with `az apic` and verifies both sides. The 2025 version only
printed the commands; this one runs them.

Needs: an API Center (`az apic create`), `Azure API Center Data Reader` for the people who should
discover the tool, and the APIM MCP URL. Set `APIC_NAME`, `APIC_RESOURCE_GROUP`, `APIM_MCP_URL`.

# %% [markdown]
## Register with az apic
"""
# %% config
import json
import os
import subprocess
import sys
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MCPTool, PromptAgentDefinition
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=False) or find_dotenv(usecwd=True))  # .env at the track root (walks up)
PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"].rstrip("/")
MODEL = os.environ.get("FOUNDRY_MODEL", "gpt-5-mini")
APIC_NAME = os.environ.get("APIC_NAME")
APIC_RG = os.environ.get("APIC_RESOURCE_GROUP") or os.environ.get("AZ_RESOURCE_GROUP")
MCP_URL = os.environ.get("APIM_MCP_URL") or "https://learn.microsoft.com/api/mcp"
API_ID, VERSION_ID, DEFINITION_ID, ENV_ID = "ticketing-mcp", "v1", "mcp", "apim-prod"

def az(*args: str) -> dict | list | None:
    out = subprocess.run(["az", *args, "-o", "json", "--only-show-errors"], capture_output=True, text=True)
    if out.returncode:
        print("  az error:", out.stderr.strip()[:300]); return None
    return json.loads(out.stdout) if out.stdout.strip() else None

# %% register api, version, definition, environment, deployment
if APIC_NAME:
    subprocess.run(["az", "extension", "add", "--name", "apic-extension", "--upgrade", "--only-show-errors"], check=False)
    az("apic", "api", "create", "-g", APIC_RG, "-n", APIC_NAME, "--api-id", API_ID, "--title", "Ticketing MCP", "--type", "mcp",
       "--description", "Support-ticket tools (ServiceNow-backed) exposed as MCP via APIM")
    az("apic", "api", "version", "create", "-g", APIC_RG, "-n", APIC_NAME, "--api-id", API_ID, "--version-id", VERSION_ID, "--title", "v1", "--lifecycle-stage", "production")
    az("apic", "api", "definition", "create", "-g", APIC_RG, "-n", APIC_NAME, "--api-id", API_ID, "--version-id", VERSION_ID, "--definition-id", DEFINITION_ID, "--title", "MCP endpoint")
    az("apic", "environment", "create", "-g", APIC_RG, "-n", APIC_NAME, "--environment-id", ENV_ID, "--title", "APIM production", "--type", "production",
       "--server", json.dumps({"type": "Azure API Management", "managementPortalUri": []}))
    az("apic", "api", "deployment", "create", "-g", APIC_RG, "-n", APIC_NAME, "--api-id", API_ID, "--deployment-id", "prod", "--title", "prod",
       "--environment-id", f"/workspaces/default/environments/{ENV_ID}",
       "--definition-id", f"/workspaces/default/apis/{API_ID}/versions/{VERSION_ID}/definitions/{DEFINITION_ID}",
       "--server", json.dumps({"runtimeUri": [MCP_URL]}))
    apis = az("apic", "api", "list", "-g", APIC_RG, "-n", APIC_NAME) or []
    print("APIs in catalog:", [a.get("name") for a in apis])
else:
    print("APIC_NAME not set: skipping registration (the Foundry side below still runs).")

# %% [markdown]
## Consume from Foundry
# In the portal the registered server now appears under **Build > Tools > Catalog** (preview) for anyone with
# API Center Data Reader; adding it there creates exactly the `mcp` tool below. The catalog is discovery and
# governance (who may see which server); the runtime contract is unchanged.
# %% consume from a prompt agent, same as 07
project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
AGENT_NAME = "ticket-agent-catalog"
tool = MCPTool(server_label="ticketing_from_catalog", server_url=MCP_URL, require_approval="never",
               **({"project_connection_id": os.environ["MCP_CONNECTION_NAME"]} if os.environ.get("MCP_CONNECTION_NAME") else {}))
try:
    project.agents.get(agent_name=AGENT_NAME)
except ResourceNotFoundError:
    project.agents.create_version(agent_name=AGENT_NAME, definition=PromptAgentDefinition(model=MODEL, instructions="Use the ticketing tools. One line answers.", tools=[tool]))
r = project.get_openai_client(agent_name=AGENT_NAME).responses.create(input="Name the tools you can call.", tool_choice="required")
print("tools seen:", [len(i.tools) for i in r.output if i.type == "mcp_list_tools"], "| answer:", r.output_text[:200])
if "--keep" not in sys.argv:
    project.agents.delete(agent_name=AGENT_NAME)
