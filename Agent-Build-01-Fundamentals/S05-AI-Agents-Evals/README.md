# S05: AI Agents Evals

Status: **In progress** (structure and the tool-use section drafted 23 October 2026; no harness or results yet).

This section is where the proposals in S03.04 (tool design), S03.05 (context efficiency) and S03.06 (trust boundary) turn into measured evidence. The first build target is the tool-use and trajectory harness in S05.02, run on the support-ticket catalogue, with the capstone scenarios in S05.04 as the suite.

## Learning order

| Subsection | What it covers |
| --- | --- |
| [S05.01: Eval Foundations](S05.01-Eval-Foundations/README.md) | What to measure and how to trust it: gold labels, development vs held-out sets, repeats and pass^k, deterministic checks vs model judges, reporting |
| [S05.02: Tool-Use and Trajectory Evals](S05.02-Tool-Use-and-Trajectory-Evals/README.md) | The dedicated section on agents using tools: selection, arguments, trajectory, end state, reliability, efficiency, safety; the harness reused by S03.04–06 |
| [S05.03: RAG Evals](S05.03-RAG-Evals/README.md) | Retrieval and answer-quality evals; ties to S06 |
| [S05.04: Agent Task Evals](S05.04-Agent-Task-Evals/README.md) | End-to-end task suites: the capstone scenarios, cost per successful task, the release decision |
| [S05.05: Eval Ops](S05.05-Eval-Ops/README.md) | Evals in CI as regression gates, production trace sampling, drift |

Start with S05.01, then S05.02; S05.04 is the build target for 1 November. S05.03 waits for S06. S05.05 is added once there is a harness to put in CI.

## Eval tools and systems

A map of what exists, so each subsection can say "use X" without re-explaining it. Grouped by what they are for. Names and features from general knowledge as of mid-2026; check current docs and licences before adopting one.

**Harness and assertion frameworks (open source)**

| Tool | What it is for | Fit here |
|---|---|---|
| Promptfoo | Declarative test cases over prompts, agents and tools; assertions, model comparison, CI; an MCP red-team module | S03.06 attack trials; CI gates in S05.05 |
| Inspect AI (UK AI Security Institute) | Python framework for agent and tool-use evals with sandboxed tool execution, scorers and logs | Trajectory and end-state evals in S05.02; the sandbox fits code mode |
| DeepEval | pytest-style LLM evals with built-in metrics (faithfulness, answer relevancy, tool correctness) and judge calibration | Unit-test feel for S05.02 scorers |
| Ragas | RAG metrics: context precision/recall, faithfulness, answer correctness; test-set generation | S05.03 |
| OpenAI Evals | Registry-style eval definitions and runners against OpenAI models | Reference for case format; less used for agents |
| lm-evaluation-harness (EleutherAI) | Academic benchmark runner for base models | Model selection only; not agent evals |
| MLflow evaluate / TruLens / Giskard | Evaluation and testing suites attached to broader ML tooling; TruLens emphasises RAG feedback functions, Giskard scanning for vulnerabilities | Optional; useful if the platform is already in use |

**Tracing and observability with evals attached**

| Tool | What it is for | Fit here |
|---|---|---|
| Langfuse (open source) | Traces, prompt management, datasets, scores, judges; self-hostable | Trace store for S05.02 and S05.05; cost per success from usage fields |
| Arize Phoenix (open source) | OpenTelemetry-based tracing and evals for LLM apps and agents | Same role; OTel fits the MCP trace-context direction |
| LangSmith | Tracing, datasets and evals for LangChain/LangGraph and others; hosted | If the harness is LangGraph-based |
| Weights & Biases Weave | Tracing and evaluations with versioned datasets | Alternative trace store |
| Braintrust | Hosted evals and logs with a playground and scorers | Alternative; commercial |

**Platform-native**

| Platform | What it offers | Fit here |
|---|---|---|
| Microsoft Foundry (`azure-ai-evaluation` SDK, portal evaluations, continuous evaluation) | Built-in quality, safety and agent evaluators (tool call accuracy, intent resolution, task adherence), simulators for adversarial inputs, evaluation runs tied to a project | S03.03b and any Foundry-hosted variant; agent evaluators map to S05.02 types |
| Amazon Bedrock evaluations and AgentCore | Model and RAG evaluations; AgentCore observability for agent traces | AWS-hosted variants |
| Google Vertex AI Gen AI evaluation | Pointwise and pairwise evaluators, agent evaluation templates | GCP-hosted variants |

**Benchmarks and public suites (method references, not tools)**

| Suite | What it measures | Fit here |
|---|---|---|
| τ-bench | Tool use under domain policies; end-state scoring; pass^k | The method S05.01 and S05.02 adopt |
| BFCL (Berkeley Function Calling Leaderboard) | Function-call correctness, single and multi-turn, parallel calls | Argument and selection scorers |
| AgentDojo, InjecAgent | Prompt-injection attacks on tool-using agents; utility under attack | S03.06 attack trials |
| MCPTox, MCP-SafetyBench | Tool poisoning and safety on real MCP servers | S03.06 adversarial fixture references |
| RAG-MCP | Tool-selection accuracy with retrieval vs all-in-prompt | S03.05 strategy B motivation |

**MCP-specific**

| Tool | What it is for | Fit here |
|---|---|---|
| MCP Inspector | Interactive protocol debugging: list tools, call them, inspect messages and auth | Debugging, not evaluation |
| MCP Conformance framework | Automated protocol-compliance checks for clients and servers | The protocol layer; S03.03b |
| MCPJam | Debug server calls, agent traces, model comparison, test suites | Off-the-shelf alternative to the S05.02 harness |
| MCP-Scan / Snyk Agent Scan | Static scanning of tool descriptions and configurations for poisoning | S03.06; detection, not proof of runtime safety |

**How to choose, for this repo:** build the S05.02 harness yourself (it is small and it is the interview story), store traces in Langfuse or Phoenix, use Promptfoo for the S03.06 attack suite and CI gate, Ragas for S05.03, and the Foundry evaluators when a variant runs on Foundry. Benchmarks are for method and for sanity-checking your own numbers, not for replacing a suite built on your own catalogue.

[Back to AI Production Systems](../README.md)
