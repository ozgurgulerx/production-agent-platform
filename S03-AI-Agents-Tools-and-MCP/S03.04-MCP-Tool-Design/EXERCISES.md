# S03.04 Exercises: MCP Tool Design

Use the [README](README.md) as the reference and write your answers in a separate file (for example `my-answers.md`), not here. Do the exercises in order. Each has a time box, a deliverable and a self-check. Exercises 1 and 2 are on paper. Exercise 3 is code and is best done after S03.03b.

Do not use the support-ticket example. Choose a system you know. A good fit for your background is **network operations**: a device inventory, configuration and telemetry API. Any system with 15 or more endpoints works.

---

## Exercise 1: Derive a tool set from scratch (60–90 min)

**Task.** Follow the derivation steps in README section 1.

1. List 15–20 raw endpoints of your system (method, path, one-line purpose).
2. Write 5 realistic tasks a user would ask an agent. Include one read-only question, one multi-step investigation, one write, one ambiguous request and one the system cannot do.
3. For each task, trace the raw call sequence an agent would need with endpoint-shaped tools. Mark every step that is fixed (always the same next call) versus a judgement the model must make.
4. Collapse the fixed runs into intent-level tools. Leave judgement steps as separate tools or as model decisions.
5. Apply the boundary tests to each proposed tool: one intent, one permission level, one failure model, reads separate from writes.
6. Decide for each tool: tool, resource or prompt (README section 1 table).

**Deliverable.** A table: raw endpoints → 4–6 proposed tools, plus a short list of endpoints you deliberately did *not* expose and why.

**Self-check.**
- [ ] No tool mixes a read and a consequential write.
- [ ] Every required argument can be obtained from the user's request or an earlier tool result (section 2, point 6).
- [ ] At least one place where you kept two tools separate because the model must make a decision between them.
- [ ] You can state, for each tool, its one permission level.
- [ ] Count: fewer tools than endpoints, but not one dispatcher tool.

---

## Exercise 2: Write one full contract (45 min)

**Task.** Take your riskiest write tool from Exercise 1 and produce the README section 9 artifacts for it.

1. Definition: name, title, description (when to use, when not to use, where arguments come from, required scope), input schema with enums and bounds, annotations.
2. Output table: every outcome, which channel carries it (result, `isError: true`, protocol or HTTP error) and its shape. Include ambiguity, policy denial, partial success and state-changed.
3. Server execution sequence, in order: authentication and scope, idempotency lookup, policy checks, confirmation, conditional write, recording, side effects, response.
4. Failure walkthrough with at least five rows, including:
   - a prompt-injection case (untrusted text asks for another action),
   - the response being lost after the action committed,
   - a race with a second authorized caller,
   - a downstream side effect failing after the main action succeeded,
   - the same operation key reused with different arguments.

**Deliverable.** One page, in the same shape as README section 9.

**Self-check.**
- [ ] The description says when *not* to use the tool and names the alternative.
- [ ] Authority comes from scopes and server policy, not from anything in a tool result.
- [ ] Every failure row names the safe next step for the caller.
- [ ] A timeout is treated as an unknown outcome, with a way to query or safely retry.
- [ ] Nothing in your design relies on annotations as a security control.

**Then, out loud, no notes (15 min).** Answer the eight questions in README section 11. Record yourself or write down the questions you stumbled on and re-read only those.

---

## Exercise 3: Mini eval (about 90 min, code)

Do this after S03.03b, or fold it into S03.05.

**Build.**
- A mock backend for your system from Exercise 1 (in-memory data is fine).
- Variant A: raw endpoint-shaped MCP tools. Variant B: the same tools with improved descriptions. Variant C: your curated set from Exercise 1.
- 10 questions with a known correct outcome. Mix: simple lookup, multi-step, ambiguous, impossible, a near-duplicate-tool trap, one write.
- Split them: 6 for development, 4 held out. Do not look at the held-out results until the descriptions are final.

**Check.** Deterministic checks only for this exercise: final backend state, no duplicate or unauthorized effects, expected tool or acceptable sequence, expected key fields in the answer.

**Run.** One model, 3 runs per question per variant. Pin the model version and record settings.

**Record**, per variant: task success (as counts, e.g. 8/10), tasks with at least one wrong tool call, invalid versus schema-valid-but-wrong arguments, calls per task, tokens per task.

**Deliverable.** A small results table and one paragraph on what the traces showed. Report honestly if the variants are close.

**Self-check.**
- [ ] You can say what A vs B tested and what B vs C tested.
- [ ] You changed only descriptions between A and B, and said so if C also changed schemas or outputs.
- [ ] Held-out cases were run once at the end.
- [ ] You looked at traces, not only final answers.
- [ ] You did not claim a general result from 10 questions.

---

## Interview rehearsal

After Exercise 2, prepare a two-minute spoken answer to: **"How would you expose our internal systems to an agent?"** It should cover, in order: intent-level tools instead of endpoint wrappers, descriptions as the interface, results and errors written for the model, authority in the server, safe retries and partial failure, and proving it with an eval. Then answer the follow-ups in README section 11 without looking.
