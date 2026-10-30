"""Give the ticket agent the knowledge base: connection -> MCP tool -> ask -> citations.

1. ARM PUT a RemoteTool connection on the project (ProjectManagedIdentity, audience https://search.azure.com/)
2. create a prompt agent version with MCPTool(allowed_tools=["knowledge_base_retrieve"])
3. ask the two questions and print the answer plus the mcp_call items, which carry the citations

Needs in .env: FOUNDRY_PROJECT_ENDPOINT, AZURE_SEARCH_ENDPOINT, AZ_SUBSCRIPTION_ID, AZ_RESOURCE_GROUP,
FOUNDRY_ACCOUNT_NAME, FOUNDRY_PROJECT_NAME, FOUNDRY_MODEL.
Roles: the project's managed identity needs Search Index Data Reader on the search service;
you need Foundry Project Manager to create the connection.

Run:  python connect_agent.py [--delete]
"""
import os, sys, json
import httpx
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MCPTool, PromptAgentDefinition
from azure.identity import DefaultAzureCredential
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))  # .env at the track root (walks up)
SEARCH = os.environ["AZURE_SEARCH_ENDPOINT"].rstrip("/")
SUB, RG = os.environ["AZ_SUBSCRIPTION_ID"], os.environ["AZ_RESOURCE_GROUP"]
ACCT, PROJ = os.environ["FOUNDRY_ACCOUNT_NAME"], os.environ["FOUNDRY_PROJECT_NAME"]
MODEL = os.environ.get("FOUNDRY_MODEL", "gpt-5-mini")
KB, CONN, AGENT = "ticket-kb", "ticket-kb-connection", "ticket-agent-kb"
MCP_URL = f"{SEARCH}/knowledgebases/{KB}/mcp?api-version=2026-08-01-preview"
PROJECT_ID = f"/subscriptions/{SUB}/resourceGroups/{RG}/providers/Microsoft.CognitiveServices/accounts/{ACCT}/projects/{PROJ}"

cred = DefaultAzureCredential()
project = AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"], credential=cred)

if "--delete" in sys.argv:
    project.agents.delete(agent_name=AGENT); print("deleted", AGENT); sys.exit()

# 1. connection (preview ARM surface). No key anywhere: the project MI presents a token for the Search audience.
arm = {"Authorization": f"Bearer {cred.get_token('https://management.azure.com/.default').token}"}
r = httpx.put(f"https://management.azure.com{PROJECT_ID}/connections/{CONN}?api-version=2025-10-01-preview", headers=arm, timeout=60, json={
    "properties": {"authType": "ProjectManagedIdentity", "category": "RemoteTool", "target": MCP_URL,
                   "audience": "https://search.azure.com/", "metadata": {"ApiType": "Azure"}}})
r.raise_for_status()
conn = project.connections.get(CONN)
print("connection:", conn.name, conn.id)

# 2. the agent: one MCP tool, one allowed tool. Retrieval behaviour is NOT in these instructions; it is on the KB.
agent = project.agents.create_version(agent_name=AGENT, definition=PromptAgentDefinition(
    model=MODEL,
    instructions="You are the UK card team's support assistant. Answer policy questions only from the knowledge base and name the document you relied on. If the knowledge base has nothing, say so.",
    tools=[MCPTool(server_label="knowledge-base", server_url=MCP_URL, require_approval="never",
                   allowed_tools=["knowledge_base_retrieve"], project_connection_id=conn.id)],
))
print("agent:", agent.name, "v", agent.version)

# 3. ask, and show where the answer came from
openai = project.get_openai_client(agent_name=AGENT)
for q in ["Can I refund £300 to a customer's new card?", "Do customers still need a travel notice?", "What is the capital of Peru?"]:
    resp = openai.responses.create(input=q)
    print(f"\nQ: {q}\nA: {resp.output_text.strip()}")
    for item in resp.output:
        if item.type == "mcp_call":
            out = json.loads(item.output) if isinstance(item.output, str) and item.output.startswith("{") else item.output
            refs = out.get("references", []) if isinstance(out, dict) else []
            print("   via knowledge_base_retrieve ->", [x.get("docKey") or x.get("sourceData", {}).get("title") for x in refs][:3] or "(see raw output)")
print("\nThe third answer should be a refusal: the agent has no web tool and the KB has no Peru.")
