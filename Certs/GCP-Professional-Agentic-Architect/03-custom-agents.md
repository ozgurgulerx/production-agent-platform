# Section 3: Developing custom agents (~33%)

Largest section. Objectives verbatim from the exam guide PDF (Sep 2026).

## 3.1 Designing and building agentic workflows in code

- [ ] Selecting and configuring the appropriate language model (e.g., large language model [LLM] vs. small language model [SLM], self-hosted vs. software as a service [SaaS], and open-source software [OSS] vs. proprietary LLM) considering cost, security, and agent architecture
- [ ] Building custom agents using open-source libraries (e.g., Agent Development Kit [ADK])
- [ ] Configuring sessions and memory (e.g., Agent Platform Memory Bank and managed sessions)
- [ ] Configuring skills using Agents CLI (e.g., plugins and agent vs. human mode)
  - Know how to: Gemini model family choice (Pro/Flash/Flash-Lite, thinking budgets), Gemma or Model Garden open models on Vertex endpoints or GKE, provisioned throughput; ADK agent types (LlmAgent, SequentialAgent, ParallelAgent, LoopAgent, custom BaseAgent), tools (function, built-in, OpenAPI, MCP toolset, agent-as-tool), callbacks, state and artifacts; Agent Runtime Sessions and Memory Bank; Agents CLI skill configuration.
  - Read: ADK docs https://google.github.io/adk-docs/ · ADK agents https://google.github.io/adk-docs/agents/ · ADK tools https://google.github.io/adk-docs/tools/ · ADK sessions, state, memory https://google.github.io/adk-docs/sessions/ · Agent Runtime Memory Bank https://cloud.google.com/agent-platform/docs/memory-bank · Agent Runtime Sessions https://cloud.google.com/agent-platform/docs/sessions · Gemini models https://cloud.google.com/vertex-ai/generative-ai/docs/models · Model Garden https://cloud.google.com/vertex-ai/generative-ai/docs/model-garden/explore-models · Provisioned Throughput https://cloud.google.com/vertex-ai/generative-ai/docs/provisioned-throughput

## 3.2 Integrating enterprise domain knowledge

- [ ] Designing, configuring, and managing retrieval-augmented generation (RAG) pipelines and vector retrieval systems (e.g., embedding models, similarity scoring, and reranking) using appropriate services such as vector databases (e.g., Vector Search and Agent Retrieval)
- [ ] Configuring agent permissions (e.g., Agent Identity)
- [ ] Using Google Cloud tools (e.g., Agent Registry, Google Cloud MCP Servers) to configure prebuilt and custom capabilities (e.g., custom integration layers for managed databases, API integrations, and MCP server that connects agents to third-party SaaS tools and remote servers)
  - Know how to: RAG Engine (corpus, import, retrieval) vs Vector Search (index, endpoint, hybrid, filtering) vs AlloyDB/Cloud SQL pgvector vs BigQuery vector search; Vertex embeddings and ranking API; Agent Identity as the agent's own principal; MCP Toolbox for Databases; Application Integration and Apigee as tool backends; Agent Registry entries.
  - Read: RAG Engine https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview · Vector Search https://cloud.google.com/vertex-ai/docs/vector-search/overview · Embeddings API https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings · Ranking API https://cloud.google.com/generative-ai-app-builder/docs/ranking · AlloyDB AI https://cloud.google.com/alloydb/docs/ai · BigQuery vector search https://cloud.google.com/bigquery/docs/vector-search-intro · MCP Toolbox for Databases https://github.com/googleapis/genai-toolbox · Agent Identity https://cloud.google.com/agent-platform/docs/agent-identity · Apigee as an MCP/tool gateway https://cloud.google.com/apigee/docs

## 3.3 Orchestrating and coordinating agentic workflows

- [ ] Orchestrating agents using agentic protocols (e.g., MCP and Agent2Agent [A2A])
- [ ] Selecting and coordinating multiagent handoffs and workflows (e.g., parallel agents, sequential agents, and graph workflow) using Google Cloud tools (e.g., Agent Identity, Agent Registry, Agent Runtime, and agent policies)
  - Know how to: ADK multi-agent hierarchy (sub_agents, transfer), SequentialAgent / ParallelAgent / LoopAgent, agent-as-tool vs handoff, A2A server and client in ADK (agent card, tasks, streaming), remote agents on Agent Runtime, agent policies in Agent Registry; LangGraph and CrewAI on Agent Runtime as alternatives.
  - Read: ADK multi-agent systems https://google.github.io/adk-docs/agents/multi-agents/ · ADK A2A https://google.github.io/adk-docs/a2a/ · A2A protocol spec https://a2a-protocol.org/latest/specification/ · Agent Runtime overview https://cloud.google.com/agent-platform/docs/agent-engine/overview · Agent Registry https://cloud.google.com/agent-platform/docs/agent-registry · Choose an agent design pattern (Architecture Center) https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system · In repo: S04.
