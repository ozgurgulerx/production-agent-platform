# Security and governance capability builds

Scope: merged production checklist architecture items 15 and 24, plus security/governance aspects of items 1–3 and 7. These are learner-written build contracts; no implementation, deployed control, or assessment result is claimed. Read the [chapter](README.md) first.

## Build contract

For each row, capture configuration/code location, versions, identities, network path, synthetic input, expected and observed outcome, trace/audit reference, and cleanup/rollback. Complete positive and negative cases before marking the capability demonstrated. Keep evidence in the existing study log; never log credentials or private customer content.

| Build | Capability and implementation task | Required production evidence |
|---|---|---|
| SG01 | Threat-model the agent using OWASP LLM Top 10 (2025), STRIDE and MITRE ATLAS; cover direct/indirect injection, excessive agency, insecure outputs, tool exfiltration and poisoned indexes. | Trust-boundary diagram, attacker path, preventive/detective/recovery controls, one attack/retest and a benign regression. |
| SG02 | Apply per-call tool authorisation, allow-lists/scopes, argument validation and approval for irreversible actions; use F03 identities and F06 execution. | Wrong-user/wrong-scope denial; changed or expired approval cannot execute; one effect under replay. |
| SG03 | Review model, skill, MCP server and package supply chains; pin/review artifacts, constrain sandbox and outbound access, define a rollback/revocation path. | Versioned inventory and a changed/unapproved artifact case; verify denied outbound path in F02 rather than assuming sandboxing provides it. |
| SG04 | Build an audit/forensics path with redacted logs, retention and reader roles; use Log Analytics and evaluate appropriate Sentinel analytics/canary signals. | Query correlating request, actor, proposed tool and outcome; redaction test, denied log access, retention settings and incident investigation record. |
| SG05 | Select and assign an applicable Azure Policy with F02; inspect compliance and exemptions. | Allowed and disallowed/noncompliant resource configurations, assignment scope/effect, remediation/exception owner and review date. |
| SG06 | Assess Foundry Control Plane inventory/oversight, Defender for Cloud AI posture and Purview AI Hub/DSPM for AI options against current availability and licensing. Configure only the chosen authorised sandbox integration. | Source date, scope/permissions, observed inventory or signal, response owner, documented gaps; no dashboard-only compliance claim. |
| SG07 | Review agent access and lifecycle governance using applicable Entra access reviews and Agent 365 integration; link F03 identities and F11 publishing. | Identity owner, entitlement/revocation path, review outcome and blocked-after-revocation observation where supported. |
| SG08 | Review Power Platform DLP boundary for a Copilot Studio integration with F11. | Connector/data-flow classification, allowed and denied integration scenarios, policy owner and rollback. |
| SG09 | Assemble A11 release and incident governance using F14 safety evidence and F08 release gates. | Threat model, model risk record, exceptions, accountable sign-off, release manifest, containment/recovery exercise and residual risk. |

Identity protocols, OBO, PKCE, audiences/scopes, PIM and Conditional Access belong to [F03](../F03-Identity-and-Zero-Trust/README.md). Private endpoints, DNS, NSG/ASG, firewall, CMK and resource deployment belong to [F02](../F02-Landing-Zones-and-Networking/README.md); APIM/WAF enforcement must identify the actual owner and service boundary. Two-user data-plane access belongs to F03/F07; F10 consumes the evidence rather than duplicating implementations.

Foundry routines, workflows and autopilots are agent runtime capabilities in F05, even when listed under a security heading in the source checklist. Safety controls and regulatory applicability research belong to [F14](../F14-Responsible-AI-and-Safety/capability-builds.md).

## Assigned source checklist items

These exact source items remain planned until the build evidence above is recorded. IDs match the shared coverage matrix.

- [ ] **CB035** — Data handling: no training on customer data, abuse monitoring and the opt-out process, logging retention — the DPO question.
- [ ] **CB146** — OWASP LLM Top 10 (2025), MITRE ATLAS, prompt injection (direct, indirect via retrieved content and tool results), tool-based exfiltration, excessive agency, insecure output handling, supply chain (models, skills, MCP servers), data poisoning of indexes; controls: input/output filters, tool allow-lists and scopes, egress control, sandboxing of code execution, human approval for irreversible actions, canary tokens, rate limits, logging for forensics; red-teaming with PyRIT; Defender for AI / Defender for Cloud AI workload protection; Sentinel analytics for AI.
- [ ] **CB147** — Azure Policy for AI, Purview AI Hub / DSPM for AI, Defender for Cloud AI posture, audit logging to Log Analytics with retention, Entra access reviews for agent identities, Power Platform DLP for Copilot Studio.
- [ ] **CB156** — Application/non-MCP tool safety controls where filters do not apply.
- [ ] **CB157** — Applicable Azure Policy assignments + compliance/enforcement.
- [ ] **CB181** — Defender for Cloud + Purview for data governance.
