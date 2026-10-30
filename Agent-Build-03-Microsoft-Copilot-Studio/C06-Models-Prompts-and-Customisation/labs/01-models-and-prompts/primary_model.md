# Switch the primary model and measure it

Portal steps on the Standard harness (K1), with the C05 test set as the judge. Nothing here is an API call because the model setting has no documented write API outside the agent definition; `pac copilot pull` / `push` (C07) is the code-first way to move it between environments.

1. **Baseline.** Monitor → Evaluation → run the C05 test set (`TESTSET_ID`) against the current model (GPT Chat Latest by default). Note the run id as `TESTRUN_BASE`.
2. **Switch.** Settings → Generative AI → Primary model → **Claude Sonnet 4.6**. If the option is greyed out, both admin switches are missing (K3): terms in the Microsoft 365 admin centre, "external models" in PPAC for this environment group (F2). Save.
3. **Run.** The same test set again. Note `TESTRUN_CANDIDATE`.
4. **Compare.** Monitor → Evaluation → version comparison (I2), or `GET .../testruns/{id}` for both ids (I3) and diff `metricsResults` per case. Look at General quality, Tool use (did `issue_refund` still get called for the refund cases?) and the refusal-aware Custom grader.
5. **Decide and record.** Keep or revert in the same settings page. Write the two run ids and the decision into the proof checklist.
6. **Retirement check.** Settings → Generative AI shows the retirement note for named GPT models; GPT Chat Latest carries none. If you kept a named model, put its retirement date in the team calendar.

What you expect to see: tone and verbosity differ; Tool use should not. If Tool use drops, the instructions rely on a model quirk and that is the finding, not the model.
