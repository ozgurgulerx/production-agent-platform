# F08 labs — Foundry IQ

Setup is shared: [`../../labs-setup/`](../../labs-setup/). Assumes F03 lab 01 (the ticket agent) and an Azure AI Search service.

```
labs/
└── 01-knowledge-base/   policies in Blob -> azureBlob source -> knowledge base -> MCP tool on the agent -> citations
```

| Lab | Chapter section | Needs beyond the shared setup |
|---|---|---|
| 01 | §1 object model, §2 one retrieval, §3 agent consumption | AI Search service, storage account, five role assignments listed in the lab README |

Contrast lab: F03 `labs/05-knowledge-ai-search` (the AI Search tool, one index, no knowledge base).
