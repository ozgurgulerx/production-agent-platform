"""The ticket agent with AgentCore Memory through Strands' session manager. Session A states a
preference and a fact; session B (new runtime session, same actor) recalls both from long-term
memory. Proves the difference between short-term (per session events) and long-term (per actor
namespaces) memory, and that the agent code only adds a session_manager.
Usage: python agent_with_memory.py   (needs TICKET_MEMORY_ID from memory_setup.py)
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01-ways-to-build"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01-ways-to-build" / "agent"))
from _common import MODEL_ID, REGION, new_session_id, require, session  # noqa: E402
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig  # noqa: E402
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager  # noqa: E402
from main import INSTRUCTIONS, get_policy, get_ticket, issue_refund, list_tickets  # noqa: E402
from strands import Agent  # noqa: E402
from strands.models import BedrockModel  # noqa: E402

require("TICKET_MEMORY_ID")
MEMORY_ID = os.environ["TICKET_MEMORY_ID"]
ACTOR = "customer-ayse"


def agent_for(session_id: str) -> Agent:
    cfg = AgentCoreMemoryConfig(
        memory_id=MEMORY_ID, session_id=session_id, actor_id=ACTOR,
        retrieval_config={
            "/tickets/{actorId}/facts": RetrievalConfig(top_k=5, relevance_score=0.3),
            "/tickets/{actorId}/prefs": RetrievalConfig(top_k=3, relevance_score=0.3),
        },
    )
    sm = AgentCoreMemorySessionManager(cfg, region_name=REGION, boto_session=session())
    return Agent(model=BedrockModel(model_id=MODEL_ID), system_prompt=INSTRUCTIONS,
                 tools=[get_ticket, list_tickets, get_policy, issue_refund], session_manager=sm)


# Session A: short-term memory within the session, events written to the memory store
a = agent_for(new_session_id())
print(a("Hi, I am Ayşe. Please always reply in British English and keep it to two sentences."))
print(a("My open ticket is T-1001; the coffee shop is called Bean There."))

print("\n... waiting for long-term extraction (asynchronous, usually under a minute) ...")
time.sleep(60)

# Session B: new runtime session, same actor; long-term records are injected on initialisation
b = agent_for(new_session_id())
print(b("Which coffee shop was my ticket about, and how do I like replies?"))
