# Section 5: Securing and governing agentic workflows (~15%)

Objectives verbatim from the exam guide PDF (Sep 2026).

## 5.1 Configuring agent security and governance

- [ ] Implementing authentication and secure tool execution (e.g., agent-to-tool API calls using OAuth 2.0)
- [ ] Configuring principal access boundary (PAB) policies using Agent Identity
- [ ] Configuring Agent Gateway to monitor traffic and track agents
- [ ] Designing and configuring agentic governance and policy enforcement (e.g., Agent Registry and Model Armor)
  - Know how to: ADK tool auth (OAuth2, OIDC, API key, service account), Auth Manager for user-delegated OAuth; Agent Identity as a principal with its own IAM bindings; IAM principal access boundary policies to cap what the agent can reach; Agent Gateway as the egress/ingress control point with logging; Model Armor templates (prompt injection, jailbreak, sensitive data, malicious URLs) attached to Vertex endpoints or called inline; Agent Registry policies.
  - Read: ADK tool authentication https://google.github.io/adk-docs/tools/authentication/ · Agent Identity https://cloud.google.com/agent-platform/docs/agent-identity · IAM principal access boundary policies https://cloud.google.com/iam/docs/principal-access-boundary-policies · Agent Gateway https://cloud.google.com/agent-platform/docs/agent-gateway · Model Armor https://cloud.google.com/security-command-center/docs/model-armor-overview · Model Armor with Vertex AI https://cloud.google.com/security-command-center/docs/model-armor-vertex-integration · Agent Registry https://cloud.google.com/agent-platform/docs/agent-registry

## 5.2 Implementing secure agent behavior and execution

- [ ] Designing appropriate safety frameworks and guardrails (e.g., Agent Gateway, Model Armor, and human-in-the-loop [HITL])
- [ ] Configuring secure access to data and identity propagation (e.g., Agent Gateway and Agent Registry)
  - Know how to: ADK callbacks as guardrails (before_model, before_tool), Gemini safety settings, Model Armor floor settings per project/folder, HITL via tool confirmation / long-running tools / pause-and-resume in ADK, Sensitive Data Protection de-identification before the model, identity propagation (end-user credentials through Agent Gateway to data stores, VPC Service Controls perimeters, CMEK).
  - Read: ADK callbacks https://google.github.io/adk-docs/callbacks/ · ADK safety and security https://google.github.io/adk-docs/safety/ · Gemini safety settings https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-attributes · Sensitive Data Protection https://cloud.google.com/sensitive-data-protection/docs · VPC Service Controls with Vertex AI https://cloud.google.com/vertex-ai/docs/general/vpc-service-controls · Secure AI Framework (SAIF) https://saif.google/ · In repo: S03.06 Client as trust boundary.
