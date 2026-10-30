# RFT on open-weight models through `bedrock-mantle` (not scripted)

Bedrock's second endpoint, `bedrock-mantle`, exposes OpenAI-compatible **Files** and **Fine-tuning** APIs for `gpt-oss-20b` and `Qwen3-32B` in `us-west-2`, with reinforcement fine-tuning and immediate inference on the result (reading map K4). The data is OpenAI chat JSONL, not the Nova conversation shape. Everything below is the documented shape, marked verify, because the lab did not run it.

```python
from openai import OpenAI                      # verify: base_url and the SigV4/bearer auth the Mantle endpoint expects
client = OpenAI(base_url=f"https://bedrock-mantle.{REGION}.amazonaws.com/v1", api_key=token)
tf = client.files.create(file=open("data/train_openai.jsonl", "rb"), purpose="fine-tune")
job = client.fine_tuning.jobs.create(model="openai.gpt-oss-20b-1:0", training_file=tf.id, suffix="ticket-tone",
                                     method={"type": "reinforcement", "reinforcement": {"grader": {...}}})   # verify grader schema
```

Price basis: USD 80 per training hour for open-weight RFT (K9). Decision rule from the chapter: use this path only when the target model must be an open-weight one you also plan to serve elsewhere; for the ticket agent, Nova 2 Lite SFT is the cheaper first experiment.
