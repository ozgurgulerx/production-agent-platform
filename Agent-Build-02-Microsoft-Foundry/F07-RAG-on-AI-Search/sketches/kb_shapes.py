"""Untested sketch. The three bodies that make a knowledge base reachable from an agent. Runnable: ../labs/01-knowledge-base/."""
SEARCH = "https://<search>.search.windows.net"
SOURCE = {  # PUT {SEARCH}/knowledgesources/ticket-policies?api-version=2026-08-01-preview
    "name": "ticket-policies", "kind": "azureBlob",
    "azureBlobParameters": {
        "connectionString": "ResourceId=/subscriptions/.../Microsoft.Storage/storageAccounts/<st>",
        "containerName": "policies", "folderPath": "",
        "ingestionParameters": {
            "embeddingModel": {"kind": "azureOpenAI", "azureOpenAIParameters": {"resourceUri": "https://<acct>.openai.azure.com", "deploymentId": "text-embedding-3-small", "modelName": "text-embedding-3-small"}},
            "contentExtractionMode": "minimal",
        },
    },
}
KB = {  # PUT {SEARCH}/knowledgebases/ticket-kb?api-version=2026-08-01-preview
    "name": "ticket-kb",
    "knowledgeSources": [{"name": "ticket-policies"}],
    "models": [{"kind": "azureOpenAI", "azureOpenAIParameters": {"resourceUri": "https://<acct>.openai.azure.com", "deploymentId": "gpt-5-mini", "modelName": "gpt-5-mini"}}],
    "retrievalReasoningEffort": {"kind": "low"}, "outputMode": "extractiveData",
    "retrievalInstructions": "Prefer refund-policy.md for refunds, card-policy.md for cards.",
}
CONNECTION = {  # PUT https://management.azure.com{project_id}/connections/ticket-kb?api-version=2025-10-01-preview
    "properties": {"authType": "ProjectManagedIdentity", "category": "RemoteTool",
                   "target": f"{SEARCH}/knowledgebases/ticket-kb/mcp?api-version=2026-08-01-preview",
                   "audience": "https://search.azure.com/", "metadata": {"ApiType": "Azure"}},
}
# Then: MCPTool(server_label="knowledge-base", server_url=CONNECTION["properties"]["target"],
#               allowed_tools=["knowledge_base_retrieve"], require_approval="never", project_connection_id=<conn id>)
