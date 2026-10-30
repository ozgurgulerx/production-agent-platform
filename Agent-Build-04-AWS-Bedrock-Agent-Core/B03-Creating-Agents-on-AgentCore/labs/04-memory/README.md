# 04 — Memory: short-term events, long-term strategies

AgentCore Memory (GA Oct 2025; episodic strategy Dec 2025; JSON `IngestData`, flexible namespaces Aug 2026; record TTL and per-GB pricing Oct 2026, reading map G) is a resource, not a flag. Short-term memory is the event log per `actorId` + `sessionId`. Long-term memory is extracted asynchronously by **strategies** (semantic, summary, user preference, episodic, custom) into **namespaces** such as `/tickets/{actorId}/facts`, and retrieved by semantic search.

```
04-memory/
├── memory_setup.py         MemoryClient.create_memory_and_wait with semantic + user-preference strategies
└── agent_with_memory.py    AgentCoreMemorySessionManager on the Strands agent; session A teaches, session B recalls
```

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
cd 04-memory
python memory_setup.py            # writes TICKET_MEMORY_ID
python agent_with_memory.py       # two sessions; the second knows "Bean There" and the British-English preference
python memory_setup.py --cleanup
```

## What it proves
- The agent code changes by one argument: `session_manager=AgentCoreMemorySessionManager(AgentCoreMemoryConfig(...))`. Retrieval per namespace is configured, not coded.
- Short-term vs long-term is session id vs actor id. A new session with the same actor still gets the long-term records; a new actor gets nothing.
- Extraction is asynchronous (the 60 s sleep is the honest part of the lab); `ListMemoryExtractionJobs` shows it.
- The same Memory can be attached to a Harness (`memory.agentCoreMemoryConfiguration`), so Harness and Runtime agents can share an actor's memory.

Unverified on 25 Oct 2026: the exact keys in `list_memories()` items (marked `# verify`), and whether the Strands session manager injects long-term records at initialisation or on first message (both are documented patterns; the proof is the recall either way).

## Proof checklist
- [ ] `memory_setup.py` prints `strategies: ['facts', 'prefs']` and `.env` has `TICKET_MEMORY_ID`
- [ ] session B answers "Bean There" and mentions British English without being told in that session
- [ ] `aws bedrock-agentcore list-events --memory-id ... --actor-id customer-ayse` shows session A's events
- [ ] `aws bedrock-agentcore retrieve-memory-records --memory-id ... --namespace /tickets/customer-ayse/facts --search-criteria searchQuery="coffee shop"` returns a record
