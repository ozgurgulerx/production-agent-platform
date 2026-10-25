# S02: LLMs

Status: **Planned** (structure and scope set 23 October 2026; no chapter written yet).

The model layer from an architect's seat: what a model can do, what it costs, how to talk to it, how to pick one, how to adapt it. Serving internals live in T-Inference.

## Learning order

| Subsection | What it covers |
| --- | --- |
| [What a Model Is, for an Architect](S02.01-Models-for-Architects/README.md) | Capabilities and limits; nondeterminism; knowledge cutoff; hallucination as a design constraint; the API surface (messages, tools, structured output, streaming); what changes between model generations and what does not. |
| [Tokens, Context Windows and Cost](S02.02-Tokens-Context-and-Cost/README.md) | Tokens and tokenizers; input, cached, output and reasoning tokens; what fills a window (instructions, tools, results, history); effective versus nominal context; pricing models; the arithmetic behind S03.05. |
| [Prompting and Instruction Design](S02.03-Prompting-and-Instruction-Design/README.md) | System, developer, user and tool roles and the instruction hierarchy; delimiting data from instructions; structure, examples, output contracts; prompt versioning; what belongs in the prompt and what belongs in code (S03.05). |
| [Structured Output and Function Calling](S02.04-Structured-Output-and-Function-Calling/README.md) | JSON schema and strict mode; function calling as the model feature under every tool framework; parallel calls; failure modes (invalid JSON, wrong arguments); the bridge to S03. |
| [Reasoning Models](S02.05-Reasoning-Models/README.md) | What reasoning tokens buy and cost; effort controls and budgets; interleaved reasoning across tool calls; when a reasoning model helps (planning, ambiguity, recovery) and when it is waste. |
| [Model Selection and Routing](S02.06-Model-Selection-and-Routing/README.md) | Hosted versus open-weight; families and tiers; public benchmarks versus your own evals; routing by task, cost and latency; fallbacks; model deprecation and pinning. |
| [Adapting Models: Prompting, RAG or Fine-Tuning](S02.07-Adapting-Models/README.md) | The decision tree; SFT, preference and reinforcement fine-tuning, distillation; when fine-tuning pays (format, tone, narrow skills) and when it does not (facts, freshness); Foundry and Bedrock fine-tuning services. |
| [Multimodal and Voice](S02.08-Multimodal-and-Voice/README.md) | Images, documents and audio as inputs; voice agents and realtime APIs; what changes in latency, cost and evaluation; brief, with pointers. |
| [Caching and Batching Economics](S02.09-Caching-and-Batching-Economics/README.md) | Prompt caching mechanics and prefix discipline; batch APIs; when each pays; the interaction with tool loading and compaction (S03.05). |

[Back to AI Production Systems](../README.md)
