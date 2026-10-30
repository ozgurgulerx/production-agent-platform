# Appendix — Amazon Bedrock Agents Classic, and `agentcore migrate`

The managed agents you may have built in 2024–2025 (agent + action groups + knowledge base + guardrail, `InvokeAgent`, supervisor/collaborator "multi-agent collaboration", `InvokeInlineAgent`) are now **Amazon Bedrock Agents Classic** (B7, page fetched 25 Oct 2026):

- maintenance mode: no new features, model catalogue frozen
- closed to accounts without 12 months of prior usage from **30 Jul 2026** (`CreateAgent` and `InvokeInlineAgent` return 403)
- no end-of-life date and no exception process announced
- Knowledge Bases and Guardrails are unaffected (they are separate services)

This is the Foundry "declarative workflows retire 1 Dec 2026" box with AWS spelling: do not start anything new on it, and move what exists.

## Mapping
| Classic | AgentCore |
|---|---|
| Agent (prompt, model) | Harness (recommended) or a code-defined agent on Runtime |
| Action group (Lambda / OpenAPI) | Gateway target (Lambda, OpenAPI, Smithy) exposed as MCP tools |
| Knowledge base attached to the agent | Gateway Managed-KB target (`Retrieve`, `AgenticRetrieveStream`) |
| Return of control | Harness inline function tools, or your own tool in the Runtime container |
| Guardrail on the agent | Guardrails-in-Policy on the Gateway, or `BedrockModel(guardrail_id=...)` in Strands |
| Supervisor + collaborators | Strands agents-as-tools / Graph / Swarm in one Runtime; A2A across Runtimes |
| Inline agent | Harness invoked with per-call `model`, `systemPrompt`, `tools` overrides (`InvokeHarness` accepts them) |
| Session (`sessionId`) | `runtimeSessionId` |

## The command
```bash
agentcore migrate                                   # AgentCore CLI 1.0 (22 Oct 2026); inspects Classic agents in the account
agentcore add runtime --agent-id <classic-agent-id> --framework strands   # imports one Classic agent as Strands code on Runtime
```
The `amazon-bedrock` skill in the agent-toolkit-for-aws automates the same mapping for coding agents (B7). Routing-mode supervisors have no one-to-one target ("not straightforward" in the AWS guide); inline-agent guidance was still "forthcoming" on 25 Oct 2026.

**Interview line.** "Classic is closed to new accounts since July 2026. Action groups become Gateway targets, the agent becomes a Harness, and the supervisor becomes a Strands graph."
