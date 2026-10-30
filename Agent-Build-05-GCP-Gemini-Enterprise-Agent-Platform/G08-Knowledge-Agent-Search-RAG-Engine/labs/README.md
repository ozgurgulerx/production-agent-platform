# G08 labs — knowledge for the ticket agent

Setup is shared: [`../../labs-setup/`](../../labs-setup/). Assumes G03 lab 01 (`ticket-agent` runs locally) and, for the optional redeploy step, G03 lab 02 (`AGENT_RUNTIME_RESOURCE` in `.env`). Facts by map letter from [`../../reference/reading-map-gcp-agents-2026-10-25.md`](../../reference/reading-map-gcp-agents-2026-10-25.md).

```
labs/
└── 01-knowledge-base/      policies -> POLICY_DOCS_BUCKET -> data store (H9) and RAG corpus (H11) -> AgentTool on ticket-agent -> citations
    ├── README.md
    ├── agent.py            knowledge agent (VertexAiSearchTool) wrapped in AgentTool inside ticket-agent
    ├── provision_kb.py     upload, create data store, create corpus, write .env values   (TODO(learner) bodies)
    ├── test_knowledge_base.py
    ├── requirements.txt
    ├── .agent_engine_config.json
    └── data/policies/      refund-policy.md, card-policy.md, escalation-policy.md (export to PDF before upload)
```

| Lab | Chapter section | Creates | Time |
|---|---|---|---|
| 01 | §2 data stores, §3 RAG Engine, §4 tool shapes, §6 citations | a GCS bucket with three PDFs, one Agent Search data store with a search app, one RAG Engine corpus in `europe-west3`, `AGENT_SEARCH_DATASTORE` and `RAG_CORPUS` in `.env`, the two-agent `agent.py` | 60–90 min plus indexing time |

Run order: G03 lab 01 → this lab → (optional) redeploy with `adk deploy agent_engine --agent_engine_id` → G05 lab 02 to add a citation case to the eval set.

Contrast lab: G03 `labs/05-grounding` (grounding tool only, no corpus, no AgentTool).

Next chapter: [`../../G09-Apigee-Integrated-Designs/`](../../G09-Apigee-Integrated-Designs/) (designs only, no labs).

Status on 25 Oct 2026: scaffold only, functionality unverified.
