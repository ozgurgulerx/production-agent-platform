# CLAUDE.md — production-agent-platform

## What this is
The flagship production-evidence repo for Ozgur Guler's contract AI architect lane: a support-operations agent for regulated financial services on Azure AI Foundry. Stages S0–S10 are in README.md; only the current stage is in scope for any session.

## Division of labour (non-negotiable)
- Ozgur writes the core logic of each stage himself: the tool functions, the agent loop, the RRF merge, the guardrail checks, the eval scorer. These arrive from python-reps or are typed in the build block without AI. Do not write these for him; if asked, write the test and the signature and stop.
- Claude Code writes: scaffolding, CI, Dockerfile, pyproject, docs skeletons, test harnesses from the SPEC, integration glue, infra, and reviews. Every change lands as a PR he reads line by line.
- Commit messages carry an authorship tag: `[human]` for code written without AI, `[pair]` for code he wrote with review, `[agent]` for scaffolding/docs/tests generated and reviewed. This is what he will say in an interview, so it must be true.

## Workflow
1. Read the stage's SPEC in docs/specs/SN-*.md. Plan first; show the plan; wait for approval. If the plan adds files, tools or dependencies not in the SPEC, it is wrong.
2. Tests first, from the SPEC's test section. Run `uv run pytest -q` and show output.
3. Implement only what the failing tests need. No speculative abstractions.
4. Update README stage table status and the evidence line only with a number sourced to a run (link the run or the file).
5. Never commit; he commits. Never push to main; branches are `sN/<name>`.

## Standards
Python 3.12, uv, ruff (E, F, I, UP, B), mypy --strict, pytest with pythonpath = ["src"], pydantic v2 models at every boundary, structured logging to stderr, no print. Every PR: tests green, ruff clean, mypy clean, README touched if behaviour changed. Dockerfile builds. Secrets via Key Vault / env, never in repo.

## Platform order
Azure AI Foundry first (Azure OpenAI, AI Search, Foundry Agent Service, Entra, APIM, Key Vault, Private Link). Amazon Bedrock as comparison notes until S10. No Vertex. No Terraform beyond design-level Bicep/Terraform in infra/ until S7.

## Off limits
Inference engineering, GPU/NVIDIA, networking, trading infrastructure. If a task drifts there, say so and stop.

## Positioning and layout
- Positioning (13 Oct 2026): Azure-first agentic AI architect for regulated financial services, Bedrock second, London from March 2027. UK work eligibility is stated on the CV, not here. Keep career-story narrative out of the repo.
- Layout: `src/pap/` platform code, `tests/{unit,contract,integration,eval,security}`, `evals/`, `data/`, `infra/`, `docs/{architecture,adr,governance,evidence,reading,specs,log}`. Timed exercises live in the separate [`python-reps`](https://github.com/ozgurgulerx/python-reps) repo.
- Stage contracts live in `docs/specs/SN-*.md`. Existing prompts are collected in `docs/specs/claude-code-prompts.md`; future stage prompts belong at the bottom of their own spec under a `Claude Code` heading.
- `R1-tickets-mcp/` is superseded by `src/pap/tools/` (S1) and git-ignored; delete it by hand.

## Engineering Journal (how the journey is recorded)

The repo shows an engineer shipping a system, not a learner's diary. No `day01/day02` files. Three layers, each with one job:

1. **Git history is the real journal.** Small commits, PR descriptions that state the problem and the decision, and a tag at every stage boundary (`r0`, `r1`, ...).
2. **`docs/log/YYYY-wNN.md`: weekly notes**, one page, four fixed headings: *Shipped* (with tag), *Measured* (eval score, p95, cost per 1k, test count), *Broke and fixed*, *Decided* (links to ADRs). Failures stay in, e.g. "recall fell 0.81 to 0.64 after the chunker change, reverted, see ADR-004".
3. **`CHANGELOG.md`: Keep-a-Changelog**, one line per shipped thing, newest first. The root README holds only a stage table with tags and a Timeline link to the changelog and log folder.

Rules:
- Nothing in the log without a number, a commit or a tag behind it. Never invent figures; write "not measured" instead.
- The log is written at the Friday review from the week's tracker rows (about 20 minutes). It is never a daily task.
- Personal narrative (career story) belongs on LinkedIn or a blog, linking to a tag. Keep it out of this repo.
- When a stage ships: update the stage table, add the CHANGELOG line, tag it, and add it to the week's log.

## Conventions
- Match the surrounding code; comments only where the why is non-obvious.
- Additive changes: preserve existing functionality and tests.
- Commits: clear, imperative messages with the authorship tag above. No `Co-Authored-By` trailers; Ozgur is the sole author.
- No secrets, personal data or employer-confidential material in any file, fixture or commit.
- Writing: outcome first, plain and specific, British spelling, no hype.
