# G03 labs — run the ticket agent every way the platform allows

Runnable scaffolds for the G03 chapter. Setup is shared: do [`../../labs-setup/`](../../labs-setup/) first (venv, `.env` at the track root, `verify.sh` printing OK). Each lab README ends with a **proof checklist**; a lab is done when the boxes are ticked with real output. Map letters refer to [`../../reference/reading-map-gcp-agents-2026-10-25.md`](../../reference/reading-map-gcp-agents-2026-10-25.md).

```
labs/
├── 01-ways-to-run/            Runner in code, adk run, adk web, adk api_server, Cloud Run (ways 1-4)
├── 02-agent-runtime/          adk deploy agent_engine, SDK deploy, :query, revisions and traffic, Gemini Enterprise (ways 5, 6, 9)
├── 03-multi-agent-workflow/   SequentialAgent as ONE root_agent, deployed as ticket-agent-workflow
├── 04-memory-bank/            Sessions and Memory Bank: recall across sessions
└── 05-grounding-agent-search/ Agent Search tool in its own agent, wrapped in AgentTool (one built-in tool rule)
```

| Lab | Chapter section                           | Creates                                                                         | Time      |
| --- | ----------------------------------------- | ------------------------------------------------------------------------------- | --------- |
| 01  | §1 invocation surface, §2 ways 1–4        | `ticket-agent` (local folder `ticket_agent/`, Cloud Run service `ticket-agent`) | 1 session |
| 02  | §2 ways 5, 6, 9; §3 revisions and traffic | `ticket-agent` on Agent Runtime; `AGENT_RUNTIME_RESOURCE` in `.env`             | 1 session |
| 03  | §4 multi-agent                            | `ticket-agent-workflow` on Agent Runtime                                        | with 02   |
| 04  | §5 Sessions and Memory Bank               | nothing new; uses `AGENT_RUNTIME_RESOURCE`                                      | optional  |
| 05  | §6 grounding                              | `policy_agent` inside `ticket-agent`; needs `AGENT_SEARCH_DATASTORE` (G08)      | optional  |

Run them in order. 02 reuses the `ticket_agent/` folder from 01; 03 deploys with the same command as 02; 04 and 05 assume `AGENT_RUNTIME_RESOURCE` is set. G04 and G05 labs assume `ticket-agent` and `ticket-agent-workflow` exist on Agent Runtime, so finish 01–03 before moving on.

```bash
source ../../labs-setup/.venv/bin/activate
cd 01-ways-to-run && python run_local.py
```

Status on 25 Oct 2026: scaffold only, functionality unverified.

Next chapter: [`../../G04-Agent-Tooling-Identity-MCP-A2A/labs/`](../../G04-Agent-Tooling-Identity-MCP-A2A/labs/).
