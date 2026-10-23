# S03 exercise plan: cram first, then integrated exercises (21 Oct 2026)

Order of work: cram S03.01–06 chapter by chapter (see `S03-MCP-cram-plan.xlsx`), then do the four integrated exercises below. The per-chapter exercises in each README (S03.04 `EXERCISES.md`, S03.05 paper exercises, S03.06 parts A–E) are skipped for now and kept as reference; the integrated exercises cover the same ground across chapters at once. Do them in order; each assumes the previous one.

Rules: README closed while answering, open only for the self-check. Every exercise ends in a dated file under `S03-AI-Agents-Tools-and-MCP/exercises/`. Log misses in the quiz sheet the same day. Finish each exercise by saying its "defend it" questions out loud.

## The four integrated exercises

### X1. From system to tool set to contract (S03.04 + S03.03 + S03.06 §4–5) — 2.5 h

Pick a system you know that is not support tickets. Network operations fits: inventory, config, telemetry, change requests.

1. List 15–20 raw endpoints and five real tasks (one read, one multi-step, one write, one ambiguous, one impossible).
2. Derive 4–6 intent-level tools: trace raw call sequences, collapse fixed runs, apply the four boundary tests (one intent, one permission level, one failure model, reads separate from writes). Decide tool / resource / prompt for each.
3. Assign each tool a scope and say which checks are authentication, authorization and policy (S03.03 vocabulary).
4. Write the full contract for the riskiest write tool in the S03.04 §9 shape: definition, outcome table by channel (result, `isError`, HTTP 401/403), server execution sequence, five-row failure walkthrough including injected text in a result, a lost response after commit, and a race.
5. Write its task grant (S03.06 §5): principal, purpose, capabilities, resources, permitted recipient, mutation allowance, lifetime.

**Deliverable:** `exercises/X1-<system>.md`.
**Self-check:** no tool mixes read and consequential write; every required argument is obtainable; the walkthrough names the safe next step in every row; authority never comes from text in a result; the grant's identity fields are host-owned.
**Defend it:** S03.04 §11 questions 1–6 and "which check stops an allowed tool serving an unauthorized objective?"

### X2. Scale it: 50 tools, big results, long run (S03.05 + S03.04 §10) — 2 h

Take the X1 tool set and multiply it the way S03.05 does: eight regions plus two third-party servers, about 50 tools.

1. Name the tools so they survive prefixing; mark the near-duplicates you have created on purpose.
2. Write the sealed prediction sheet (template at the end): strategy × metric, with a reason per cell, where B's discovery fails first, where C will not help. Date it.
3. For one tool that returns a large result, design the four delivery patterns (download URL, chunked resource, projection, aggregate), the artifact envelope, and the follow-up question the aggregate cannot answer.
4. Write the 30-step investigation's checkpoint: what must survive compaction (goal, open work, exact ids and amounts, operation status, changed constraints) and what may be dropped.
5. State the minimum viable build you would run after S04, and the three failure kinds you would report (discovery, selection, arguments).

**Deliverable:** `exercises/X2-scale.md` with the sealed sheet.
**Self-check:** reduction ladder in the right order; truncation always flagged; handle carries id, hash, version; "summary is not an execution receipt" appears in the checkpoint rules; parallel calls and catalogue refresh are mentioned.
**Defend it:** S03.05's nine explain-it questions, plus "why can fewer tokens mean higher cost per successful task?"

### X3. Attack it: the trust boundary (S03.06 + S03.03 identity lifecycle) — 2.5 h

Use the X1 system and grant. A third-party server (the equivalent of `fx-rates`) is hostile.

