"""The ticket agent answers policy questions through the gateway's knowledge-base tools and cites documents.

Proves: one MCPClient against the gateway (bearer from Cognito), filtered to the TicketPolicies tools; the
retrieval behaviour lives on the knowledge base and the gateway, the agent's prompt only says "use it and
cite"; question three is not in the documents, so a refusal is the correct output.
Run:  python connect_agent.py
"""
import json

from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient

from _common import MODEL_ID, QUESTIONS, cognito_token, need

GATEWAY_URL = need("TICKET_GATEWAY_URL")
SYSTEM = ("You are the UK card team's support assistant. Answer policy questions only from the TicketPolicies "
          "tools and name the document you relied on (the s3 location). If the tools return nothing relevant, "
          "say the policies do not cover it. Never answer general-knowledge questions.")

client = MCPClient(url=GATEWAY_URL, headers={"Authorization": f"Bearer {cognito_token()}"},
                   tool_filters={"allowed": ["TicketPolicies___Retrieve", "TicketPolicies___AgenticRetrieveStream"]})  # ToolFilters keys: allowed / rejected (verified in venv)

with client:
    tools = client.list_tools_sync()
    print("tools from gateway:", [t.tool_name for t in tools])
    agent = Agent(model=BedrockModel(model_id=MODEL_ID, temperature=0), system_prompt=SYSTEM, tools=tools,
                  callback_handler=None)
    for q in QUESTIONS:
        result = agent(q)
        print(f"\nQ: {q}\nA: {str(result).strip()[:600]}")
        for m in agent.messages[-4:]:                                   # the tool result that carried the citation
            for block in m.get("content", []):
                if "toolResult" in block:
                    text = json.dumps(block["toolResult"].get("content"))[:300]
                    print("   via", block["toolResult"].get("toolUseId", "")[:8], text)
