# F03 labs — build the ticket agent every way Foundry allows

Runnable proofs for the F03 chapter. Setup is shared: do [`../../labs-setup/`](../../labs-setup/) first (venv, `.env` at the track root, `verify.sh` printing OK). Each lab README ends with a **proof checklist**; a lab is done when the boxes are ticked with real output.

```
labs/
├── 01-seven-ways/            prompt agent (portal, SDK, azd), voice, ephemeral, FoundryAgent, one invocation surface, versions & publish
├── 02-hosted-agents/         hosted from source, from a container (+ LangGraph, OpenAI Agents SDK), self-hosted on Container Apps
├── 03-multi-agent-workflow/  Agent Framework workflow hosted as ONE agent; retiring Foundry declarative workflow as appendix
├── 04-memory/                memory store + memory search tool (preview)
└── 05-knowledge-ai-search/   Azure AI Search tool grounding (Foundry IQ knowledge base = follow-up)
```

| Lab | Chapter section | Creates | Time |
|---|---|---|---|
| 01 | §1 one invocation surface, §2 ways 1–4, §3 versions and publish | `ticket-agent-prompt` | 1 session |
| 02 | §2 ways 5–7 | `ticket-agent-hosted-code`, `ticket-agent-hosted` | 1 session |
| 03 | §4 multi-agent | `ticket-agent-workflow` | with 02 |
| 04, 05 | side proofs cited in §2 | agents with memory / AI Search | optional |

Run them in order: 02 and 03 reuse the `.env` and the invoke script from 01. F04 and F05 labs assume the three agents above exist, so finish 01–03 before moving on.

```bash
source ../../labs-setup/.venv/bin/activate
cd 01-seven-ways && python 02-prompt-agent-sdk.py --keep
```

Next chapter: [`../../F06-Agent-Tooling-MCP-and-Integration/labs/`](../../F06-Agent-Tooling-MCP-and-Integration/labs/).
