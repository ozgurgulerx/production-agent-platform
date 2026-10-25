# S05.01: Eval Foundations

Status: **Planned** (scope only).

What every eval in this section shares, so the later subsections do not restate it:

- **A known right answer per case.** Gold labels: acceptable tools or sequences, expected final answer, required end state. Allow equivalent valid paths rather than one exact trace.
- **Development vs held-out.** Tune on development cases; report on cases never seen during tuning. Repeats of one case are not new cases.
- **Repeats and pass^k.** Model output is nondeterministic; run each case k times and report pass^k (all k succeed) beside pass@1. One run proves little.
- **Deterministic checks first, judges last.** Valid arguments, authorized actions, final backend state, duplicate effects and required confirmations are checked by code. A model judge is used only where answer quality needs semantic assessment, with a fixed rubric calibrated against human grades on a sample, and never as a substitute for checking whether the effect happened.
- **Reporting.** Counts with percentages (17/20), per-case variation, pinned model versions, sampling and reasoning settings, execution budgets, and what was excluded from cost.
- **Three test layers, kept apart.** Protocol conformance (does the implementation speak valid MCP), system reliability (latency, auth failures, cache hit rate), agent evaluation (does the model choose and use tools correctly and safely). Passing the first says nothing about the third.

Sources to cite when written: τ-bench (end-state checks, pass^k), the S03.04 §6 eval design, the S03.05 evaluation section.

[Back to S05](../README.md)
