# 01 — A managed knowledge base for the ticket agent

Three policy documents go to S3. One Managed Knowledge Base ingests them (no vector store, no embedding model, no chunking choice). The B04 gateway gets a knowledge-base target, so the ticket agent sees two more tools next to `get_ticket` and `issue_refund`, under the same JWT and the same Cedar engine. No key appears anywhere.

## Prerequisites
- Shared setup done (`../../../labs-setup/`), B04 labs 01 and 03 run once (`COGNITO_*`, `TICKET_GATEWAY_ID`, `TICKET_GATEWAY_URL`, `AGENTCORE_GATEWAY_ROLE_ARN` in `.env`), `CODE_BUCKET` set.
- Region with Managed Knowledge Bases (GA 17 Jun 2026; check the region list before you start).
- Roles, assigned once:

| Principal | Permission | On |
|---|---|---|
| you (or the pipeline) | `bedrock:CreateKnowledgeBase`, `CreateDataSource`, `StartIngestionJob`, `iam:CreateRole`/`PassRole` for the KB role | account |
| knowledge-base role (`agentcore-ticket-kb-role`, created by `provision_kb.py`) | `s3:GetObject`, `s3:ListBucket` on `CODE_BUCKET/policies/` | bucket |
| gateway role (`AGENTCORE_GATEWAY_ROLE_ARN`) | `bedrock:Retrieve`, `bedrock:AgenticRetrieveStream` | the knowledge base |
| Cognito test user | a Cedar `permit` on `TicketPolicies___Retrieve` once B09 lab 01 is in `ENFORCE` | gateway |
| you, for the variant | `bedrock:Retrieve` | the knowledge base |

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
python provision_kb.py                 # upload, managed KB, S3 source, ingestion, two direct retrieves with citations
python add_gateway_target.py           # TicketPolicies target on the B04 gateway (Retrieve, AgenticRetrieveStream)
python connect_agent.py                # three questions through the gateway; refusal for Peru
python strands_memory_store_variant.py # same KB, no gateway: Strands MemoryManager store with SigV4
python add_gateway_target.py --cleanup && python provision_kb.py --cleanup
```

## What to notice
- `provision_kb.py` passes `knowledgeBaseConfiguration.type = MANAGED` and nothing else: no `storageConfiguration`, no embedding ARN. Compare with the customer-managed shape in `../../sketches/kb_shapes.py`.
- Each `retrievalResults` item carries `location.s3Location.uri` and `score`. That is the citation. Keep one in the proof.
- The gateway target is what makes the knowledge base an agent capability. The agent's prompt says "use it and cite"; retrieval settings (reranker, number of results, retrieval instructions) are on the knowledge base and the target, so every agent on this gateway behaves the same way.
- The agent is called with the Cognito user's token. The knowledge base is not permissioned per user in this lab; `userContext.userId` on `Retrieve` is the hook for that, and the gateway's `JWT_PASSTHROUGH` mode would carry it. B04 §3 explains.
- Question three has no answer in the documents and the agent has no web tool, so a refusal is the correct output. If it answers "Lima", the system prompt or the tool filter is wrong.

## Compare with B03 and Foundry F08
Foundry's knowledge base is an Azure AI Search object reached through one MCP tool on a `RemoteTool` connection. Bedrock's Managed KB is a Bedrock object reached through a gateway connector target. The agent-side code is the same shape on both: one MCP client, two allowed tools, cite the location.

## Proof (checklist)
- [ ] `provision_kb.py` prints `ingestion: COMPLETE` with statistics, and two retrieves naming `card-policy.md` / `refund-policy.md` with scores
- [ ] `add_gateway_target.py` prints the target READY and both tool names
- [ ] `connect_agent.py` lists both tools from the gateway, answers questions one and two with a `via` line that shows an s3 uri, and refuses the Peru question
- [ ] `strands_memory_store_variant.py` answers the same two questions without the gateway
- [ ] Bedrock console shows the knowledge base as Managed; no key in any file

## Known gaps
The exact Gateway connector id and configuration keys for the knowledge-base target were not verifiable from boto3 shapes alone (marked `# verify` in `add_gateway_target.py`); the console target wizard shows them. `AgenticRetrieveStream` through the gateway was not exercised directly; the direct API shape (retrievers, `maxAgentIteration`, optional memory and guardrail) is in the sketch. Nothing here has run against AWS yet.
