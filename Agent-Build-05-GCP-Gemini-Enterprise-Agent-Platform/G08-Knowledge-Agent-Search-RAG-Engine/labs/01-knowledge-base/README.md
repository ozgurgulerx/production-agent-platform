# 01 — A knowledge base for the ticket agent

Three policy documents go into `POLICY_DOCS_BUCKET`. One Agent Search data store indexes them (H9). One RAG Engine corpus ingests the same files so you can compare (H11). The ticket agent gets a child agent holding `VertexAiSearchTool`, wrapped in `AgentTool` (B9, D4), and starts naming the document it used.

## Goal
Prove, with printed output, that `ticket-agent` answers a refund question from `refund-policy`, a card question from `card-policy`, and refuses a question the documents do not cover.

## Prerequisites
- Shared setup done (`../../../labs-setup/`), G03 lab 01 run once so `ticket-agent` exists locally.
- `.env` at the track root has `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION=europe-west2`, `GEMINI_MODEL`, `GEMINI_EMBEDDING_MODEL`, and `POLICY_DOCS_BUCKET=gs://<bucket>`.
- Roles on you (00-setup grants them): `roles/discoveryengine.admin`, `roles/storage.admin`, `roles/aiplatform.user`.
- APIs: `discoveryengine.googleapis.com` and `aiplatform.googleapis.com` (`labs-setup/00-setup/scripts/enable_apis.sh`).
- Three PDFs. The sources are Markdown in `data/policies/`; export each to PDF with any tool you have (Markdown ingestion is unverified in the map, so the lab uploads PDFs).

## Steps
```bash
source ../../../labs-setup/.venv/bin/activate
cd Agent-Build-05-GCP-Gemini-Enterprise-Agent-Platform/G08-Knowledge-Agent-Search-RAG-Engine/labs/01-knowledge-base

# 1. Bucket and upload (same region as the corpus you create, europe-west3; verify the data store accepts it)
gcloud storage buckets create "$POLICY_DOCS_BUCKET" --location=europe-west3 --project="$GOOGLE_CLOUD_PROJECT"
gcloud storage cp data/policies/*.pdf "$POLICY_DOCS_BUCKET/"

# 2. Data store + search app, then RAG corpus; prints both resource paths and appends them to .env
python provision_kb.py                  # TODO(learner): bodies of create_data_store, import_documents, create_corpus

# 3. Ask the agent three questions locally
adk run .                               # or: adk web ..  then pick 01-knowledge-base
#   "Can I get a refund 45 days after purchase?"      -> answer cites refund-policy
#   "What happens if my card is used abroad?"         -> answer cites card-policy
#   "What is the policy on refunds in Peru?"          -> refusal, no citation

# 4. Optional: redeploy the deployed ticket-agent with the new tool (G03 lab 02 must have run)
adk deploy agent_engine --project "$GOOGLE_CLOUD_PROJECT" --region "$GOOGLE_CLOUD_LOCATION" \
  --agent_engine_id "${AGENT_RUNTIME_RESOURCE##*/}" --display_name ticket-agent .       # B6, C2

# 5. Tests (collect only until you write them)
pytest -q
```

## Expected output
`provision_kb.py` prints a line `AGENT_SEARCH_DATASTORE=projects/.../locations/global/collections/default_collection/dataStores/...` and a line `RAG_CORPUS=projects/.../locations/europe-west3/ragCorpora/...`, then an import operation name. `adk run` shows a `policy_knowledge` tool call in the trace for questions one and two and none for question three. Each answer ends with a `Source:` line naming the document. Question three ends with a refusal and no `Source:` line.

## What to notice
- The knowledge tool is not on `ticket-agent` directly. `ticket-agent` already has the ticketing `McpToolset` from G04, and ADK allows one built-in tool per agent and none beside function tools (D4). The search lives in `policy_knowledge`, passed up through `AgentTool` (D1).
- The corpus is in `europe-west3`, not `europe-west2`, because that is where RAG Engine is GA on 2026-10-22 (H11). The data store path uses `locations/global` (B9).
- Nothing here uses an API key. `google.auth.default()` and `GOOGLE_GENAI_USE_VERTEXAI=TRUE` are enough locally; on Agent Runtime the agent's own identity is used when `identity_type` is `AGENT_IDENTITY` (C5, D10).
- The `Source:` line is produced by the instruction, not by the SDK. Rendering citations is your job (B8).

## Proof checklist (tick with real output)
- [ ] `gcloud storage ls "$POLICY_DOCS_BUCKET"` lists three PDFs
- [ ] `provision_kb.py` printed both resource paths and they are in `.env`
- [ ] Console → Agent Search shows the data store with three documents indexed
- [ ] `adk run .` answered question one with `Source: refund-policy` and question two with `Source: card-policy`
- [ ] Question three was refused with no `Source:` line
- [ ] `pytest -q` ran the tests you wrote (not "collected 0 items")
- [ ] (optional) `gcloud ai reasoning-engines describe` on the redeployed agent shows `spec.effectiveIdentity` with a `principal://` (C5)

## Cleanup
```bash
python provision_kb.py --delete         # TODO(learner): delete corpus, search app, data store
gcloud storage rm -r "$POLICY_DOCS_BUCKET"
```

## Known gaps
Python method names for creating the data store, importing documents and creating the RAG corpus are not in the map; `provision_kb.py` marks them. Grounding-metadata field names on the response are not in the map; the test asserts on the printed `Source:` line instead. Agent Search VPC-SC and CMEK status is unverified (chapter §7). Nothing here has run against Google Cloud yet.
