"""Create the S00–S05 subchapter folders and scope READMEs for production-agent-platform.

Run from the repository root:  python3 create_s00_s05.py
Idempotent: never overwrites an existing README.md; prints what it created and what it skipped.
Section READMEs (S00/README.md etc.) are rewritten only if they are the 'Planned' placeholder.
"""

from pathlib import Path

ROOT = Path(".")

SECTIONS = {
    "S00-Enterprise-AI-and-Solution-Discovery": ("S00: Enterprise AI and Solution Discovery",
        "Before any architecture: which problems deserve an agent, what must exist first, what each action is allowed to cost, how the business case is measured, and how the work is run.", [
        ("S00.01-Use-Case-Discovery-and-Qualification", "Use-Case Discovery and Qualification",
         ["Turn 'we want AI' into one bounded workflow: operational truth, the discovery ladder, segment by risk then value, hard gates before scores, the wedge, the PRD as a decision contract."]),
        ("S00.02-Agent-Readiness", "Agent Readiness: Data, Systems, Identity, Risk",
         ["What has to exist before an agent can act: access classes per system, identity and scopes, data rules, named owners, the one-day workshop, hosting as a readiness input, the readiness checklist."]),
        ("S00.03-Decision-Economics-and-Action-Risk", "Decision Economics and Action Risk",
         ["Every safeguard is insurance: the failure-cost taxonomy, the reversibility ladder (gate, cap, audit, exile), write physics (timeout as unknown, idempotency from intent, verify-then-retry), audit on the failure path and full reconstruction."]),
        ("S00.04-Business-Case-and-Operating-Model", "Business Case and Operating Model",
         ["Cost per resolved task; containment versus true resolution; rollout gates with numbers; rollback triggers; degraded modes; who owns the agent in production; pilot-to-scale and capability transfer."]),
        ("S00.05-Build-Buy-Platform", "Build, Buy or Platform",
         ["Copilot Studio / Agentforce-style low-code, Foundry Agent Service, Bedrock AgentCore, Vertex Agent Builder, or custom on an SDK; decision criteria (control, identity, data residency, evals, cost); when a chatbot product is enough."]),
    ]),
    "S01-Production-AI-Application-Architecture": ("S01: Production AI Application Architecture",
        "The whole application an agent lives in: the request path, state, control plane, tenancy, cost and deployment. The diagram every later chapter zooms into.", [
        ("S01.01-Reference-Architecture", "Reference Architecture",
         ["The one diagram: client → gateway → orchestration/harness → model → tools (MCP) → data and backends, with state, policy, evals and observability as cross-cutting planes; what each box owns; where S02–S09 plug in."]),
        ("S01.02-Request-Path", "Request Path: Sync, Streaming, Async, Background",
         ["One user request end to end; streaming tokens and tool events; async and background runs for long tasks; timeouts, deadlines, cancellation; Foundry background mode and AgentCore runtime sessions."]),
        ("S01.03-State-Sessions-and-Storage", "State, Sessions and Storage",
         ["Conversation history, task state, artifacts, approvals and long-term memory as separate stores with separate owners; keys, versions, retention; what the model sees versus what the system records."]),
        ("S01.04-Control-Plane", "Control Plane: Routing, Config, Versioning, Release",
         ["Model routing and fallbacks, prompt and tool-definition versioning, feature flags, canary releases, config as code; evals as the release gate (S05); rollback."]),
        ("S01.05-Multi-Tenancy-and-Identity-Propagation", "Multi-Tenancy and Identity Propagation",
         ["Tenant isolation at every layer (prompt, tools, data, cache, traces); the user's identity carried to tools (OAuth passthrough, on-behalf-of) versus the agent's own identity; pointers to S03.03 and S08."]),
        ("S01.06-Cost-and-Latency-Budgets", "Cost and Latency Budgets",
         ["Where time and money go per request (prefill, decode, tools, retrieval); SLOs; prompt caching, batching, model tiers; cost per successful task; links to T-Inference for serving internals."]),
        ("S01.07-Deployment-Topologies", "Deployment Topologies",
         ["Foundry (Agent Service, Container Apps, Functions, private networking), Bedrock AgentCore (Runtime, Gateway), Vertex, and self-hosted (Kubernetes); where MCP servers run; network boundaries; the same ticket agent on each."]),
        ("S01.08-Reliability", "Reliability: Retries, Idempotency, Backpressure",
         ["Failure modes of an LLM app (timeouts, partial tool failure, rate limits, lost responses); retry budgets, idempotency keys, circuit breakers, graceful degradation; operation keys and reconciliation from S03.04 generalised."]),
    ]),
    "S02-LLMs": ("S02: LLMs",
        "The model layer from an architect's seat: what a model can do, what it costs, how to talk to it, how to pick one, how to adapt it. Serving internals live in T-Inference.", [
        ("S02.01-Models-for-Architects", "What a Model Is, for an Architect",
         ["Capabilities and limits; nondeterminism; knowledge cutoff; hallucination as a design constraint; the API surface (messages, tools, structured output, streaming); what changes between model generations and what does not."]),
        ("S02.02-Tokens-Context-and-Cost", "Tokens, Context Windows and Cost",
         ["Tokens and tokenizers; input, cached, output and reasoning tokens; what fills a window (instructions, tools, results, history); effective versus nominal context; pricing models; the arithmetic behind S03.05."]),
        ("S02.03-Prompting-and-Instruction-Design", "Prompting and Instruction Design",
         ["System, developer, user and tool roles and the instruction hierarchy; delimiting data from instructions; structure, examples, output contracts; prompt versioning; what belongs in the prompt and what belongs in code (S03.05)."]),
        ("S02.04-Structured-Output-and-Function-Calling", "Structured Output and Function Calling",
         ["JSON schema and strict mode; function calling as the model feature under every tool framework; parallel calls; failure modes (invalid JSON, wrong arguments); the bridge to S03."]),
        ("S02.05-Reasoning-Models", "Reasoning Models",
         ["What reasoning tokens buy and cost; effort controls and budgets; interleaved reasoning across tool calls; when a reasoning model helps (planning, ambiguity, recovery) and when it is waste."]),
        ("S02.06-Model-Selection-and-Routing", "Model Selection and Routing",
         ["Hosted versus open-weight; families and tiers; public benchmarks versus your own evals; routing by task, cost and latency; fallbacks; model deprecation and pinning."]),
        ("S02.07-Adapting-Models", "Adapting Models: Prompting, RAG or Fine-Tuning",
         ["The decision tree; SFT, preference and reinforcement fine-tuning, distillation; when fine-tuning pays (format, tone, narrow skills) and when it does not (facts, freshness); Foundry and Bedrock fine-tuning services."]),
        ("S02.08-Multimodal-and-Voice", "Multimodal and Voice",
         ["Images, documents and audio as inputs; voice agents and realtime APIs; what changes in latency, cost and evaluation; brief, with pointers."]),
        ("S02.09-Caching-and-Batching-Economics", "Caching and Batching Economics",
         ["Prompt caching mechanics and prefix discipline; batch APIs; when each pays; the interaction with tool loading and compaction (S03.05)."]),
    ]),
    "S04-Agentic-Workflows-and-Harnesses": ("S04: Agentic Workflows and Harnesses",
        "How an agent is actually run: the loop, the state, the patterns, the humans, the other agents, and the runtimes that host it. S03 gave the agent hands; S04 gives it a body.", [
        ("S04.01-The-Agent-Loop", "The Agent Loop",
         ["From one model call to a harness: observe, decide, act, repeat; turn limits and stop conditions; parallel tool calls; where the loop runs (your code, an SDK, a managed runtime); the S03.02 loop revisited."]),
        ("S04.02-Workflows-versus-Agents", "Workflows versus Agents: The Patterns",
         ["Prompt chaining, routing, parallelisation, orchestrator-workers, evaluator-optimiser, and the autonomous loop; choosing the least agentic design that works; Anthropic's building-effective-agents framing with the ticket system as the example."]),
        ("S04.03-State-Memory-and-Checkpoints", "State, Memory and Checkpoints",
         ["Task state (host-written effects, model-written notes, user constraints), short-term and long-term memory, checkpoints and resume; what survives compaction; LangGraph checkpointers, Agent Framework threads, AgentCore Memory; absorbs the state material drafted in S03.05."]),
        ("S04.04-Human-in-the-Loop", "Human in the Loop",
         ["Approvals, elicitation, escalation and interrupts; binding approval to the exact action; approval fatigue; where the human sits in Foundry (`require_approval`), AgentCore and the Agents SDK; the S03.06 rules applied to the loop."]),
        ("S04.05-Multi-Agent-Systems", "Multi-Agent Systems",
         ["Handoffs, agents-as-tools, supervisor and worker, debate and critique; context isolation as the real benefit; coordination cost and when a single agent is better; typed handoff contracts."]),
        ("S04.06-Agent-to-Agent-Protocols", "Agent-to-Agent Protocols: A2A and Beyond",
         ["A2A agent cards, tasks and messages; MCP versus A2A (tools versus peers); discovery and trust between agents from different owners; identity propagation across agents; what is standardised today and what is not."]),
        ("S04.07-Long-Running-and-Durable-Agents", "Long-Running and Durable Agents",
         ["Background runs, the MCP tasks capability, durable execution (Durable Task, Temporal), crash recovery and replay without repeating side effects, deadlines and cancellation; the lost-response and restart cases from S05.04."]),
        ("S04.08-Frameworks-and-Runtimes", "Frameworks and Runtimes",
         ["OpenAI Agents SDK, Microsoft Agent Framework, LangGraph, Foundry Agent Service, Bedrock AgentCore Runtime, Vertex ADK: what each owns (loop, state, tools, approvals, tracing), how to choose, how to keep your policy out of the framework."]),
        ("S04.09-Harness-Engineering", "Harness Engineering",
         ["Context compilation per turn, tool loadout, skills and procedure graphs, sandboxes and code mode, computer-use and browser agents, prompt caching discipline; the operational craft that makes a loop reliable."]),
        ("S04.10-Capstone", "Capstone: The Ticket Agent End to End",
         ["The support-ticket agent built on one runtime with everything above: loop, state, approvals, a second agent, durable execution, evals from S05 as the gate; the nine capstone scenarios run and reported."]),
    ]),
}

def write(path: Path, text: str) -> str:
    if path.exists() and "Status: **Planned**." not in path.read_text(encoding="utf-8"):
        return f"skip   {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return f"wrote  {path}"

for folder, (title, lead, stages) in SECTIONS.items():
    rows = "\n".join(f"| [{name}]({slug}/README.md) | {scope[0]} |" for slug, name, scope in stages)
    section_readme = f"""# {title}

Status: **Planned** (structure and scope set 23 October 2026; no chapter written yet).

{lead}

## Learning order

| Subsection | What it covers |
| --- | --- |
{rows}

[Back to AI Production Systems](../README.md)
"""
    print(write(ROOT / folder / "README.md", section_readme))
    for slug, name, scope in stages:
        body = "\n\n".join(scope)
        stage_readme = f"""# {slug.split('-')[0]}: {name}

Status: **Planned** (scope only).

{body}

[Back to {title.split(':')[0]}](../README.md)
"""
        print(write(ROOT / folder / slug / "README.md", stage_readme))
