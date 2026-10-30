"""Generate ~60 SFT rows for tone + policy phrasing from the policy documents, using the base model via Converse.

Proves: one training line is one Converse conversation (schemaVersion bedrock-conversation-2024); the data teaches how to
*say* the refusal, never the cap. You MUST read the output before training: every row is printed. Writes data/train.jsonl
and data/valid.jsonl and uploads both to s3://$CODE_BUCKET/finetune/.
"""
import json
import random
import re
from pathlib import Path

from _common import MODEL_ID, need, session

HERE = Path(__file__).resolve().parent
POLICIES = HERE / "data" / "policies"
SYSTEM = ("You are the UK card team's support assistant. Warm, brief, British English, no exclamation marks. "
          "State the policy rule you applied in one clause. Never invent amounts or dates.")
BUCKET = need("CODE_BUCKET")


def generate(n: int = 60) -> list[dict]:
    rt = session().client("bedrock-runtime")
    policy_text = "\n\n".join(p.read_text() for p in sorted(POLICIES.glob("*.md")))
    prompt = (f"From these policies, write {n} realistic customer questions with ideal answers in this exact style: {SYSTEM}\n"
              "Cover refunds under and over £250, goodwill credits, lost cards, limit raises, travel notices, and three "
              'escalation cases. Return only JSON: {"rows":[{"user":"...","assistant":"..."}]}\n\n' + policy_text)
    r = rt.converse(modelId=MODEL_ID, messages=[{"role": "user", "content": [{"text": prompt}]}],
                    inferenceConfig={"maxTokens": 8000, "temperature": 0.7})
    text = r["output"]["message"]["content"][0]["text"]
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    return json.loads(text)["rows"]


def to_nova(row: dict) -> dict:
    return {"schemaVersion": "bedrock-conversation-2024",
            "system": [{"text": SYSTEM}],
            "messages": [{"role": "user", "content": [{"text": row["user"]}]},
                         {"role": "assistant", "content": [{"text": row["assistant"]}]}]}


def main() -> None:
    rows = generate()
    random.seed(7)
    random.shuffle(rows)
    split = int(len(rows) * 0.85)
    s3 = session().client("s3")
    for name, part in (("train.jsonl", rows[:split]), ("valid.jsonl", rows[split:])):
        path = HERE / "data" / name
        path.write_text("".join(json.dumps(to_nova(r), ensure_ascii=False) + "\n" for r in part))
        s3.upload_file(str(path), BUCKET, f"finetune/{name}")
        print(f"{name}: {len(part)} rows -> s3://{BUCKET}/finetune/{name}")
    for i, r in enumerate(rows, 1):
        print(f"\n[{i}] Q: {r['user']}\n    A: {r['assistant']}")
    print("\nRead every row. Delete anything that invents a number or softens the £250 rule, re-upload, then run submit_sft.py.")


if __name__ == "__main__":
    main()
