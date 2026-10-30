# 01 — A knowledge base for the ticket agent

Three policy documents go into Blob. One `azureBlob` knowledge source indexes them. One knowledge base holds the retrieval rules. The ticket agent gets a single MCP tool and starts citing documents. No key appears anywhere.

## Prerequisites
- Shared setup done (`../../../labs-setup/`), F03 lab 01 run once.
- An Azure AI Search service (Basic is enough for this lab; Standard costs a few hundred dollars a month idle) and a storage account, both named in the track-root `.env`: `AZURE_SEARCH_ENDPOINT`, `AZ_STORAGE_ACCOUNT`, plus `AZ_SUBSCRIPTION_ID`, `AZ_RESOURCE_GROUP`, `FOUNDRY_ACCOUNT_NAME`, `FOUNDRY_PROJECT_NAME`.
- `pip install azure-storage-blob` into the shared venv (only this lab needs it).
- Roles, assigned once:

| Principal | Role | On |
|---|---|---|
| you (or the pipeline) | Search Service Contributor, Search Index Data Contributor | search service |
| search service managed identity | Storage Blob Data Reader | storage account |
| search service managed identity | Cognitive Services User | Foundry account |
| project managed identity | Search Index Data Reader | search service |
| you | Foundry Project Manager | project (to create the connection) |

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
python provision_kb.py      # upload, source, knowledge base, direct retrieve with activity
python connect_agent.py     # connection, agent, three questions with citations
python connect_agent.py --delete && python provision_kb.py --delete   # tear down
```

## What to notice
- `provision_kb.py` never creates an index, skillset or indexer by hand; the `azureBlob` source creates `ticket-policies-datasource/-skillset/-index/-indexer` and runs them.
- The direct `retrieve` call returns `activity`: the plan and sub-queries. That is the audit trail; keep it in the proof.
- The retrieval instructions live on the knowledge base. The agent's instructions only say "use it and cite". Change the instructions once and every agent on this knowledge base changes.
- The agent is called with the project MI; permissioned filtering would need `x-ms-query-source-authorization`, which this lab does not set, so the knowledge base answers unfiltered (the documents are not permissioned). The F08 chapter §3 explains the difference.
- Question three has no answer in the documents and the agent has no web tool, so a refusal is the correct output.

## Compare with F03 lab 05
Same documents could go behind the Azure AI Search **tool** on the agent. One index, no planning cost, GA. Pick that when there is one source and one agent; pick this when there are several sources, several agents, citations, or ACLs.

## Proof (checklist)
- [ ] `provision_kb.py` prints `indexer: success`, a retrieve answer naming `refund-policy.md`, and non-empty `activity steps`
- [ ] `connect_agent.py` shows the connection id, the agent version, two answers with `via knowledge_base_retrieve -> [...]`, and a refusal for Peru
- [ ] Search portal shows `ticket-kb` under Knowledge bases with one source; no API key was used (check the connection shows `ProjectManagedIdentity`)

## Known gaps
`azure-search-documents` SDK path (`KnowledgeBase`, `create_or_update_knowledge_base`) not shown; the preview build was not pinned into the shared venv. Hosted-agent variant through a toolbox (`FoundryToolbox` + `azd ai toolbox create`) is the upstream sample `17-foundry-iq-toolbox`; not reproduced here. Nothing here has run against Azure yet.
