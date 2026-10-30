# F04 labs — identity, tools and MCP for the ticket agent

Runnable proofs for the F04 chapter. Setup is shared: [`../../labs-setup/`](../../labs-setup/). These labs assume the agents from F03 labs 01–03 exist (`ticket-agent-prompt`, `ticket-agent-hosted-code`, `ticket-agent-workflow`). Each lab README ends with a **proof checklist**.

```
labs/
├── 01-identity-conditional-access/  agent identity, blueprints, Conditional Access proof
├── 02-mcp-tool/                     the `mcp` tool and its approval loop; Logic Apps Standard as an MCP host
├── 03-toolbox/                      many MCP servers behind one toolbox; versions; tool search
├── 04-mcp-auth-apim/                the six connection auth types, OAuth consent, APIM AI Gateway in front
├── 05-private-tool-catalog/         API Center registration → Foundry tool catalog
└── 06-a2a/                          A2A tool v1.0; Logic Apps calling the agent
```

| Lab | Chapter section | Needs beyond the shared setup |
|---|---|---|
| 01 | §1 identity, §4 Entra Agent ID + Conditional Access | Entra admin to see the agent identity and create a CA policy |
| 02 | §5 MCP tool, approval loop | nothing (falls back to the public Learn MCP server) |
| 03 | §5 toolbox, tool search | nothing |
| 04 | §2 auth types, §3 OAuth passthrough, §8 APIM | an app registration for the `oauth2` row; APIM optional |
| 05 | §8 private tool catalog | an API Center instance |
| 06 | §7 A2A | a second agent (F03 lab 03 workflow agent works) |

Order: 01 → 02 → 03 → 04 → 05 → 06. Session 3 is 01–03, session 4 is 04–06.

```bash
source ../../labs-setup/.venv/bin/activate
cd 02-mcp-tool && python mcp_tool_demo.py
```

Next chapter: [`../../F08-Evals-Tracing-and-Release/labs/`](../../F08-Evals-Tracing-and-Release/labs/).
