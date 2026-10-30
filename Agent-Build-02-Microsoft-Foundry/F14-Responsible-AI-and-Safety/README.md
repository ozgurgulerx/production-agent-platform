# F14 — Responsible AI and safety

Study status: **unassessed**. Architecture target: 3 for item 7; code target: F2 for C9 and one bounded C24 exercise. This module separates responsible-use and safety work from [F10 Security and Governance](../F10-Security-and-Governance/README.md). It preserves the safety teaching and exercises from the former combined F10 chapter; no runtime assurance is implied.

Prerequisites: [F03 identity](../F03-Identity-and-Zero-Trust/README.md), [F06 tool execution](../F06-Agent-Tooling-MCP-and-Integration/README.md), [F07 retrieval](../F07-RAG-on-AI-Search/README.md), and [F08 evaluation](../F08-Evals-Tracing-and-Release/README.md). F02 still owns network/resource-policy deployment. F10 owns threat models, authorisation, audit, and the final governance decision. F14 defines safety outcomes and evidence; F08 owns reusable evaluation execution.

Individual feature builds and acceptance evidence: [capability build contracts](capability-builds.md#build-contract).

## Build route and evidence

- [ ] Define the use-case harm taxonomy: affected people, harmful outputs/actions, foreseeable misuse, exclusions, severity rationale, and owners.
- [ ] Configure one supported content-safety control and test benign, harmful, and ambiguous cases; record false positives and missed harms.
- [ ] Test direct and indirect prompt injection, including malicious retrieved text and tool results, using non-effecting targets.
- [ ] Evaluate groundedness, protected-material and sensitive-content controls separately; record the supported model/input path and each control's limits.
- [ ] Define a human-review/escalation point; verify an unsafe or uncertain case reaches it and cannot execute an unapproved action.
- [ ] Run a bounded red-team and benign regression through the existing F08 execution path; record findings, remediation, retest, and residual risk.
- [ ] Produce the system card and impact assessment for A11; link the exact agent/model/tool versions, dataset, measurements, limitations, owners, and review trigger.

Treat these as individual builds. Capture configuration, test inputs, expected/observed outcome, trace reference, and a short explanation of trade-offs. No numerical threshold or successful test result is supplied here. Choose the actual control and deployment after checking current support in the local documentation and official source.

## 1. Start with the harm, then choose the control

A complaints assistant retrieves policy, drafts a response, and proposes a refund. Its intended user is an authorised case handler. The assistant must not decide eligibility outside policy, expose another customer's case, or issue payment without the required approval. This is a teaching scenario: the business owner must set actual approval limits and acceptable risk.

Separate three questions. **Quality:** is the answer useful and grounded? **Security:** can an attacker cross a trust boundary? **Responsible use:** can the workflow cause unfair or inappropriate outcomes even when nobody attacks it? A fluent answer can fail all three. A content-category filter cannot determine whether this case handler is allowed to refund this customer.

Define the action boundary first: drafting is reversible; sending a customer message or submitting payment creates an external effect. For the latter, authorisation and approval belong in the executing service, not in the model's instructions. An approval must bind the actor, action, case, amount and expiry; changed arguments require a new decision. F06 owns durable execution and idempotency.

## 2. Place safety controls deliberately

Prompt Shields analyse supplied user and document text for attack patterns. Decide which inputs reach a detector, how results affect the workflow, and how detector failure is handled. They supplement authorisation rather than replacing it. Review the current [Prompt Shields documentation](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/content-filter-prompt-shields).

For the worked scenario, an illustrative control path screens external input and retrieved content before model use, validates proposed tool arguments before execution, and checks the response before delivery. This is a design to evaluate, not a universal requirement to make one network call per chunk. Batching, latency, supported interfaces, cost, and false positives affect placement.

Choose an explicit failure policy. If an essential control is unavailable, block a consequential action and offer human handling. A low-risk draft might be held for review rather than discarded. Log a decision category and correlation ID, not raw customer records. Test streaming separately: content already displayed may not be recoverable after a later block.

Groundedness checks, harmful-content classification, PII controls and authorisation answer different questions. Record what each control cannot detect. Avoid assuming a supported feature, SDK method or default configuration applies to every model/deployment.

## 3. Run a bounded red-team exercise

Reuse the existing [evaluation labs](../F08-Evals-Tracing-and-Release/labs/README.md), including their safety material. Do not duplicate their implementation here. Use synthetic cases and a mock or non-effecting payment target; the learner writes any new test code.

1. State scope: selected agent/version, permitted tools, synthetic records, attempt budget and stop conditions.
2. Establish a benign baseline that successfully retrieves an authorised policy and proposes an allowed action.
3. Introduce direct injection, an injected document, and malicious tool-result text. Add cross-user retrieval and duplicate-action cases.
4. Record attack class, expected control, observed result, trace reference and severity rationale. A blocked output is not proof that no tool ran.
5. Remediate one finding, rerun it and the benign baseline, and report remaining gaps.

Use PyRIT for a bounded automated run after understanding the manual cases. The [PyRIT project](https://github.com/Azure/PyRIT) is the source for current interfaces. Record tool version and configuration. Do not turn one successful run into a claim of general robustness.

## 4. System card, impact assessment, and human oversight

The system card records purpose, intended users, exclusions, data/model/tool versions, known limits, escalation, and measured results. The impact assessment identifies affected people, plausible harms, data flows, alternatives, mitigations, uncertainty, and accountable owners. Keep the two artifacts linked to the [A11 governance evidence pack](../F10-Security-and-Governance/README.md#4-build-the-governance-evidence-pack), which retains the regulatory research tasks and release decision.

For the complaints assistant, compare a correct-but-inappropriate response with an incorrect response: factual grounding alone does not establish a fair or suitable outcome. Explain which decisions require an accountable human, how that person receives context, and what happens if review is unavailable. F06 implements the approval binding and durable execution; do not duplicate its orchestration here.

## 5. Completion evidence and shared execution

Produce the harm/control/evidence matrix, one attack and retest, a benign regression, the system card, impact assessment, and one residual-risk explanation. Record source versions, dataset size, conditions, assistance, and results in the study log. Architecture and code scores remain unassessed until demonstrated.

Use the existing [F08 safety/evaluation labs](../F08-Evals-Tracing-and-Release/labs/02-evals/README.md), including [red-team execution](../F08-Evals-Tracing-and-Release/labs/02-evals/05_red_team.py). Inspect their dependencies and targets before execution; code presence is not runtime verification. F10 consumes the evidence for release/incident decisions, while F08 owns the evaluation gate and result handling.

Source review: 30 October 2026. Use the [local documentation index](../../documentation/INDEX.md) and its coverage limits; recheck vendor support and relevant official obligations before implementation. This documentation split adds no lab code, cloud resources, or passing-test claims.
