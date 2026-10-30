"""Create the knowledge base end to end, in REST so the shapes stay visible.

1. upload the three policy documents to a Blob container
2. PUT an azureBlob knowledge source   (auto-creates datasource, skillset, index, indexer)
3. PUT the knowledge base               (sources + model + retrieval defaults)
4. retrieve once directly, to prove it works before any agent is involved

Needs in .env: AZURE_SEARCH_ENDPOINT, AZ_STORAGE_ACCOUNT, AZ_SUBSCRIPTION_ID, AZ_RESOURCE_GROUP,
FOUNDRY_ACCOUNT_NAME, FOUNDRY_MODEL, FOUNDRY_EMBEDDING_MODEL. Entra only.
Roles: you need Search Service Contributor + Search Index Data Contributor; the search service's
managed identity needs Storage Blob Data Reader on the storage account and Cognitive Services User on the Foundry account.

Run:  python provision_kb.py [--delete]
"""
import os, sys, time
from pathlib import Path

import httpx
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))  # .env at the track root (walks up)
SEARCH = os.environ["AZURE_SEARCH_ENDPOINT"].rstrip("/")
ST = os.environ["AZ_STORAGE_ACCOUNT"]
SUB, RG = os.environ["AZ_SUBSCRIPTION_ID"], os.environ["AZ_RESOURCE_GROUP"]
ACCT = os.environ["FOUNDRY_ACCOUNT_NAME"]
CHAT = os.environ.get("FOUNDRY_MODEL", "gpt-5-mini")
EMB = os.environ.get("FOUNDRY_EMBEDDING_MODEL", "text-embedding-3-small")
API = "2026-08-01-preview"
KS, KB, CONTAINER = "ticket-policies", "ticket-kb", "policies"
AOAI = f"https://{ACCT}.openai.azure.com"

cred = DefaultAzureCredential()
def hdr():
    tok = cred.get_token("https://search.azure.com/.default").token
    return {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}
def put(path, body):
    r = httpx.put(f"{SEARCH}/{path}?api-version={API}", headers=hdr(), json=body, timeout=60)
    r.raise_for_status(); return r.json()

if "--delete" in sys.argv:
    for p in (f"knowledgebases/{KB}", f"knowledgesources/{KS}"):
        r = httpx.delete(f"{SEARCH}/{p}?api-version={API}", headers=hdr(), timeout=60); print(p, r.status_code)
    sys.exit()

# 1. documents
blob = BlobServiceClient(f"https://{ST}.blob.core.windows.net", credential=cred)
try: blob.create_container(CONTAINER)
except Exception: pass
for f in (Path(__file__).parent / "data/policies").glob("*.md"):
    blob.get_blob_client(CONTAINER, f.name).upload_blob(f.read_bytes(), overwrite=True); print("uploaded", f.name)

# 2. knowledge source (indexed, azureBlob): Search builds and runs the indexer for us
aoai = lambda dep: {"kind": "azureOpenAI", "azureOpenAIParameters": {"resourceUri": AOAI, "deploymentId": dep, "modelName": dep}}
put(f"knowledgesources/{KS}", {
    "name": KS, "kind": "azureBlob", "description": "UK card team policies: refunds, cards, escalation.",
    "azureBlobParameters": {
        "connectionString": f"ResourceId=/subscriptions/{SUB}/resourceGroups/{RG}/providers/Microsoft.Storage/storageAccounts/{ST};",
        "containerName": CONTAINER, "folderPath": "",
        "ingestionParameters": {"embeddingModel": aoai(EMB), "chatCompletionModel": aoai(CHAT), "contentExtractionMode": "minimal"},
    },
})
print("knowledge source:", KS, "(auto objects:", f"{KS}-datasource/-skillset/-index/-indexer)")

# 3. knowledge base: where retrieval behaviour lives, once, for every agent that uses it
put(f"knowledgebases/{KB}", {
    "name": KB, "description": "Ticket agent policy knowledge",
    "knowledgeSources": [{"name": KS}],
    "models": [aoai(CHAT)],
    "retrievalReasoningEffort": {"kind": "low"},
    "outputMode": "extractiveData",
    "retrievalInstructions": "Prefer refund-policy.md for refund questions, card-policy.md for card questions, escalation-policy.md when a human may be needed. Always cite the document.",
})
print("knowledge base:", KB)

# 4. wait for the indexer, then retrieve directly (no agent yet)
for _ in range(30):
    r = httpx.get(f"{SEARCH}/indexers/{KS}-indexer/status?api-version={API}", headers=hdr(), timeout=60)
    st = r.json().get("lastResult", {}).get("status") if r.status_code == 200 else None
    if st == "success": break
    time.sleep(10)
print("indexer:", st)
r = httpx.post(f"{SEARCH}/knowledgebases/{KB}/retrieve?api-version={API}", headers=hdr(), timeout=120, json={
    "messages": [{"role": "user", "content": [{"type": "text", "text": "Can an agent refund £300 on their own?"}]}],
    "includeActivity": True,
})
r.raise_for_status(); body = r.json()
print("\nretrieve ->", body["response"][0]["content"][0]["text"][:600])
print("activity steps:", [a.get("type") for a in body.get("activity", [])])
print("refs:", [x.get("sourceData", {}).get("title") or x.get("docKey") for x in body.get("references", [])][:5])
print("\nMCP endpoint for the agent:", f"{SEARCH}/knowledgebases/{KB}/mcp?api-version={API}")
