# Google Cloud Certified – Professional Agentic Architect

New certification. Beta exam ran 8–30 Sep 2026; **GA exam launches mid-November 2026** (registration opens then, 200 USD; beta was 120 USD). Exam guide read from the official PDF on 25 Oct 2026. Two-part credential: you must pass both parts.

## Official links

| What | Link |
|---|---|
| Certification page | https://cloud.google.com/learn/certification/agentic-architect |
| Exam guide (PDF) | https://services.google.com/fh/files/misc/professional_agentic_architect_exam_guide_english.pdf |
| Sample questions (Google Form) | https://docs.google.com/forms/d/1fi1gqbWsNCFxm1CT9V-JNGff1lyqfU9kNWAaaQMvRi4/preview |
| FAQ (beta/GA dates, lab mechanics) | https://support.google.com/cloud-certification/answer/18080541 |
| Learning path (Google Skills, path 4525) | https://www.skills.google/paths/4525 |
| Agentic skill badges | https://www.skills.google/catalog?skill-badge%5B%5D=skill-badge&keywords=agent |
| Partner learning path | https://partner.skills.google/paths/4531 |
| Exam terms | https://cloud.google.com/certification/terms |

## Format

- **Part 1**: proctored multiple-choice (Pearson VUE, online or test centre). Beta was 3 hours and about 80 questions; GA is a **2-hour** session, English only, results in 7–10 business days. Passing score not published.
- **Part 2**: hands-on labs in Google Skills, offered only after passing Part 1, estimated under 5 hours, two months to complete after the CM Connect notification. Distinct from the learning-path labs; validates execution and coding in a live project.
- Validity 1 year (other Google professional certs are 2). No prerequisites; recommended 3+ years cloud, 1+ year building agentic solutions on Google Cloud.

## Blueprint

| # | Section | Weight | File |
|---|---|---|---|
| 1 | Building agents using low-code tools | ~13% | [01-low-code-agents.md](01-low-code-agents.md) |
| 2 | Using coding agents for application development | ~17% | [02-coding-agents.md](02-coding-agents.md) |
| 3 | Developing custom agents | ~33% | [03-custom-agents.md](03-custom-agents.md) |
| 4 | Evaluating and deploying agentic workflows | ~22% | [04-evaluating-deploying.md](04-evaluating-deploying.md) |
| 5 | Securing and governing agentic workflows | ~15% | [05-security-governance.md](05-security-governance.md) |

Plus [progress.md](progress.md).

## In-scope tools (from the guide)

Agent Development Kit (ADK) · Agent evaluation · Agent Gateway · Agent Identity · Agent Registry · Agent Retrieval and Vector Search 1.0 · Agent Runtime (formerly Agent Engine) · Agent Search (formerly Vertex AI Search) · Agentic protocols (A2A, MCP) · Agents CLI in Agent Platform · Antigravity (CLI, SDK, App) · Auth Manager (OAuth 2.0) · BigQuery · Cloud Run · Cloud SQL · Cloud Storage · Firestore · Gemini Enterprise · Gemini LLMs · Google Cloud Observability (Cloud Logging and Cloud Trace) · GKE · Memorystore for Redis · Model Armor · MCP servers · Model Garden · RAG Engine · Sensitive Data Protection · Skill Registry

Note the 2026 renames: Vertex AI Agent Engine → **Agent Runtime**, Vertex AI Search → **Agent Search**, Vertex AI Agent Builder → **Agent Platform**. Older docs and courses use the old names.

## Documentation hubs

- Agent Platform / Agent Runtime docs https://cloud.google.com/agent-platform/docs
- ADK https://google.github.io/adk-docs/ · ADK GitHub https://github.com/google/adk-python · ADK samples https://github.com/google/adk-samples
- A2A protocol https://a2a-protocol.org/latest/ · https://github.com/a2aproject/A2A
- Gemini Enterprise https://cloud.google.com/gemini-enterprise/docs
- Vertex AI / Gemini API https://cloud.google.com/vertex-ai/generative-ai/docs
- Vertex AI Vector Search https://cloud.google.com/vertex-ai/docs/vector-search/overview · RAG Engine https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview
- Gen AI evaluation service https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview
- Model Armor https://cloud.google.com/security-command-center/docs/model-armor-overview
- Antigravity https://antigravity.google/docs
- Google Cloud Architecture Center, AI and ML https://cloud.google.com/architecture/ai-ml
- Google Cloud blog, AI and ML https://cloud.google.com/blog/products/ai-machine-learning

## Community (unofficial)

- Medium: "2 days to Professional Agentic Architect Exam (Beta)" https://medium.com/google-cloud/2-days-to-professional-agentic-architect-exam-beta-ab794eb4e7cf
- Whizlabs exam guide https://www.whizlabs.com/blog/gcp-agentic-architect-exam-guide/
- CertCrush beta guide https://www.certcrush.app/blog/google-cloud-agentic-architect-exam-guide-beta-2026

## Mapping to the other tracks

ADK + Agent Runtime ≈ Agent Framework + Foundry hosted agents ≈ Strands + AgentCore Runtime. Agent Gateway/Identity/Registry ≈ Foundry toolbox/agent identity/Entra Agent Registry ≈ AgentCore Gateway/Identity. Model Armor ≈ Prompt Shields/Content Safety ≈ Bedrock Guardrails. Vendor-neutral parts live in [S03](../../Agent-Build-01-Fundamentals/S03-AI-Agents-Tools-and-MCP/) and [S04](../../Agent-Build-01-Fundamentals/S04-Agentic-Workflows-and-Harnesses/).
