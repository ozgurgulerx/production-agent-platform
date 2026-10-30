# Section 1: Building agents using low-code tools (~13%)

Objectives verbatim from the exam guide PDF (Sep 2026).

## 1.1 Configuring agentic workflows and behavior using low-code tools

- [ ] Configuring state-based workflows (pages, transition routes, and event handlers) using Gemini Enterprise tools (e.g., Gemini Enterprise Agent Designer and Customer Experience Agent Studio [CX Agent Studio])
- [ ] Creating system instructions and in-console prompt templates (e.g., few-shot and chain-of-thought) to guide agent behavior (e.g., Agent Designer and CX Agent Studio)
  - Know how to: build a no-code agent in Agent Designer (goal, instructions, tools, data stores), and a CX Agent Studio (Dialogflow CX lineage) flow with pages, intents/routes, parameters, event handlers, generators and playbooks; when to pick each.
  - Read: Gemini Enterprise docs https://cloud.google.com/gemini-enterprise/docs · Agent Designer https://cloud.google.com/gemini-enterprise/docs/agent-designer · CX Agent Studio / Conversational Agents https://cloud.google.com/dialogflow/cx/docs · Playbooks https://cloud.google.com/dialogflow/cx/docs/concept/playbook · Generators https://cloud.google.com/dialogflow/cx/docs/concept/generators

## 1.2 Connecting enterprise data to Gemini Enterprise

- [ ] Configuring agents to securely connect and query enterprise proprietary data sources (e.g., Gemini Enterprise and Agent Search)
- [ ] Ingesting and processing unstructured multimodal data (e.g., videos, audio, and images) into the agentic workflow
  - Know how to: create data stores (Cloud Storage, BigQuery, websites, third-party connectors like SharePoint, Confluence, Jira), access control with ACLs and identity-aware search, media and document parsing (layout parser, OCR), grounding a Gemini Enterprise agent on a data store.
  - Read: Agent Search (Vertex AI Search) docs https://cloud.google.com/generative-ai-app-builder/docs/introduction · Data store connectors https://cloud.google.com/generative-ai-app-builder/docs/connect-third-party-data-source · Access control for data sources https://cloud.google.com/generative-ai-app-builder/docs/data-source-access-control · Parse and chunk documents https://cloud.google.com/generative-ai-app-builder/docs/parse-chunk-documents · Media search https://cloud.google.com/generative-ai-app-builder/docs/create-data-store-media
