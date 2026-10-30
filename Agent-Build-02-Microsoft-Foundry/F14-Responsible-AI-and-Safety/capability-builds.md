# Responsible AI and safety capability builds

Scope: merged production checklist architecture item 7, C9 and C24, content-filter and trust/safety items. These are learner-written build contracts; existing evaluation code is a starting point, not completion evidence. Read the [chapter](README.md) first.

## Build contract

For each build, record the intended use, affected users, risk/control hypothesis, agent/model/tool versions, dataset and judge configuration, expected/observed outcomes, false positives/negatives, latency/cost effect, residual risk and accountable owner. Use synthetic data and non-effecting targets. F08 owns evaluation execution and CI; F06 owns durable approval/action execution; F10 owns governance decisions.

| Build | Capability and implementation task | Required production evidence |
|---|---|---|
| RA01 | Apply Microsoft Responsible AI Standard principles to the use case; define harm taxonomy, exclusions and human oversight points. | Harm/control matrix and a case that is factually correct but inappropriate for the intended user. |
| RA02 | Implement supported text/image Content Safety analysis, severity/category thresholds and blocklists; inspect `azure-ai-contentsafety` interfaces before coding. | Benign/harmful/ambiguous input cases, threshold rationale, false positives/negatives and trace decisions. |
| RA03 | Implement Prompt Shields checks for user input and retrieved/document/tool text; preserve C9's retrieved-chunk middleware exercise, then compare batching and placement. | Direct and indirect injection cases, detector-unavailable behavior, decision trace and latency/cost evidence; backend authorisation remains enforced. |
| RA04 | Compare groundedness, protected-material detection, and Language-service PII detection/redaction as separate controls. | Distinct datasets/outcomes and limitations for each; avoid treating similarity or groundedness as general safety. |
| RA05 | Configure supported model/agent content filters or guardrails at the correct scope and test streaming behavior. | Actual assignment, blocked/allowed outcomes, failure policy and evidence for what reached the user; recheck inheritance/defaults rather than copying historical claims. |
| RA06 | Implement human escalation/approval with F06; define what the reviewer sees and how uncertainty is handled. | Consequential action blocked without valid approval, changed-argument denial, expired approval test and usable human handoff. |
| RA07 | Run manual attacks and bounded PyRIT orchestration with converters/scorers; compare the applicable Foundry red-team path in F08. | Attack scope/budget, benign baseline, findings, remediation/retest and A11 red-team evidence. |
| RA08 | Build safety evaluation gates with F08, keeping content safety, task adherence and tool execution outcomes distinct. | A deliberately unsafe version fails promotion; dataset/version provenance; no averaging away unauthorised actions. |
| RA09 | Produce transparency/system card, impact assessment and DPIA outline, model risk record and approval-gate checklist. | Intended use/exclusions, measured limits, human oversight, data flows, affected people, mitigations, remaining uncertainty and owners; submit to F10 evidence review. |

## Regulatory and standards study

Preserve these original checklist topics as applicability research, not automatic legal requirements: EU AI Act use-case risk tier, GPAI versus deployer roles, Article 50 transparency, logging/record-keeping; GDPR Article 22 and DPIA triggers; FCA Consumer Duty, PRA SS1/23 and SMCR; DORA and third-party ICT resilience; NIST AI RMF Govern/Map/Measure/Manage; ISO/IEC 42001 AIMS clauses. DORA is not a blanket UK obligation: identify jurisdiction and entity before mapping any control.

For each topic, consult the current official source, record version/date, organisation role and use-case scope, and capture an applicability question for the accountable reviewer. Link the proposed technical or documentary evidence and identify gaps. No legal determination or compliance certification follows from completing this study task.

Use the existing [F08 evaluation/red-team labs](../F08-Evals-Tracing-and-Release/labs/02-evals/README.md) for execution. No duplicate runnable labs are created in this folder. The original C9 API names are study targets to verify against current installed packages, not guaranteed interfaces.

## Assigned source checklist items

These exact source items remain planned until the build evidence above is recorded. IDs match the shared coverage matrix.

- [ ] **CB034** — Content filtering: default severity levels, custom filters, prompt shields (jailbreak, indirect injection), groundedness detection, protected-material detection, asynchronous filter mode, modified-content-filter approval for regulated use.
- [ ] **CB104** — content filters
- [ ] **CB105** — Content Safety (prompt shields, groundedness, protected material)
- [ ] **CB142** — Microsoft Responsible AI Standard principles; harm taxonomy for the use case; transparency note; impact assessment template; human oversight points.
- [ ] **CB143** — Technical controls: Content Safety categories and thresholds, prompt shields, groundedness, PII detection (Language service), red-team evidence (PyRIT, Foundry red-teaming agent), eval gates.
- [ ] **CB144** — Regulatory mapping: EU AI Act risk tier for the use case, GPAI vs deployer obligations, Article 50 transparency, logging and record-keeping; UK: FCA Consumer Duty, SS1/23 model risk management, SMCR accountability, DORA for ICT third-party risk; GDPR Article 22 and DPIA triggers; NIST AI RMF functions (Govern, Map, Measure, Manage); ISO/IEC 42001 AIMS clauses.
- [ ] **CB145** — Be able to produce: system card outline, DPIA outline, model risk record, approval-gate checklist. Governance as artefact, not reading list (Boston Hale, TEKsystems ads).
- [ ] **CB148** — `ContentSafetyClient.analyze_text` / `analyze_image`, categories and severity, blocklists, Prompt Shields (`shield_prompt` for user prompts and documents — indirect injection), groundedness detection, protected material detection; where to place each in the request path; how to fail closed and log.
- [ ] **CB149** — Exercise: middleware for the agent that runs Prompt Shields on every retrieved chunk before it enters context and records the decision in the trace.
- [ ] **CB150** — PyRIT — red-teaming orchestrators against your agent, converters, scorers; produce the red-team evidence file for A11.
- [ ] **CB155** — Supported model content filters; test blocked input/output.
