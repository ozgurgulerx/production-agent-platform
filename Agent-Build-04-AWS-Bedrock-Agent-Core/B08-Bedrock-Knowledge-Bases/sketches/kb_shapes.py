"""Request shapes for Bedrock knowledge bases, taken from boto3 1.43.118 on 25 Oct 2026. Not run; shapes only.

Three things to recognise on sight:
1. the managed line: knowledgeBaseConfiguration.type MANAGED and nothing about storage;
2. the customer-managed line: type VECTOR plus a storageConfiguration (S3 Vectors shown);
3. the three retrieval calls and the one that makes the KB an agent tool (the gateway target).
"""

# 1. Managed Knowledge Base (GA 17 Jun 2026, J1). AWS owns store, embeddings and reranker.
create_managed_kb = {
    "name": "ticket-policies-kb",
    "roleArn": "arn:aws:iam::123456789012:role/agentcore-ticket-kb-role",
    "knowledgeBaseConfiguration": {
        "type": "MANAGED",
        "managedKnowledgeBaseConfiguration": {
            "embeddingModelType": "MANAGED",            # or CUSTOM + embeddingModelArn
            # "serverSideEncryptionConfiguration": {"kmsKeyArn": "..."},
        },
    },
}

# 2. Customer-managed on S3 Vectors (GA 2 Dec 2025, J3). You own the vector bucket and the embedding model.
create_vector_kb_s3_vectors = {
    "name": "ticket-policies-kb-vectors",
    "roleArn": "arn:aws:iam::123456789012:role/agentcore-ticket-kb-role",
    "knowledgeBaseConfiguration": {
        "type": "VECTOR",
        "vectorKnowledgeBaseConfiguration": {
            "embeddingModelArn": "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-multimodal-embeddings-v1:0",  # verify id
        },
    },
    "storageConfiguration": {
        "type": "S3_VECTORS",                           # OPENSEARCH_SERVERLESS | RDS | NEPTUNE_ANALYTICS | PINECONE | ...
        "s3VectorsConfiguration": {"vectorBucketArn": "arn:aws:s3vectors:us-east-1:123456789012:bucket/ticket-vectors",
                                   "indexName": "policies"},
    },
}

# S3 data source: the same for both lines. Managed connectors (SharePoint, Confluence, ...) use
# type MANAGED_KNOWLEDGE_BASE_CONNECTOR and are only creatable on managed KBs from 30 Sep 2026 (J4).
create_s3_source = {
    "knowledgeBaseId": "KB123",
    "name": "ticket-policies-s3",
    "dataSourceConfiguration": {"type": "S3", "s3Configuration": {
        "bucketArn": "arn:aws:s3:::my-code-bucket", "inclusionPrefixes": ["policies/"]}},
    "dataDeletionPolicy": "DELETE",
    # customer-managed only: chunking / parsing decisions
    # "vectorIngestionConfiguration": {"chunkingConfiguration": {"chunkingStrategy": "HIERARCHICAL", ...},
    #                                  "parsingConfiguration": {"parsingStrategy": "BEDROCK_DATA_AUTOMATION", ...}},
}

# 3a. Retrieve: passages + locations + scores. The caller writes the answer.
retrieve = {
    "knowledgeBaseId": "KB123",
    "retrievalQuery": {"text": "Can a customer in Peru get a replacement card?"},
    "retrievalConfiguration": {"managedSearchConfiguration": {        # vectorSearchConfiguration on the VECTOR line
        "numberOfResults": 3, "rerankingModelType": "MANAGED",
        # "filter": {"equals": {"key": "team", "value": "cards"}},
    }},
    # "userContext": {"userId": "sub-from-jwt"},   # per-user filtering hook
    # "guardrailConfiguration": {"guardrailId": "...", "guardrailVersion": "1"},
}

# 3b. RetrieveAndGenerate: Bedrock also writes the answer with citations (one model, one KB, no agent loop).
retrieve_and_generate = {
    "input": {"text": "Can a customer in Peru get a replacement card?"},
    "retrieveAndGenerateConfiguration": {"type": "KNOWLEDGE_BASE", "knowledgeBaseConfiguration": {
        "knowledgeBaseId": "KB123", "modelArn": "arn:aws:bedrock:us-east-1::inference-profile/global.anthropic.claude-haiku-5-5"}},
}

# 3c. AgenticRetrieveStream: multi-hop retrieval planned by a model across several retrievers, optional memory
# and guardrail, streamed. The Foundry analogue is retrievalReasoningEffort on the knowledge base.
agentic_retrieve_stream = {
    "messages": [{"role": "user", "content": {"text": "Which policy applies to a duplicate charge on a cancelled card?"}}],  # verify content shape
    "retrievers": [{"description": "UK card team policies", "configuration": {"knowledgeBase": {"knowledgeBaseId": "KB123"}}}],  # verify key
    "agenticRetrieveConfiguration": {"foundationModelType": "MANAGED", "maxAgentIteration": 3, "rerankingModelType": "MANAGED"},
    "generateResponse": True,
    # "policyConfiguration": {"bedrockGuardrailConfiguration": {...}},
    # "memoryConfiguration": {"memoryId": "...", "sessionBinding": {"actorId": "...", "sessionId": "..."}},
}

# 4. The knowledge base as an agent tool: a Gateway connector target (D1, J2). The agent sees
# TicketPolicies___Retrieve and TicketPolicies___AgenticRetrieveStream next to the ticket tools.
gateway_kb_target = {
    "gatewayIdentifier": "gw-123",
    "name": "TicketPolicies",
    "targetConfiguration": {"mcp": {"connector": {
        "source": {"connectorId": "bedrock-knowledge-base"},            # verify: connector id
        "enabled": ["Retrieve", "AgenticRetrieveStream"],
        "configurations": [{"knowledgeBaseId": "KB123"}],               # verify: configuration keys
    }}},
    "credentialProviderConfigurations": [{"credentialProviderType": "GATEWAY_IAM_ROLE"}],
}
