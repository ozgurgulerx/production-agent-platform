# 05 — Grounding with the Agent Search tool, under the one-built-in-tool rule

`ticket-agent` cites policy documents. The documents live in an Agent Search data store (ex-Vertex AI Search, API Discovery Engine, H9), and ADK reaches it through `VertexAiSearchTool(data_store_id=...)` (B9). The rule that shapes the code (D4): a built-in tool cannot sit beside function tools in one agent, and cannot sit in a sub-agent except Google Search and Agent Search with `bypass_multi_tools_limit=True`. The workaround is one built-in tool per agent, wrapped in `AgentTool` (D1, D4). So the policy search gets its own small `policy_agent`, and `ticket-agent` keeps its ticket tools and calls `policy_agent` like any other tool.

| Knowledge need                       | Product                                                                                  | Map     |
| ------------------------------------ | ---------------------------------------------------------------------------------------- | ------- |
| managed search over your policy PDFs | Agent Search data store                                                                  | H9, H13 |
| DIY chunk, embed, retrieve           | RAG Engine (G08)                                                                         | H11     |
| public web                           | `google_search`; must render `renderedContent` in production                             | B8      |
| outside ADK                          | google-genai `Tool(retrieval=Retrieval(vertex_ai_search=VertexAISearch(datastore=...)))` | H12     |

## Prerequisites

`AGENT_SEARCH_DATASTORE` in `.env` in the form `projects/P/locations/global/collections/default_collection/dataStores/ID` (B9). Creating the data store from `POLICY_DOCS_BUCKET` is G08 lab 01; if you have not done it, create one in the console from a Cloud Storage source (H9) and paste its resource name. `roles/discoveryengine.admin` from `labs-setup/00-setup`.

## Files

```
05-grounding-agent-search/
├── agent.py                 policy_agent (Agent Search tool only) wrapped in AgentTool inside ticket_agent
├── ask.py                   one question that needs a policy citation; prints the answer and grounding metadata
├── requirements.txt
└── test_05_grounding_agent_search.py
```

## Run

```bash
source ../../../labs-setup/.venv/bin/activate
cd 05-grounding-agent-search
python ask.py "Is a £80 goodwill refund allowed for a duplicate-charge complaint? Cite the policy."
adk web --port 8000      # Events tab: ticket_agent calls policy_agent, which calls the Agent Search tool
```

To deploy this variant, copy it over `ticket_agent/` in lab 02 and redeploy with `--agent_engine_id` (B6); the deployed Agent Identity then needs read access to the data store (C5 default roles do not include Discovery Engine; grant explicitly, role name unverified here).

## Expected output

- `ask.py` prints an answer that names a policy document and section, plus the grounding metadata the tool returned (field names unverified; print the raw event).
- The negative control, `python ask.py --no-policy-agent "..."`, answers without a citation or says it cannot cite one.

## What to notice

- Putting `VertexAiSearchTool` directly into `ticket_agent.tools` beside `get_ticket` is the D4 failure: the deploy succeeds and the first call fails. The test for this lab asserts the shape, not the model output.
- Per-user filtering is an override of `_build_vertex_ai_search_config` on the tool (B9); the shape is in `agent.py` as a TODO.
- This is the same agent shape G08 keeps when the knowledge base moves to a RAG Engine corpus (H11, H13).

## Proof (checklist)

- [ ] `ask.py` prints a citation naming a policy document from the data store
- [ ] `--no-policy-agent` prints no such citation (negative control)
- [ ] `adk web` Events tab shows `ticket_agent → policy_agent → Agent Search tool`
- [ ] `test_05_grounding_agent_search.py::test_built_in_tool_is_alone_in_policy_agent` is written and passes
- [ ] `pytest test_05_grounding_agent_search.py` runs the tests you wrote

## Cleanup

Nothing created here. The data store belongs to G08.

## Next

[`../../../G04-Agent-Tooling-Identity-MCP-A2A/labs/`](../../../G04-Agent-Tooling-Identity-MCP-A2A/labs/): the ticket tools become an MCP Toolbox server, and `ticket-agent` gets its SPIFFE identity checked.
