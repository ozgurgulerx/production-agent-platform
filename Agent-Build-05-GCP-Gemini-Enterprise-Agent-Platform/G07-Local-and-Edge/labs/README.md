# G07 labs — Local and edge

No cloud needed to run the agent. Shared venv from [`../../labs-setup/`](../../labs-setup/) (it already pins `litellm>=1.84`, map H8) plus Ollama. The comparison step reads the G05 lab 02 evalset and, for the cloud side, the G03 lab 01 agent with ADC.

Status on 25 Oct 2026: scaffold only, functionality unverified.

```
labs/
└── 01-local-ticket-agent/
    ├── README.md                      goal, steps, proof checklist, cleanup
    ├── agent.py                       ticket-agent-local: LiteLlm(ollama_chat/gemma4:e4b) + stdio McpToolset (maps H8, D3)
    ├── ticket_mcp_stub.py             local stdio MCP server with get_ticket / list_tickets; TODO(learner) fills the handlers
    ├── compare_with_cloud.py          runs adk eval twice (local, cloud) on the G05 evalset, prints the two tables
    ├── requirements.txt               pins from ../../labs-setup/requirements.txt
    └── test_local_ticket_agent.py     pytest skeleton, TODO(learner)
```

| Lab | Chapter section                                                     | Creates                                                                                     | Time                                |
| --- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ----------------------------------- |
| 01  | §2 runtimes, §3 LiteLlm, §6 MCP stub in Gemini CLI, §7 what you own | a local Gemma 4 pull, a running stdio MCP stub, `ticket-agent-local`, two `adk eval` tables | ~45 minutes plus the model download |

## Run order

1. `ollama pull gemma4:e4b`, confirm `:11434` answers.
2. `adk run .` with the local agent; ask the three ticket questions.
3. `compare_with_cloud.py` on the G05 evalset; paste both tables into the lab README.
4. Optional: add the stub to `~/.gemini/settings.json` and call it from Gemini CLI.

Next chapter: [G08 — Knowledge: Agent Search and RAG Engine](../../G08-Knowledge-Agent-Search-RAG-Engine/), where the policy documents the agent cites get a managed home.
