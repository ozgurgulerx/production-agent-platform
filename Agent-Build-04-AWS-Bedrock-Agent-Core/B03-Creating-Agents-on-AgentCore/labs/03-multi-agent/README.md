# 03 — Multi-agent: one Runtime, or many over A2A

Two patterns, one scenario. Inside one Runtime, a Strands **Graph** routes triage → refund specialist or info desk; the Runtime sees a single `/invocations` and a single trace tree. Across Runtimes, the refund specialist is an **A2A** server on port 9000 with an agent card, and a client (another agent, or a Gateway HTTP target in B04 lab 06) sends it tasks over JSON-RPC without ever seeing its tools. The appendix covers Classic Bedrock Agents and `agentcore migrate`.

```
03-multi-agent/
├── graph_agent/main.py        GraphBuilder triage -> refunds | info, served by BedrockAgentCoreApp
├── a2a_server/main.py         serve_a2a(StrandsA2AExecutor(...), AgentCard) on 9000
├── a2a_client.py              A2ACardResolver + ClientFactory through the Runtime URL, SigV4
├── deploy_multi.py            creates ticket_agent_graph (HTTP) and ticket_refund_a2a (A2A) from zips
└── appendix-classic-agent-migration/
```

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
cd 03-multi-agent
python deploy_multi.py --keep            # two runtimes; writes TICKET_GRAPH_RUNTIME_ARN and TICKET_A2A_RUNTIME_ARN
TICKET_AGENT_RUNTIME_ARN=$TICKET_GRAPH_RUNTIME_ARN python ../01-ways-to-build/04-invoke-everything.py
python a2a_client.py                     # card, then one refund task; expect the 480 GBP refusal
python deploy_multi.py --cleanup
```
Local check without AWS: `cd a2a_server && python main.py` then `curl localhost:9000/.well-known/agent-card.json`.

## What it proves
- Multi-agent inside one Runtime costs nothing extra in the platform: one session, one version, one endpoint; the graph's `execution_order` is returned so you can see the route taken.
- `serverProtocol` (HTTP | MCP | A2A | AGUI) is a Runtime property; the same `create_agent_runtime` creates both.
- A2A is the trust boundary: the client gets a card and a task result. Tools, prompts and model stay private to the server.
- Gateway can front an A2A Runtime as an HTTP passthrough target (D3), which is how Policy applies to agent-to-agent calls.

## Proof checklist
- [ ] `deploy_multi.py` prints READY for both runtimes
- [ ] invoking the graph with "Refund 4.50 on T-1001" returns `path: ['triage', 'refunds']`; "What is T-1001 about?" returns `['triage', 'info']`
- [ ] `a2a_client.py` prints the card with skill `refund` and the task result contains `refused` for 480 GBP
- [ ] the local `curl` on 9000 returns the agent card JSON
