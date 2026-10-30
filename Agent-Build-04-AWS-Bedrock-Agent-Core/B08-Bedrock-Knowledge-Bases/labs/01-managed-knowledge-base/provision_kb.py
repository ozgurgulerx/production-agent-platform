"""Documents -> managed knowledge base -> ingestion -> one direct Retrieve with citations.

Proves: a Managed Knowledge Base (type MANAGED, embeddingModelType MANAGED) needs no vector store, embedding
model or chunking decision from you; an S3 data source plus StartIngestionJob is the whole pipeline; Retrieve
returns the document location and score for every hit, which is the citation. Writes TICKET_KB_ID to .env.

Needs in .env: CODE_BUCKET, AWS_REGION, AWS_PROFILE; creates the KB role if KB_ROLE_ARN is missing.
Run:  python provision_kb.py [--cleanup]
"""
import json
import sys
import time
from pathlib import Path

from _common import account_id, agent_runtime, kb_control, need, session, write_env, REGION

KB_NAME, DS_NAME, PREFIX = "ticket-policies-kb", "ticket-policies-s3", "policies/"
HERE = Path(__file__).resolve().parent
BUCKET = need("CODE_BUCKET")


def kb_role_arn() -> str:
    """Least-privilege role the KB assumes: read the prefix, (managed path needs no embedding-model permission)."""
    iam, name = session().client("iam"), "agentcore-ticket-kb-role"
    trust = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "bedrock.amazonaws.com"},
             "Action": "sts:AssumeRole", "Condition": {"StringEquals": {"aws:SourceAccount": account_id()}}}]}
    policy = {"Version": "2012-10-17", "Statement": [
        {"Effect": "Allow", "Action": ["s3:GetObject", "s3:ListBucket"],
         "Resource": [f"arn:aws:s3:::{BUCKET}", f"arn:aws:s3:::{BUCKET}/{PREFIX}*"]}]}
    try:
        arn = iam.create_role(RoleName=name, AssumeRolePolicyDocument=json.dumps(trust))["Role"]["Arn"]
        time.sleep(10)   # IAM propagation before CreateKnowledgeBase validates the role
    except iam.exceptions.EntityAlreadyExistsException:
        arn = iam.get_role(RoleName=name)["Role"]["Arn"]
    iam.put_role_policy(RoleName=name, PolicyName="read-policies", PolicyDocument=json.dumps(policy))
    return arn


def upload() -> None:
    s3 = session().client("s3")
    for doc in sorted((HERE / "data" / "policies").glob("*.md")):
        s3.put_object(Bucket=BUCKET, Key=f"{PREFIX}{doc.name}", Body=doc.read_bytes(), ContentType="text/markdown")
        print("  uploaded", doc.name)


def create_kb(ba) -> str:
    existing = [k for k in ba.list_knowledge_bases(maxResults=100)["knowledgeBaseSummaries"] if k["name"] == KB_NAME]
    if existing:
        return existing[0]["knowledgeBaseId"]
    kb = ba.create_knowledge_base(
        name=KB_NAME, roleArn=kb_role_arn(),
        description="UK card team policies for the ticket agent (B08)",
        knowledgeBaseConfiguration={           # the managed line: AWS owns store, embeddings and reranker (J1)
            "type": "MANAGED",
            "managedKnowledgeBaseConfiguration": {"embeddingModelType": "MANAGED"},
        },
    )["knowledgeBase"]
    while (kb := ba.get_knowledge_base(knowledgeBaseId=kb["knowledgeBaseId"])["knowledgeBase"])["status"] != "ACTIVE":
        if kb["status"] == "FAILED":
            raise SystemExit(kb.get("failureReasons"))
        print("  kb:", kb["status"]); time.sleep(10)
    return kb["knowledgeBaseId"]


def create_source_and_ingest(ba, kb_id: str) -> None:
    sources = ba.list_data_sources(knowledgeBaseId=kb_id)["dataSourceSummaries"]
    ds_id = next((d["dataSourceId"] for d in sources if d["name"] == DS_NAME), None) or ba.create_data_source(
        knowledgeBaseId=kb_id, name=DS_NAME,
        dataSourceConfiguration={"type": "S3", "s3Configuration": {
            "bucketArn": f"arn:aws:s3:::{BUCKET}", "inclusionPrefixes": [PREFIX]}},
        dataDeletionPolicy="DELETE",
    )["dataSource"]["dataSourceId"]
    job = ba.start_ingestion_job(knowledgeBaseId=kb_id, dataSourceId=ds_id)["ingestionJob"]
    while (job := ba.get_ingestion_job(knowledgeBaseId=kb_id, dataSourceId=ds_id,
                                       ingestionJobId=job["ingestionJobId"])["ingestionJob"])["status"] not in ("COMPLETE", "FAILED"):
        print("  ingestion:", job["status"]); time.sleep(10)
    print("  ingestion:", job["status"], job.get("statistics"))


def retrieve(kb_id: str, query: str) -> None:
    r = agent_runtime().retrieve(
        knowledgeBaseId=kb_id, retrievalQuery={"text": query},
        retrievalConfiguration={"managedSearchConfiguration": {"numberOfResults": 3, "rerankingModelType": "MANAGED"}},
    )
    print(f"\nretrieve: {query}")
    for hit in r["retrievalResults"]:
        loc = hit.get("location", {}); where = loc.get("s3Location", {}).get("uri", json.dumps(loc)[:80])
        print(f"  {hit['score']:.3f}  {where}\n         {hit['content'].get('text', '')[:140].strip()!r}")


def cleanup(ba) -> None:
    for k in ba.list_knowledge_bases(maxResults=100)["knowledgeBaseSummaries"]:
        if k["name"] == KB_NAME:
            for d in ba.list_data_sources(knowledgeBaseId=k["knowledgeBaseId"])["dataSourceSummaries"]:
                ba.delete_data_source(knowledgeBaseId=k["knowledgeBaseId"], dataSourceId=d["dataSourceId"])
            ba.delete_knowledge_base(knowledgeBaseId=k["knowledgeBaseId"]); print("[cleanup] deleted", KB_NAME)
    s3 = session().client("s3")
    for o in s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX).get("Contents", []):
        s3.delete_object(Bucket=BUCKET, Key=o["Key"])


if __name__ == "__main__":
    ba = kb_control()
    if "--cleanup" in sys.argv:
        cleanup(ba); raise SystemExit(0)
    upload()
    kb_id = create_kb(ba)
    write_env("TICKET_KB_ID", kb_id)
    create_source_and_ingest(ba, kb_id)
    retrieve(kb_id, "Can a customer in Peru get a replacement card?")
    retrieve(kb_id, "What is the refund limit without a second approver?")
    print(f"\nconsole: https://{REGION}.console.aws.amazon.com/bedrock/home?region={REGION}#/knowledge-bases/{kb_id}")
