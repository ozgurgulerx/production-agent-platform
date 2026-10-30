"""AgentCore Memory: one Memory resource with a semantic and a user-preference long-term strategy.
Short-term memory is the event log per actor+session; long-term records are extracted
asynchronously into namespaces. Proves that memory is a resource with an id, not a feature flag.
Usage: python memory_setup.py [--cleanup]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01-ways-to-build"))
from _common import REGION, session, write_env  # noqa: E402
from bedrock_agentcore.memory import MemoryClient  # noqa: E402

NAME = "ticket_agent_memory"
client = MemoryClient(region_name=REGION, boto3_session=session())

ap = argparse.ArgumentParser()
ap.add_argument("--cleanup", action="store_true")
args = ap.parse_args()

existing = next((m for m in client.list_memories() if m.get("name") == NAME or m.get("id", "").startswith(NAME)), None)  # verify list item keys
if args.cleanup:
    if existing:
        client.delete_memory_and_wait(existing["id"])
        print("[cleanup] memory deleted")
    raise SystemExit(0)

if existing:
    memory = existing
else:
    memory = client.create_memory_and_wait(
        name=NAME,
        description="B03 lab 04: ticket agent memory",
        event_expiry_days=30,
        strategies=[
            {"semanticMemoryStrategy": {"name": "facts", "namespaces": ["/tickets/{actorId}/facts"]}},
            {"userPreferenceMemoryStrategy": {"name": "prefs", "namespaces": ["/tickets/{actorId}/prefs"]}},
        ],
    )
print("memory:", memory["id"], memory.get("status"))
print("strategies:", [s.get("name") for s in client.get_memory_strategies(memory["id"])])
write_env("TICKET_MEMORY_ID", memory["id"])
