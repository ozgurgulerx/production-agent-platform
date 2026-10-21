# S03.04–06 exercise plan (21 Oct 2026)

The three chapters each end in exercises, but of different kinds: S03.04 has a one-line design prompt, S03.05 has a seven-step build plan with a minimum-viable subset, S03.06 has a four-part specification exercise plus two tooling TODOs. None of them yet produces a dated artefact you can show, and none has a self-check that catches a wrong answer. This file fixes both, then lays out eight sessions.

## What the current exercises are missing

| Chapter | Current exercise | What is missing | Fix |
|---|---|---|---|
| S03.04 | "Pick a system, list endpoints, derive tools, write one contract" (one paragraph at the end of the README) | No time box, no deliverable shape, no self-check, no retrieval step; uses the same ticket domain the reader just read | `EXERCISES.md` with three exercises (derive, contract, mini eval), each with a deliverable and self-check; a system other than tickets; an out-loud step after exercise 2 |
| S03.05 | Seven build steps with a minimum-viable subset | Entirely a build; nothing to do on paper before S04 exists; no "predict first" step, so results cannot surprise you | Add two paper exercises before the build: a prediction sheet (what you expect A vs B vs C to show, and why) and a large-result design for one real tool; keep the build as the third exercise, after S04 |
| S03.06 | Four-part spec (contracts, three traces, adversarial fixture, limits) plus scanner and gateway TODOs | Parts A–D are good but have no answer key or scoring; the tooling TODOs are builds; the twelve defence questions are not tied to the exercise | Add a scoring rubric for A–D, a "red-team your own spec" step (write three attacks your spec does not stop), and tie the twelve questions to the trace in B |

Common rules for all three:

1. Write the answer with the README closed. Open it only for the self-check.
2. Every exercise ends in a file in the chapter folder (`exercises/<name>.md`), dated. Design work that stays in your head is not evidence.
3. Log misses in the quiz sheet the same day. A miss in a design exercise is the same signal as a miss in a quiz.
4. Do the out-loud step. The S03.03 quiz showed that recall, not understanding, is where points are lost.

## S03.04 exercises (file: `S03.04-MCP-Tool-Design/EXERCISES.md`)

Three exercises, already written: derive a tool set from a system you know (network operations suggested), write one full contract for the riskiest write tool, run a mini eval. Improvements over the README's one-liner: time boxes, deliverable shape, self-check lists, an injection and a race case in the failure walkthrough, and the section-11 questions out loud after exercise 2. Exercise 3 is a build; do it inside S04, not before.

## S03.05 exercises (new section to add under "Plan")

**Exercise 1: predict before you measure (45 min, paper).** For the 50-tool catalogue and the twenty questions, write a prediction table: strategy × metric, with your expected direction and a one-line reason. Include where you think B's discovery will fail and which question types C will not help. Seal it (date it, commit it). The point of the later build is to compare against this sheet, not to confirm it.

**Exercise 2: large-result design for one real tool (45 min, paper).** Take a tool from your S03.04 exercise that can return a big result (telemetry, logs, inventory). Write the four delivery patterns for it (download URL, chunked resource, projection, aggregate), the artifact envelope, and the "surprise follow-up" question the aggregate cannot answer. Self-check: the ladder order is right; truncation is always flagged; the handle carries id, hash, version; authorization is rechecked on read.

**Exercise 3: minimum viable build (after S04).** Steps 1, 2, 3 keyword arm, 5 projection arm, 6, as the README already states. Compare against the exercise-1 sheet and write the decision note from the differences.

## S03.06 exercises (additions to section 10)

**Scoring rubric for A–D** (self-grade 0–4 each; under 3 means redo that part with the README open, then redo it closed next day):

