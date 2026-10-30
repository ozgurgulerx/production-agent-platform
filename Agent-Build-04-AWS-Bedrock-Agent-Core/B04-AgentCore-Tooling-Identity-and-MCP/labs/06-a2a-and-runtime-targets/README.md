# 06 — A2A and agents as Gateway targets

**Start with the failure.** Two Runtimes need to talk. The quick fix is to give agent A the ARN of agent B and `InvokeAgentRuntime` on it. Now B's audit log says "A's execution role" for every human request, and the 90/10 rollout of B v2 has nowhere to live. This lab routes A→B through the Gateway instead.

## Goal
Register the B03 ticket Runtime as an `agentcoreRuntime` HTTP target (`CALLER_IAM_CREDENTIALS`), add an A2A passthrough target to the B03 refund specialist (`JWT_PASSTHROUGH`, session stickiness), fetch its agent card through the Gateway path, and write a weighted rule for a canary.

## You will end with
- `TICKET_AGENT_TARGET_ID`, `REFUND_A2A_TARGET_ID`, `TICKET_CANARY_RULE_ID` in `.env`
- a SigV4 call to `https://<gwId>.gateway.bedrock-agentcore.<region>.amazonaws.com/ticket-agent/invocations` answered by the agent
- the specialist's agent card fetched through the Gateway

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
cd 06-a2a-and-runtime-targets
python runtime_as_gateway_target.py     # needs TICKET_AGENT_RUNTIME_ARN (B03 lab 01)
python a2a_passthrough_target.py        # needs TICKET_A2A_RUNTIME_ARN (B03 lab 03)
python gateway_rule_weighted.py         # needs a second target named ticket-agent-v2 (repeat the first script with a v2 endpoint)
```

## Facts that matter
- Runtime A2A: `serverProtocol: A2A`, container on **9000** at `/`, card at `/.well-known/agent-card.json`, `serve_a2a(executor, agent_card)` in the SDK, `get_agent_card` on the data plane.
- HTTP targets (GA Jul 2026) are path-routed (`/<targetName>/invocations`), not aggregated, not searchable; credential types `CALLER_IAM_CREDENTIALS` or `JWT_PASSTHROUGH`.
- A2A passthrough is `protocolType: A2A` on a `passthrough` target; stickiness keeps one Runtime session per conversation. Card federation across Gateways is still "coming" per the FAQ.
- Rules (`create_gateway_rule`): priority, conditions on principal/path/model, `staticRoute` or `weightedRoute` with fallback and circuit breaker. This is the only traffic split on AgentCore.
- Signing: Gateway HTTP targets with IAM are called with SigV4; the service name used by the lab is `bedrock-agentcore` (marked verify).

## Proof (checklist)
- [ ] `get_gateway_target` for `ticket-agent` is `READY` with `protocolType` reflecting HTTP
- [ ] the SigV4 call returns 200 and the ticket Runtime's CloudWatch log shows the **caller's** role, not the Gateway role
- [ ] the agent card JSON names the specialist's skills and its `url` is the Runtime invocations URL
- [ ] the weighted rule is `ACTIVE`; 20 calls land roughly 18/2 across the two Runtime log groups

## Next
B05: traces and evaluations for everything built so far.
