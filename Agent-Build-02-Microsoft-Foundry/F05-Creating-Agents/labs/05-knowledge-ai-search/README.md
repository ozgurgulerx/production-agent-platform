# 06 — Foundry IQ: Grounding with Azure AI Search

## Goal
Connect an Azure AI Foundry agent to an existing Azure AI Search index for grounded responses (RAG).

## Configuration

| Setting | Value |
|---------|-------|
| AI Search Service | `chatops` |
| Index Name | `imf_baseline` |
| Agent Name | `imf-grounded-agent` |

## What You'll Learn
- How to connect Foundry project to Azure AI Search
- Configure the `AzureAISearchTool` for an existing index
- Create an agent grounded in indexed content
- Best practices for reducing hallucination

## You Will End With
- Connection between Foundry project and AI Search service
- Agent that retrieves from `imf_baseline` index before responding
- Grounded responses based on indexed IMF data

## Prerequisites
- Azure CLI authenticated (`az login`)
- Azure AI Foundry project (from section 02)
- Azure AI Search service (`chatops`) with index (`imf_baseline`)
- RBAC permissions on AI Search service

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Grounding** | Anchoring agent responses in indexed content |
| **RAG** | Retrieval-Augmented Generation - retrieve then generate |
| **AzureAISearchTool** | Tool that queries an AI Search index |
| **Connection** | Link between Foundry project and AI Search |
| **Query Type** | SIMPLE (keyword) or SEMANTIC (AI-powered) |

## Proof (Checklist)
- [ ] AI Search connection exists in Foundry project
- [ ] `imf_baseline` index is accessible
- [ ] Agent created with AI Search tool
- [ ] Agent answers questions using indexed content
- [ ] Responses cite source documents

## Files
- `foundry-iq-grounding.ipynb` - Main notebook

## Quick Start

```python
from azure.ai.agents.models import AzureAISearchTool, AzureAISearchQueryType

# Configure AI Search tool
ai_search_tool = AzureAISearchTool(
    index_connection_id=connection_id,
    index_name="imf_baseline",
    query_type=AzureAISearchQueryType.SIMPLE,
    top_k=5,
)

# Create grounded agent
agent = client.agents.create_agent(
    model="gpt-5-nano",
    name="imf-grounded-agent",
    instructions="Answer using the knowledge base only...",
    tools=ai_search_tool.definitions,
    tool_resources=ai_search_tool.resources,
)
```

## Sources
- [Azure AI Search Tool - Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/azure-ai-search)
- [Foundry IQ Knowledge Bases](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/knowledge-retrieval)
- [Agentic Retrieval Overview](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview)

## Next
Continue to F04: `../../../F06-Agent-Tooling-MCP-and-Integration/labs/02-mcp-tool`.

---

**Author:** Ozgur Guler | AI Solution Leader, AI Innovation Hub | [ozgur.guler1@gmail.com](mailto:ozgur.guler1@gmail.com)
© 2025 Ozgur Guler. All rights reserved.

---
## 2026-10 refresh
All invocation now goes through `client.get_openai_client(agent_name=...)` + `responses.create(...)`; the `extra_body={"agent": ...}` spelling, `client.agents.invoke` and `--pre` installs are gone. Use the repo `.venv` (`azure-ai-projects` 2.7). See `../README.md` for the full list of retired APIs.
Naming note: this notebook uses the **Azure AI Search tool** (`AzureAISearchAgentTool`). A **Foundry IQ knowledge base** is a different object, consumed through its MCP endpoint via a toolbox connection (upstream sample `hosted-agents/agent-framework/responses/17-foundry-iq-toolbox`); it is listed as follow-up work in the F04 chapter.