1. Threat model in ten lines: attackers, goals, trusted base.
2. Six attacks against your X1 design: description poisoning, shadowing, rug pull, result injection, elicitation phishing, sampling abuse. Add final-output exfiltration and resource exhaustion. For each: what the model is steered to propose, which control stops it, and the backend assertion that proves it failed.
3. Fill the attack × defence matrix (attacks as rows; namespacing, approved-contract hashes, result labelling, elicitation gate, per-server allow-list, task grant, bound approval, egress control as columns). Mark cells "stops", "detects", "no effect".
4. Three traces in the S03.06 §10-B shape: authorized read, unauthorized export, unauthorized send; then the identity-lifecycle case: the user is deprovisioned while a confirmation is open. Who stops what?
5. Red-team your own spec: three attacks it does not stop, at least one not injection, each with the closing control and its false-denial cost.

**Deliverable:** `exercises/X3-trust-boundary.md` with the matrix.
**Self-check:** every attack has a backend assertion, not a model refusal; the matrix has at least one "no effect" cell you can explain; approval is bound to canonical arguments; the lifecycle case names the component, not "the system".
**Defend it:** the twelve questions in S03.06 §12, answered from your traces only.

### X4. Evaluate and decide (S03.04 §6 + S03.05 evaluation + S03.06 §11) — 1.5 h, paper now, build in S04

1. Design the eval for X1–X3 as one suite: twenty questions over the 50-tool catalogue (lookups, multi-region, ambiguous, impossible, near-duplicate traps, large results), four attack trials, one lifecycle trial. Development versus held-out split.
2. For each question: acceptable tool sequences, expected end state, deterministic checks. Attack trials score unauthorized effects and false denials separately.
3. Metrics table: task success, cost per successful task, wrong-tool rate split by failure kind, discovery recall@5, tokens (input, cached, output), calls, latency, unauthorized or duplicate effects.
4. Write the release-decision rule before running anything: what result would make you ship, hold, or revert a tool-design change ("selection improved but cost per success rose" must have an answer).
5. Map this to the S04 build: this suite is the S04 scenario set; the capstone steps from the coverage review (read → auth → confirmation → lost response → restart → injection → revocation → quota → decision) are its ordering.

**Deliverable:** `exercises/X4-eval-design.md`; becomes the S04 spec.
**Self-check:** every question has an end-state check; attacks score effects not words; held-out cases exist; the decision rule is written before results.
**Defend it:** "How do you prove consolidation helped rather than changing the task?", "What evidence would make you reverse your design?", "Would you ship?"

## Sequence

| Step | What | When | Time |
|---|---|---|---|
| 0 | Cram S03.01–06 per the cram plan; retrieval drills; misses to cards | first | 10–12 h |
| 1 | X1 | after the cram, one sitting | 2.5 h |
| 2 | X2 | next day | 2 h |
| 3 | X3 | next day | 2.5 h |
| 4 | X4 | next day; feeds S04 | 1.5 h |
| 5 | Closed-book redo of any self-check that failed; Anki for misses | following day | 1 h |
| 6 | Transfer test: repeat X1 steps 1–2 on an unseen domain (payments) in 45 min | end | 45 min |
| 7 | Commit `exercises/`; update the completion list | end | 30 min |

About 11 hours after the cram. If time is short, X1 and X3 are the two that produce interview stories; X2 and X4 can be compressed to their deliverables' tables.

## Prediction sheet template (X2 step 2)

| Strategy | Task success | Wrong-tool rate | Failed discovery | Tokens/task | Calls/task | Latency | Why I expect this |
|---|---|---|---|---|---|---|---|
| A ordered | | | n/a | | | | |
| A random | | | n/a | | | | |
| B keyword | | | | | | | |
| B embeddings | | | | | | | |
| C code mode | | | | | | | |

Where B will fail first: ______. Where C will not help: ______. Sealed on: ______.

## Per-chapter exercises (reference only, skipped for now)

- S03.04 `EXERCISES.md`: derive, contract, mini eval (X1 and X4 cover them).
- S03.05 paper exercises under "Plan": prediction sheet and large-result design (X2 covers them).
- S03.06 §10 A–E with the rubric: contracts, traces, fixture, limits, red-team (X3 covers them). Rubric: 4 = every field named with host-owned vs attacker-controlled distinguished and a backend assertion per attack; 0 = endpoints described as capabilities, model refusal counted as enforcement.
