# Production capability build inventory

For exhaustive source coverage, use the [229-item module matrix](production-build-coverage.md) and [preserved checklist](production-build-checklist.md). This page is the shorter static artifact/gap view.

Static review: 30 October 2026. This inventory connects the merged production checklist to existing module material. **Code present does not mean runtime-verified, deployed, or mastered.** No lab was executed for this review. Read the relevant module before starting; the learner writes implementations and tests.

## Evidence required to close a capability

Record the capability and module, exact agent/model/dataset/configuration versions, interpreter and dependency lock, reproducible command, positive and negative cases, observed result, trace/test reference, measured latency/cost where relevant, assistance used, and remaining limitation. Keep targets distinct from measurements. A README exercise without implementation is **instruction only—functionality unverified**; an empty scaffold is **scaffold only—functionality unverified**. Existing script presence is **code present—runtime unverified**.

| Capability and owner | Existing starting point | Static evidence and next learner build |
|---|---|---|
| Reproducible private infrastructure — F02/F04 | [Landing-zone chapter](../F02-Landing-Zones-and-Networking/README.md), [model Bicep](../labs-setup/01-models/deployments.bicep) | Model provisioning code targets an existing account. Build a scoped account/project and dependency stack with identity, private DNS/endpoints, policy, deny-path checks and teardown. The complete private stack is not established by this model template. |
| Identity and access — F03 | [Identity exercises](../F03-Identity-and-Zero-Trust/README.md) | Instruction and design contracts. Demonstrate developer/runtime identity differences, wrong audience, insufficient role, missing consent and two-user data access. |
| Prompt and hosted agents — F05 | [Agent creation labs](../F05-Creating-Agents/labs/01-seven-ways/README.md), [hosting labs](../F05-Creating-Agents/labs/02-hosted-agents/README.md) | Code present. Record one prompt and one hosted version performing the same task. Harden the self-hosted variant separately: denied anonymous access, controlled network paths, readiness, runtime identity and persistent state. |
| Durable tool execution — F06 | [Tooling chapter](../F06-Agent-Tooling-MCP-and-Integration/README.md), [MCP lab](../F06-Agent-Tooling-MCP-and-Integration/labs/02-mcp-tool/README.md), [toolbox lab](../F06-Agent-Tooling-MCP-and-Integration/labs/03-toolbox/README.md) | MCP/toolbox code exists; durable business-action scenarios remain instructions. Implement one queue/approval/idempotency path and prove one side effect under replay, crash recovery, expired approval and poison-message handling. |
| Permission-aware retrieval — F07 | [Retrieval chapter](../F07-RAG-on-AI-Search/README.md), [knowledge-base lab](../F07-RAG-on-AI-Search/labs/01-knowledge-base/README.md) | Knowledge-base code exists. Build PDF/layout ingestion with page citations, vector/hybrid/semantic comparisons, ACL denial and revocation, deletion/freshness, and index switch/rollback. These are not demonstrated by uploading the existing small Markdown sample. |
| Evaluations and release gate — F08 | [Evaluation scripts](../F08-Evals-Tracing-and-Release/labs/02-evals/README.md) | Code and configuration exist. Distinguish similarity from groundedness; bind dataset/agent versions; bound polling; fail the release on errors or missed thresholds. Capture a deliberately bad version blocking promotion and a measured rollback. |
| Gateway enforcement — F09 | [Gateway chapter](../F09-APIM-AI-Gateway/README.md) | Policy and failure contracts are instructional. Write policies/load probes for token limits, identity, backend fallback, cache isolation and redacted metrics; prove denied JWT access and expected throttling. |
| Security and governance — F10 | [Security/governance chapter](../F10-Security-and-Governance/README.md) | Instructional ownership for threat models, tool authorization, supply-chain review, audit and policy evidence. Reuse F02/F03/F06/F09 implementations rather than duplicate them. |
| Responsible AI and safety — F14 | [Responsible-AI chapter](../F14-Responsible-AI-and-Safety/README.md) | Own harm taxonomy, safety control decisions, oversight, system card and impact assessment. Execute bounded safety/red-team evaluations in F08 and action approval mechanics in F06; document remediation and residual risk. |
| Fine-tuning and local runtime — F12/F13 | [SFT lab](../F12-Fine-Tuning-and-Model-Routing/labs/01-sft-ticket-tone/README.md), [local agent lab](../F13-Foundry-Local/labs/01-local-ticket-agent/README.md) | Code present, runtime unverified. Preserve these as depth options; compare to a measured baseline before claiming improvement. |

## Build order and boundaries

1. Define the F01 request path and numerical targets; decide the current Terraform/Bicep build depth explicitly. The source checklist prioritizes Terraform while the historical synthesis limits it to awareness; neither source is silently discarded.
2. Establish F02/F03 infrastructure and access evidence, then F04/F05 execution and environment reproducibility.
3. Add F07 permission-aware retrieval and F06 safe durable tools.
4. Measure and gate through F08/F09. Apply F10/F14 controls throughout, and collect their shared A11 evidence after testing.

Use per-lab dependencies and lockfiles when implementing a lab; do not assume the root `.venv` or a moved environment matches its API surface. Keep the Projects SDK / Agent Framework compatibility distinction in [SDK compatibility](sdk-compatibility.md). No dependency changes are made by this inventory.

Before execution, review historical samples for broad exception suppression, public-ingress assumptions, in-memory state and unbounded polling. Those are build-review tasks, not proof that a deployed service is insecure. Keep all cloud mutations scoped to the exercise requested by the user.
