# 04 — Sessions and Memory Bank: recall across conversations

`ticket-agent` with platform-managed state. Sessions hold one conversation; Memory Bank holds what should survive across conversations. Both are resources under the same `ReasoningEngine`, which is why `VertexAiSessionService` needs `AGENT_RUNTIME_RESOURCE` (B5). Both went GA on `us`, `eu` and `global` on 17 Jun 2026; `IngestEvents` GA 8 Jul 2026; memory profiles GA 15 Jul 2026; metered on the Agent Platform compute SKU since 1 Sep 2026 (A2). `europe-west2` is supported; `global` has no CMEK (A9, F5).

The proof is a two-session test: session A tells the agent the customer prefers SMS; session B, a new session for the same `user_id`, asks which channel to use. Without Memory Bank the agent cannot know; with it the answer is SMS.

| Scope                | Store       | Wire-up                                                                                          | Map    |
| -------------------- | ----------- | ------------------------------------------------------------------------------------------------ | ------ |
| one conversation     | Sessions    | `VertexAiSessionService` in code; `agentengine://` inside the Agent Runtime container            | B5, C2 |
| across conversations | Memory Bank | `--memory_service_uri` on Cloud Run; `agentengine://` on Agent Runtime; class in code unverified | B7, C2 |
| tests                | in-memory   | `InMemorySessionService`; SQLite memory service since ADK 2.11.0                                 | B5, A8 |

## Prerequisites

Lab 02 done: `AGENT_RUNTIME_RESOURCE` in `.env`. `google-adk[gcp]` is in the shared venv.

## Files

```
04-memory-bank/
├── agent.py                 ticket_agent with an instruction that saves and recalls the preferred channel
├── two_sessions.py          session A sets, session B asks; prints both answers
├── requirements.txt
└── test_04_memory_bank.py
```

## Run

```bash
source ../../../labs-setup/.venv/bin/activate
cd 04-memory-bank
python two_sessions.py --sessions-only       # VertexAiSessionService: session B does NOT know the channel
python two_sessions.py --with-memory         # Memory Bank attached: session B answers SMS
adk web --port 8000 --session_service_uri "agentengine://${AGENT_RUNTIME_RESOURCE##*/}"   # dev UI over cloud sessions (B6); URI form from C2
```

The ADK class for the Memory Bank memory service and the kwargs of `VertexAiSessionService` are not on any fetched page (25 Oct 2026); `two_sessions.py` marks both as unverified and the learner confirms them on adk.dev before running.

## Expected output

- `--sessions-only`: session A acknowledges SMS; session B says it does not know the preferred channel.
- `--with-memory`: session A acknowledges SMS; session B answers SMS and (if your instruction asks) says it recalled it.
- Quota headroom: 100 session writes and 100 memory writes per minute (A10), far above what this lab does.

## Proof (checklist)

- [ ] `--sessions-only` prints a session B answer that does not know the channel
- [ ] `--with-memory` prints a session B answer of SMS
- [ ] the two sessions are visible under the resource (console or `adk web` with the `agentengine://` session URI)
- [ ] `pytest test_04_memory_bank.py` runs the tests you wrote

## Cleanup

Sessions and memories are metered (A2). Delete the test user's sessions and memories when done; the API calls are not on a fetched page, so note how you did it in the checklist.

## Next

`../05-grounding-agent-search/` (optional) or G04.
