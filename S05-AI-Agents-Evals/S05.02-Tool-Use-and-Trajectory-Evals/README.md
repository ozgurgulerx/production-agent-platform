# S05.02: Tool-Use and Trajectory Evals

Status: **Drafted 23 October 2026; no harness or results yet.** This is the dedicated section on evaluating agents that use tools. It is fed by S03.04 (tool design), S03.05 (context efficiency) and S03.06 (trust boundary), and it is the harness those chapters reuse. General eval discipline (gold labels, held-out sets, repeats, judges) is in S05.01 and not repeated here.

## Why a separate section

"The agent picked the right tool" is several different claims: it found the tool, chose it over its neighbours, filled the arguments correctly, called things in a sensible order, left the backend in the right state, did so every time, at an acceptable cost, and did nothing it was not allowed to do. Each is a different measurement with a different failure to diagnose. Scoring only the final answer hides all of them: a model can reach the right answer by a wasteful or lucky path.

## The nine eval types

| Type | Question | How it is done | Diagnoses |
|---|---|---|---|
| **Tool selection** | Did it pick the right tool, or an acceptable one? | Gold label per case: the acceptable tool set. Wrong-tool rate = incorrect selections / tool calls; also tasks with at least one wrong selection | Overlapping tools, vague descriptions (S03.04 §1–2) |
| **Discovery** | Was the right tool even available to choose? | For tool search and filters: discovery recall@k = relevant tools in the first k retrieved / relevant tools for an acceptable solution; also whether all required tools for one acceptable solution were loaded | Search quality, namespace routing, over-narrow filters (S03.05 B) |
| **Argument correctness** | Right tool, right arguments? | Two layers: schema validation catches malformed arguments; hand-labelled expected arguments catch schema-valid-but-wrong ones (the "next Friday" date, the wrong customer id) | Loose schemas, missing "where this argument comes from" in descriptions (S03.04 §2) |
| **Trajectory** | Was the sequence of calls sensible? | Compare the call trace to acceptable sequences; allow equivalent valid paths; penalise redundant calls, retries with unchanged arguments, a read not followed by the required confirmation, and a consequential call made without it | Planning, error recovery, missing next-step hints in errors (S03.04 §3) |
| **End state** | Did the backend end up right? | Deterministic check of final state (ledger, ticket status, notifications sent) against the expected state; the τ-bench method. A denial message with a changed ledger is a failure | Authority, idempotency, partial failure (S03.04 §4) |
| **Reliability** | Does it succeed every time, not once? | Run each case k times; report pass^k (all k succeed) beside pass@1; look at per-case variation | Nondeterminism, ambiguous tools, fragile prompts |
| **Efficiency** | At what cost? | Tokens (input, cached, output, reasoning), calls, model turns, backend calls counted separately from model-visible calls, latency, and cost per successful task = total spend across all attempts / successful tasks | Context strategy (S03.05); never a reason to trade away correctness or safety |
| **Safety and authority** | Did anything unauthorized or duplicate happen? | Attack trials and direct policy probes (submit the prohibited call straight to the gate, so a model refusal cannot hide missing enforcement); score effects in the backend and captured egress, not model wording; also false denials on benign tasks and approvals per completed task | Trust boundary (S03.06 §11) |
| **Judgement quality** | Was the final answer good where there is no exact check? | A model judge with a fixed rubric, calibrated against human grades on a sample, independent of which variant produced the answer; never a substitute for the end-state check | Explanation quality, summaries |

A tenth, **robustness**, is a dimension across the others rather than a type: run on two model families and on paraphrased and held-out questions, and report whether gains hold.

## The harness

One harness serves S03.04, S03.05 and S03.06. Its parts:

1. **Catalogue and fixtures.** The support-ticket servers (curated set from S03.04; the 50-tool regional catalogue from S03.05; the hostile `fx-rates` server from S03.06), a mock backend with a resettable ledger, fake secrets and an inert notification sink that captures egress.
2. **Cases.** About twenty questions per comparison: single-tool lookups, multi-step and multi-region tasks, ambiguous requests ("Smith"), impossible requests, near-duplicate traps, large-result tasks, plus attack trials and one identity-lifecycle trial. Each case records: acceptable tools or sequences, expected arguments where exact, expected end state, expected final-answer fields, and whether confirmation is required. Development and held-out splits.
3. **Runner.** Pinned model versions; fixed sampling, reasoning and parallel-call settings; reset mutable state between trials; k repeats per case; the same execution budgets across variants. Records the full trace: every model turn, tool call, arguments, result size, proxied backend calls, usage fields, stop reasons, latency.
4. **Scorers.** Deterministic checks for selection, discovery, arguments, trajectory, end state, duplicates and confirmations; a calibrated judge only for answer quality.
5. **Report.** A table of variant × model × metric with counts and percentages, per-case variation, and the traces behind every failure. Treat an improvement as a hypothesis confirmed on held-out cases, not a verdict.

**Minimum first build** (the 1 November target): the curated catalogue, ten development and four held-out cases, k = 3, one model, selection / arguments / end-state / efficiency scorers, and the direct policy probes for `issue_refund`. The three-variant tool-design comparison from S03.04 §6 (raw, raw with better descriptions, curated) is the first experiment; the context-strategy comparison from S03.05 is the second.

## What the chapters ask of this section

| Chapter | Experiment | Primary metrics |
|---|---|---|
| S03.04 | Raw vs improved-descriptions vs curated tools | Task success, wrong-tool rate, argument errors, calls, tokens |
| S03.05 | All-tools (ordered, random) vs tool search (keyword, embeddings, namespace, native) vs code mode; large-result delivery patterns; optional 30-step masking comparison | Cost per successful task, schema-token share, discovery recall@5, peak and cumulative input, cached tokens, failed discovery, latency, unauthorized or duplicate effects |
| S03.06 | Variants A–E (broad exposure → bound approvals and isolation) against the six attacks plus output exfiltration and resource exhaustion | Unauthorized effects per trial, prohibited disclosures, false denials, approvals per completed task, policy latency |

## Tooling

Build your own harness first; it is the better interview story and it fits the fixtures. Off the shelf: MCPJam (agent traces, model comparison, test suites) and Promptfoo (evals and MCP red-teaming) as alternatives; MCP Inspector for protocol debugging, not evaluation; the MCP Conformance framework for the protocol layer, which answers a different question. Public references for method: τ-bench (end-state checks, pass^k), BFCL-style suites for tool-call correctness.

## What you should be able to explain

1. Why final-answer accuracy is not enough for a tool-using agent.
2. The difference between a discovery failure, a selection failure and an argument failure, with an example of each.
3. Why end state is checked in the backend and never from the model's wording.
4. What pass^k measures that pass@1 does not.
5. How to prove consolidation helped rather than changing the task.
6. Why cost per successful task, not tokens per call.
7. How attack trials are scored, and why prohibited calls are also submitted directly to the gate.
8. When a model judge is acceptable and what it must never replace.

[Back to S05](../README.md)
