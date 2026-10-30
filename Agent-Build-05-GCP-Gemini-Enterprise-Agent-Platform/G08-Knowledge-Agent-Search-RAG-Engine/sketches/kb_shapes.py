"""Untested sketch. The three knowledge shapes side by side: Agent Search data store, RAG Engine corpus, grounding tool.
Runnable version: ../labs/01-knowledge-base/. Map letters in comments; "unverified" marks names not in the map.
"""
import os

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "P")
DATASTORE = os.environ.get("AGENT_SEARCH_DATASTORE", f"projects/{PROJECT}/locations/global/collections/default_collection/dataStores/ticket-policies")  # path form B9
CORPUS = os.environ.get("RAG_CORPUS", f"projects/{PROJECT}/locations/europe-west3/ragCorpora/ID")  # RAG Engine GA region H11
BUCKET = os.environ.get("POLICY_DOCS_BUCKET", "gs://<bucket>")

# 1. Agent Search data store (Discovery Engine API, H9). Vertical GENERIC, source Cloud Storage, app type search.
DATA_STORE_SHAPE = {  # field names unverified: taken from the H9 vocabulary, not from an API reference
    "display_name": "ticket-policies",
    "industry_vertical": "GENERIC",          # GENERIC | MEDIA | HEALTHCARE_FHIR (H9)
    "solution_types": ["SOLUTION_TYPE_SEARCH"],  # or CHAT, GENERATIVE_CHAT, RECOMMENDATION (H9)
    "source": {"gcs": {"input_uris": [f"{BUCKET}/*.pdf"]}},
}
# Terraform equivalent (I8): google_discovery_engine_data_store + google_discovery_engine_search_engine.

# 2. RAG Engine corpus (H11): ingest -> chunk -> embed -> corpus -> retrieve -> generate.
RAG_CORPUS_SHAPE = {  # field names unverified
    "display_name": "ticket-policies-corpus",
    "location": "europe-west3",              # GA europe-west3/4 (H11); europe-west2 not listed
    "vector_db": "RagManagedDb",             # GA default; Vector Search, Pinecone GA; Feature Store, Weaviate preview (H11)
    "embedding_model": os.environ.get("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001"),
    "import": {"gcs_uris": [f"{BUCKET}/"]},
}

# 3a. Grounding tool in google-genai (H12). Verified shape.
def genai_grounding_tool():
    from google.genai import types
    return types.Tool(retrieval=types.Retrieval(vertex_ai_search=types.VertexAISearch(datastore=DATASTORE)))

# 3b. The same data store as an ADK built-in tool (B9), alone in its agent (D4), handed up through AgentTool (D1).
def adk_knowledge_agent():
    from google.adk.agents import LlmAgent
    from google.adk.tools import AgentTool
    from google.adk.tools import VertexAiSearchTool  # import path per adk.dev/integrations/agent-search (B9)

    knowledge = LlmAgent(
        name="policy_knowledge",
        model=os.environ.get("GEMINI_MODEL", "gemini-3.5-flash"),
        instruction="Answer only from the policy documents. Name the document you used.",
        tools=[VertexAiSearchTool(data_store_id=DATASTORE)],  # the only tool here (D4)
    )
    return AgentTool(agent=knowledge)  # goes into ticket-agent's tools beside the McpToolset

# What the agent must render (B8 for Google Search; same discipline for Agent Search): the source name, not just text.
# TODO(learner): inspect a real response and record the grounding metadata field names here.
