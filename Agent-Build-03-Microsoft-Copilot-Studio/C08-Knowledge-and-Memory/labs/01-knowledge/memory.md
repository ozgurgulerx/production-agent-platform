# Memory in Copilot Studio: what it is, who sees it, and why it is not where the refund limit goes

Read this after the three questions. There is nothing to run; the facts are G1–G4 in the reading map.

## Three objects called memory

|                          | Memory (GitHub harness)                | Structured memory (Customer Conversation harness) | Business-process memory (persistent agents) |
| ------------------------ | -------------------------------------- | ------------------------------------------------- | ------------------------------------------- |
| Status                   | production-ready preview (G1)          | preview, with the harness (G2)                    | announced 15 Oct 2026, Frontier (G3)        |
| Scope                    | one user × one agent                   | one customer conversation                         | one agent across runs                       |
| Storage                  | Microsoft-managed per-user files       | the harness                                       | the harness                                 |
| Maker can read           | **no**                                 | no                                                | to be documented                            |
| User can read and delete | yes, memory portal                     | no                                                | no                                          |
| Lifetime                 | deleted after 28 days without activity | conversation lifecycle                            | to be documented                            |

## And one thing that is not memory

`ConversationTranscript` in Dataverse (G4) stores every session as Bot Framework activity JSON for 30 days by default (extendable to 12 months), for analytics (C05) and compliance (Purview, F7). It is never read back into a conversation. SharePoint-grounded answers are stored `REDACTED`, which is a second reason it cannot act as memory.

## Try it (GitHub-harness copy, test pane)

1. Say: "Always address me as Dr Osei and keep answers under two sentences."
2. Start a new conversation. Ask Q2 from the lab. The agent addresses you as Dr Osei and keeps it short.
3. Open the agent in the maker portal. Find the stored fact. You cannot; open the memory portal as the user and you can, and you can delete it.
4. Now ask the product owner's question: "Can we use memory so the agent remembers the new £250 refund limit?" Write the answer: no; the limit is shared, must be governed and must survive 28 days of silence, so it goes in instructions or knowledge (and in a tool-side policy, C09), not in memory.

## Same thing elsewhere

| Copilot Studio                        | Foundry (F03 lab 04)                                    | AgentCore (B03 lab 04)                                                                 |
| ------------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| per-user memory, maker-blind, 28 days | memory store + memory search tool, developer-configured | AgentCore Memory, semantic / user-preference / episodic strategies, developer-readable |
| no developer read API                 | `MemorySearchTool`, scopes                              | `RetrieveMemoryRecords`, namespaces                                                    |
| user portal for deletion              | none built in                                           | record TTL                                                                             |

The design difference is deliberate: Copilot Studio treats memory as the user's property. If your scenario needs an agent-readable store of facts about a customer, that is a Dataverse table and a tool, not memory.
