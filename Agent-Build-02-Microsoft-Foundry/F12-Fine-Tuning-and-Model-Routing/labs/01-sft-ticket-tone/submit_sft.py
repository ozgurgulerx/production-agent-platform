"""Upload the two JSONL files, start a supervised fine-tuning job on gpt-4.1-mini (Developer training type), wait, print the model name.

Run:  python submit_sft.py            then deploy the printed model with labs-setup/01-models (SKU DeveloperTier first)
"""
import os, time
from pathlib import Path
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))  # .env at the track root (walks up)
BASE = os.environ.get("FT_BASE_MODEL", "gpt-4.1-mini")
HERE = Path(__file__).parent / "data"
client = AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"], credential=DefaultAzureCredential()).get_openai_client()

files = {}
for name in ("train.jsonl", "validation.jsonl"):
    f = client.files.create(file=open(HERE / name, "rb"), purpose="fine-tune")
    client.files.wait_for_processing(f.id); files[name] = f.id; print("uploaded", name, f.id)

job = client.fine_tuning.jobs.create(
    model=BASE, training_file=files["train.jsonl"], validation_file=files["validation.jsonl"], suffix="ticket-tone",
    method={"type": "supervised", "supervised": {"hyperparameters": {"n_epochs": "auto", "batch_size": "auto", "learning_rate_multiplier": "auto"}}},
    extra_body={"trainingType": "Developer"},   # cheapest, pre-emptible; use "GlobalStandard" for a real run
)
print("job", job.id, job.status)
while job.status not in ("succeeded", "failed", "cancelled"):
    time.sleep(60); job = client.fine_tuning.jobs.retrieve(job.id); print(time.strftime("%H:%M"), job.status)
print("result:", job.status, "fine_tuned_model =", job.fine_tuned_model)
print("Next: deploy it (DeveloperTier, 24 h), create ticket-agent-tuned on it, run F05 lab 02 with EVAL_AGENT_NAME for base and tuned.")
