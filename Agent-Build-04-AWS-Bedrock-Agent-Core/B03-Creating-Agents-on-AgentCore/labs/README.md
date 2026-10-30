# B03 labs — build the ticket agent every way AgentCore allows

Runnable proofs for the B03 chapter. Setup is shared: do [`../../labs-setup/`](../../labs-setup/) first (venv, `.env` at the track root, `aws sso login`, `verify.sh` printing OK). Each lab README ends with a **proof checklist**; a lab is done when the boxes are ticked with real output. Nothing in this folder has been run against AWS yet (no account on 25 Oct 2026).

```
labs/
├── 01-ways-to-build/         harness (managed loop), runtime from code (zip), ephemeral Strands, one invocation surface, versions & endpoints
├── 02-runtime-containers/    runtime from a container (+ LangGraph, OpenAI Agents SDK), Instances (described), self-hosted on Lambda
├── 03-multi-agent/           Strands Graph in ONE runtime; A2A server + client across runtimes; Classic Agents migration appendix
└── 04-memory/                Memory resource with semantic + user-preference strategies; session manager on the agent
```

| Lab | Chapter section | Creates | Time |
|---|---|---|---|
| 01 | §1 one invocation surface, §2 ways 1, 2, 5, §3 versions and endpoints | `ticket_agent_harness`, `ticket_agent_code` | 1 session |
| 02 | §2 ways 3, 4, 6 | `ticket_agent_container`, a Lambda | 1 session |
| 03 | §4 multi-agent | `ticket_agent_graph`, `ticket_refund_a2a` | with 02 |
| 04 | side proof cited in §2 and §5 | `ticket_agent_memory` | optional |

Run them in order: 02, 03 and 04 import `_common.py` from 01 and reuse its `.env` keys. B04 and B05 labs assume `ticket_agent_code` (and its `TICKET_AGENT_RUNTIME_ARN`) exists, so finish 01 with `--keep` before moving on.

```bash
source ../../labs-setup/.venv/bin/activate
cd 01-ways-to-build && python 03-ephemeral-strands.py && python 02-runtime-code-deploy.py --keep
```

Next chapter: [`../../B04-AgentCore-Tooling-Identity-and-MCP/labs/`](../../B04-AgentCore-Tooling-Identity-and-MCP/labs/).
