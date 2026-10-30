"""Same knowledge base without the gateway: a Strands MemoryManager store that wraps bedrock-agent-runtime Retrieve.

Proves: the classic `strands_tools.retrieve` tool is deprecated (J5); the current pattern is a read-only
MemoryStore given to `Agent(memory_manager=MemoryManager(stores=[...]))`, which injects relevant passages
before each turn and exposes a search tool. `BedrockKnowledgeBaseStore` is not in strands-agents 1.62.0 /
strands-agents-tools 0.8.10 in this venv, so the store below implements the MemoryStore protocol directly
(search only, writable=False).                                            # verify: the shipped store name/module
Pick this when one agent runs in your process with SigV4 and no gateway is needed; pick the gateway when
several agents share the knowledge base, or Cedar and JWT must govern it.
Run:  python strands_memory_store_variant.py
"""
from strands import Agent
from strands.memory import MemoryEntry, MemoryManager
from strands.models import BedrockModel

from _common import MODEL_ID, QUESTIONS, agent_runtime, need

KB_ID = need("TICKET_KB_ID")


class BedrockKnowledgeBaseStore:
    """Read-only MemoryStore over a Bedrock knowledge base (managed or vector)."""
    name = "ticket_policies"
    description = "UK card team refund, card and escalation policies"
    max_search_results = 3
    writable = False
    extraction = None

    def __init__(self, knowledge_base_id: str):
        self.kb_id = knowledge_base_id
        self.rt = agent_runtime()

    async def search(self, query: str, options=None) -> list[MemoryEntry]:
        n = (options or {}).get("max_search_results") or self.max_search_results
        r = self.rt.retrieve(knowledgeBaseId=self.kb_id, retrievalQuery={"text": query},
                             retrievalConfiguration={"managedSearchConfiguration": {"numberOfResults": n}})
        return [MemoryEntry(content=h["content"].get("text", ""), store_name=self.name,
                            metadata={"source": h.get("location", {}).get("s3Location", {}).get("uri", ""),
                                      "score": h.get("score", 0.0)})
                for h in r["retrievalResults"]]


if __name__ == "__main__":
    agent = Agent(model=BedrockModel(model_id=MODEL_ID, temperature=0),
                  system_prompt="Answer only from the injected policy passages and cite the source uri. Refuse otherwise.",
                  memory_manager=MemoryManager(stores=[BedrockKnowledgeBaseStore(KB_ID)]), callback_handler=None)
    for q in QUESTIONS:
        print(f"\nQ: {q}\nA: {str(agent(q)).strip()[:500]}")
