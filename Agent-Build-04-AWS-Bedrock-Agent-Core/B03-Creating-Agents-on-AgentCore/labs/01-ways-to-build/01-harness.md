# Way 1 — AgentCore Harness (managed loop)

A Harness is the AgentCore-side agent definition: model, system prompt, tools, skills, memory, hooks and limits, stored and versioned by the service, with the loop (Strands-powered) running in AgentCore. It is the closest thing AWS has to a Foundry prompt agent. Preview 22 Apr 2026, GA Jun 2026, lifecycle hooks and interactive shells Sep 2026 (reading map B1).

## The CLI path
```bash
npm install -g @aws/agentcore                   # Node 20.12+; 1.0.0 released 22 Oct 2026
agentcore create --template agent-python-strands ticket-agent && cd ticket-agent
agentcore add harness                           # writes harness.yaml, registers it in agentcore/agentcore.json
agentcore deploy                                # thin CDK app: role, harness, DEFAULT endpoint
agentcore invoke --harness ticket_agent_harness "What is ticket T-1001 about?"
agentcore logs --harness ticket_agent_harness
agentcore remove all --yes && agentcore deploy --yes   # teardown
```
Do **not** `pip install bedrock-agentcore-starter-toolkit`; it is deprecated and shadows the `agentcore` binary (C1).

## The SDK twin
`01-harness-sdk.py` calls `create_harness` with the same fields the YAML holds, then drives the Converse-shaped `InvokeHarness` stream. Inline functions are **return of control**: the stream yields a `toolUse` block, your process runs the function and replies with a `toolResult` block in the next `messages`. For tools that must run server-side, point the harness at a Gateway (`type: agentcore_gateway`), which is where governance (Policy, B09) attaches.

## What to notice
- `executionRoleArn` is the harness's identity for `bedrock:InvokeModel` and tool calls, not yours.
- `runtimeSessionId` is required on every invoke (≥33 chars) and gives you the same session semantics as a Runtime.
- Versions: `harnessVersion` increments on update; `CreateHarnessEndpoint` pins a version exactly like Runtime endpoints.
- Memory can be attached as `agentCoreMemoryConfiguration` (your Memory resource) or `managedMemoryConfiguration` (service-created with strategies).
- `hooks` (Sep 2026) run before/after tool calls; `hookEvent` items appear in the stream with a `decision`.

Unverified on 25 Oct 2026: the exact YAML key spelling the CLI writes, the `inputSchema` wrapper (`{"json": {...}}` assumed from the Converse tool schema), and whether `create_harness` returns `harness` or a flat object. All three are marked `# verify` in the script.

**Interview line.** "A Harness is a prompt agent with AWS spelling: definition in the service, loop in the service, inline tools as return-of-control, everything else behind a Gateway."
