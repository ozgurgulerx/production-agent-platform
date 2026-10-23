# S04: Agentic Workflows and Harnesses

Status: **In progress** (structure and scope set 23 October 2026; S04.09 drafted as a design proposal the same day; other chapters planned).

How an agent is actually run: the loop, the state, the patterns, the humans, the other agents, and the runtimes that host it. S03 gave the agent hands; S04 gives it a body.

## Learning order

| Subsection | What it covers |
| --- | --- |
| [The Agent Loop](S04.01-The-Agent-Loop/README.md) | From one model call to a harness: observe, decide, act, repeat; turn limits and stop conditions; parallel tool calls; where the loop runs (your code, an SDK, a managed runtime); the S03.02 loop revisited. |
| [Workflows versus Agents: The Patterns](S04.02-Workflows-versus-Agents/README.md) | Prompt chaining, routing, parallelisation, orchestrator-workers, evaluator-optimiser, and the autonomous loop; choosing the least agentic design that works; Anthropic's building-effective-agents framing with the ticket system as the example. |
| [State, Memory and Checkpoints](S04.03-State-Memory-and-Checkpoints/README.md) | Task state (host-written effects, model-written notes, user constraints), short-term and long-term memory, checkpoints and resume; what survives compaction; LangGraph checkpointers, Agent Framework threads, AgentCore Memory; absorbs the state material drafted in S03.05. |
| [Human in the Loop](S04.04-Human-in-the-Loop/README.md) | Approvals, elicitation, escalation and interrupts; binding approval to the exact action; approval fatigue; where the human sits in Foundry (`require_approval`), AgentCore and the Agents SDK; the S03.06 rules applied to the loop. |
| [Multi-Agent Systems](S04.05-Multi-Agent-Systems/README.md) | Handoffs, agents-as-tools, supervisor and worker, debate and critique; context isolation as the real benefit; coordination cost and when a single agent is better; typed handoff contracts. |
| [Agent-to-Agent Protocols: A2A and Beyond](S04.06-Agent-to-Agent-Protocols/README.md) | A2A agent cards, tasks and messages; MCP versus A2A (tools versus peers); discovery and trust between agents from different owners; identity propagation across agents; what is standardised today and what is not. |
| [Long-Running and Durable Agents](S04.07-Long-Running-and-Durable-Agents/README.md) | Background runs, the MCP tasks capability, durable execution (Durable Task, Temporal), crash recovery and replay without repeating side effects, deadlines and cancellation; the lost-response and restart cases from S05.04. |
| [Frameworks and Runtimes](S04.08-Frameworks-and-Runtimes/README.md) | OpenAI Agents SDK, Microsoft Agent Framework, LangGraph, Foundry Agent Service, Bedrock AgentCore Runtime, Vertex ADK: what each owns (loop, state, tools, approvals, tracing), how to choose, how to keep your policy out of the framework. |
| [Harness Engineering](S04.09-Harness-Engineering/README.md) | **Drafted (design proposal, 23 Oct 2026).** Harness versus runtime versus framework; the eight responsibilities (context compiler, capability compiler, policy gate, credential and sandbox boundary, budgets and stop conditions, effect ledger, approval binding, trace and eval surface); eleven sourced rules; the fault-injection list the capstone runs. Skills, computer-use and browser agents remain to be added. |
| [Capstone: The Ticket Agent End to End](S04.10-Capstone/README.md) | The support-ticket agent built on one runtime with everything above: loop, state, approvals, a second agent, durable execution, evals from S05 as the gate; the nine capstone scenarios run and reported. |

[Back to AI Production Systems](../README.md)
