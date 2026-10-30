# Microsoft Foundry learning path

Design, build and defend a support-ticket agent and its regulated-client variant. Existing labs and notes are retained; new documentation adds architecture, identity, governance and platform-boundary depth. **All proficiency scores are unassessed. Existing code is not newly runtime-verified.**

## Module map and targets

| Module | Architecture target | Code target | Current score |
|---|---|---|---|
| [F01 — Architecture and WAF](F01-Reference-Architecture-and-WAF/README.md) | 3 | — | Unassessed |
| [F02 — Landing zones and networking](F02-Landing-Zones-and-Networking/README.md) | 3 | F2 | Unassessed |
| [F03 — Identity and Zero Trust](F03-Identity-and-Zero-Trust/README.md) | 3 | F3 | Unassessed |
| [F04 — SDKs and deployment](F04-Foundry-SDKs-and-Deployment/README.md) | 3 | F3 core / F2 supporting | Unassessed |
| [F05 — Creating agents and hosting](F05-Creating-Agents/README.md) | 3 | F3 core | Unassessed |
| [F06 — Tooling and durable integration](F06-Agent-Tooling-MCP-and-Integration/README.md) | 3 | F2 / selected F3 | Unassessed |
| [F07 — Retrieval and document ingestion](F07-RAG-on-AI-Search/README.md) | 3 | F3 Search / F2 ingestion | Unassessed |
| [F08 — Evaluation, tracing and release](F08-Evals-Tracing-and-Release/README.md) | 3 | F3 | Unassessed |
| [F09 — Gateway controls and routing](F09-APIM-AI-Gateway/README.md) | 2–3 | F2 | Unassessed |
| [F10 — Security and governance](F10-Security-and-Governance/README.md) | 3 | F2 | Unassessed |
| [F11 — Copilot and M365 integration](F11-Copilot-Studio-and-M365-Boundary/README.md) | 3 | F2 integration | Unassessed |
| [F12 — Fine-tuning and routing decisions](F12-Fine-Tuning-and-Model-Routing/README.md) | 2 | Optional | Unassessed |
| [F13 — Local runtime awareness](F13-Foundry-Local/README.md) | 1–2 | F1 / optional F2 | Unassessed |
| [F14 — Responsible AI and safety](F14-Responsible-AI-and-Safety/README.md) | 3 | F2 | Unassessed |

## Study order

Start F01 with a first-pass design; learn F02/F03 foundations, then F04/F05 execution. Build retrieval in F07 and tool integration in F06, then use F08/F09 to measure and control the workload. Apply F10 security/governance and F14 responsible-AI decisions from the first design; complete their shared A11 evidence pack after evaluation. F03 keeps identity and token flows, F02 keeps network/resource-policy implementation, and F08 executes evaluations. Demonstrate F11's integration boundary. Revisit F01 with measured results. F12/F13 are optional depth; their existing labs remain available.

Architecture scale: 0 cannot explain; 1 describe; 2 whiteboard and defend; 3 built with real measurements; 4 teach with reliable sources. Code scale: F0 never used; F1 read; F2 write with documentation; F3 write unaided under time constraints; F4 review production gaps. Record assistance and evidence; do not infer proficiency from file presence.

## Working material

- [Setup](labs-setup/README.md) and existing [.env.example](.env.example).
- [Curriculum mapping and depth contracts](reference/curriculum-mapping.md).
- [Full production build checklist](reference/production-build-checklist.md) and [all-item module coverage](reference/production-build-coverage.md).
- [Production capability build inventory](reference/production-capability-builds.md).
- [Requirements provenance](reference/requirements-map.md) and [SDK compatibility](reference/sdk-compatibility.md).
- [Original reading map](reference/reading-map-foundry-agents-2026-10-25.md).
- [Study log format](study-log/README.md).

A3 means the reference build and measured walkthrough; A11 the safety/governance evidence pack; A12 the architecture/handover pack. Targets and worked examples are not measurements. Learners write functions and tests; exercises describe contracts without supplying hidden solutions.

## Preservation and verification

The nine existing modules were moved intact to the names above and extended through documentation. Historical material remains available, including dated API/status claims; consult dated official references before executing it. No dependencies were upgraded and no lab functionality is claimed by this structural update. Moved virtual environments may retain old absolute paths; see the compatibility note before use. Shared setup remains historical structure, not permission for new cross-stage imports.

[Migration verification and limitations](reference/migration-verification.md).