| Part | 4 means | 0 means |
|---|---|---|
| A. Contracts | Every capability names principal, resource, operation, constraints, sensitivity and destination; grant has zero mutation allowance and an expiry; host-owned vs attacker-controlled fields listed | Capabilities described as API endpoints; grant missing or derived from model text |
| B. Three traces | Each proposal has decision, reason, credential used, backend effect and audit event; the authorized-notification variant changes exactly the grant and destination | Decisions without reasons; "the model refused" counted as enforcement |
| C. Fixture | Poisoned metadata, hostile result, changed definition, unauthorized recovery all specified with fake secrets and an inert sink; each has an observable effect to assert | Attacks listed without the backend assertion that proves they failed |
| D. Limits | Names answer contamination, remote behaviour, coarse provenance, approval fatigue and at least one bypass path you could not close | "The design prevents injection" |

**Exercise E: red-team your own spec (30 min).** Write three attacks your A–D design does not stop. At least one must not be prompt injection (supply chain, output exfiltration, resource exhaustion, cached approval). For each, say which control would close it and what it would cost in false denials.

**Tie-in:** answer the twelve defence questions in section 12 using only your trace from B. If a question cannot be answered from your trace, the trace is incomplete.

The scanner and gateway TODOs stay as builds inside the S03.06 demo (completion list, group D).

## Eight sessions (hypothetical, 22–31 Oct, 2–3 h each, alongside the S04 build)

Each line: priority · expected outcome · how to confirm · why · time.

| # | Day | Task | Outcome | Confirm | Why | Time |
|---|---|---|---|---|---|---|
| 1 | Wed 22 | S03.04 exercise 1 (derive a tool set) on network operations | `exercises/04-derive.md`: 15–20 endpoints → 4–6 tools, boundary tests, a list of endpoints deliberately not exposed | Self-check list all ticked; no tool mixes read and consequential write | Core S03.04 skill; first interview story | 90 min |
| 2 | Thu 23 | S03.04 exercise 2 (full contract) + section 11 out loud | `exercises/04-contract.md` in the section-9 shape; misses logged | Five failure rows incl. injection and race; eight questions answered without notes | Turns design into something you can defend under follow-ups | 75 min |
| 3 | Fri 24 | S03.06 parts A and B | `exercises/06-spec.md` parts A–B, self-graded | Rubric ≥3 on both; the authorized-notification variant changes only grant and destination | Trust boundary is what interviewers push on | 90 min |
| 4 | Sat 25 | S03.06 parts C, D and exercise E; twelve questions from the trace | Parts C–E added; questions answered or trace fixed | Rubric ≥3; three attacks written with their closing control | Completes the chapter's exercise with evidence | 90 min |
| 5 | Mon 27 | S03.05 exercises 1 and 2 | `exercises/05-predictions.md` (sealed) and `exercises/05-large-result.md` | Prediction table complete for every strategy × metric; ladder order correct | Makes the later build falsifiable; cheap paper work | 90 min |
| 6 | Tue 28 | Redo any part scored under 3, closed book; Anki cards for all misses | Re-graded parts; cards in the deck | All rubric scores ≥3; every logged miss has a card | Retrieval, not re-reading | 60 min |
| 7 | Thu 30 | Three timed two-minute answers, recorded; one unseen variation (change the domain to payments) for exercise 1 | Recordings; `exercises/04-derive-payments.md` | Answers within time and hit the section-6 summary points; derivation done in under 45 min | Transfer test: can you do it on a domain you did not prepare | 75 min |
| 8 | Fri 31 | Commit all exercise files; update the completion list; decide S03.05 build date after S04 | Commit on main; completion list ticks | `git log` shows the exercise files; completion list group E updated | Evidence in the repo, not in a notebook | 45 min |

Total about 10 hours. If S04 slips, drop sessions 7 and 8 first, never 1–4.

## Prediction sheet template (for S03.05 exercise 1)

| Strategy | Task success | Wrong-tool rate | Failed discovery | Tokens/task | Calls/task | Latency | Why I expect this |
|---|---|---|---|---|---|---|---|
| A ordered | | | n/a | | | | |
| A random | | | n/a | | | | |
| B keyword | | | | | | | |
| B embeddings | | | | | | | |
| C code mode | | | | | | | |

Where B will fail first: ______. Where C will not help: ______. Sealed on: ______.
