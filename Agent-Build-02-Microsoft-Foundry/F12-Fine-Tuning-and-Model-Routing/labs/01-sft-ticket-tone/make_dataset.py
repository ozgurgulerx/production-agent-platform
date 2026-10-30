"""Generate ~60 SFT rows for tone + policy phrasing from the F08 policy documents, using the base model.
You MUST read the output before training; it prints every row. Writes data/train.jsonl and data/validation.jsonl.

Run:  python make_dataset.py
"""
import json, os, random
from pathlib import Path
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))  # .env at the track root (walks up)
MODEL = os.environ.get("FOUNDRY_MODEL", "gpt-5-mini")
HERE = Path(__file__).parent
POLICIES = (HERE / "../../../F07-RAG-on-AI-Search/labs/01-knowledge-base/data/policies").resolve()
SYSTEM = "You are the UK card team's support assistant. Warm, brief, British English, no exclamation marks. State the policy rule you applied in one clause. Never invent amounts or dates."

client = AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"], credential=DefaultAzureCredential()).get_openai_client()
policy_text = "\n\n".join(p.read_text() for p in sorted(POLICIES.glob("*.md")))
prompt = f"""From these policies, write 60 realistic customer questions with ideal answers in this exact style: {SYSTEM}
Cover refunds under and over £250, goodwill credits, lost cards, limit raises, travel notices, and three escalation cases.
Return JSON: {{"rows":[{{"user":"...","assistant":"..."}}]}}

{policy_text}"""
resp = client.responses.create(model=MODEL, input=prompt, text={"format": {"type": "json_object"}})
rows = json.loads(resp.output_text)["rows"]
random.seed(7); random.shuffle(rows)
split = int(len(rows) * 0.85)
for name, part in (("train.jsonl", rows[:split]), ("validation.jsonl", rows[split:])):
    with open(HERE / "data" / name, "w") as f:
        for r in part:
            f.write(json.dumps({"messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": r["user"]}, {"role": "assistant", "content": r["assistant"]}]}) + "\n")
    print(f"{name}: {len(part)} rows")
for i, r in enumerate(rows, 1):
    print(f"\n[{i}] Q: {r['user']}\n    A: {r['assistant']}")
print("\nRead every row. Delete anything that invents a number or softens the £250 rule, then run submit_sft.py.")
