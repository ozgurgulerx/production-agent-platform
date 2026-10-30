"""Upload data/*.jsonl to GCS, start a supervised tuning job on gemini-3.5-flash-lite on the eu endpoint, poll, print the endpoint.

Run:  python submit_sft.py
Map G4: google-genai with api_version="v1beta1"; client.tunings.tune(base_model, training_dataset, config=CreateTuningJobConfig(...));
hyperparameters epochCount, adapterSize, learningRateMultiplier; result tuning_job.tuned_model.endpoint.
Map G2: Gemini 3.5 tunes and serves on us/eu only, so the location here is eu, not GOOGLE_CLOUD_LOCATION.
"""

import os
import subprocess
import time
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from google import genai
from google.genai import types

load_dotenv(find_dotenv(usecwd=True))  # .env at the track root (walks up)

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = os.environ.get("TUNING_LOCATION", "eu")  # map G2
BASE = os.environ.get("GEMINI_LITE_MODEL", "gemini-3.5-flash-lite")  # map G1 SFT base
BUCKET = os.environ.get("TUNING_BUCKET") or os.environ["AGENT_RUNTIME_STAGING_BUCKET"]
DATA = Path(__file__).parent / "data"
PREFIX = f"{BUCKET.rstrip('/')}/g06-sft"


def upload(name: str) -> str:
    """gcloud storage cp data/<name> to the bucket; returns the gs:// URI."""
    uri = f"{PREFIX}/{name}"
    subprocess.run(["gcloud", "storage", "cp", str(DATA / name), uri], check=True)
    print("uploaded", uri)
    return uri


def start_job(client: genai.Client, train_uri: str, validation_uri: str):
    """Start the SFT job. Returns the tuning job object."""
    # TODO(learner): confirm the keyword spellings against google-genai 2.33.0 (map G4 gives the REST names
    # epochCount, adapterSize, learningRateMultiplier; the Python names and the adapter-size enum are unverified).
    config = types.CreateTuningJobConfig(
        tuned_model_display_name="ticket-tone",
        validation_dataset=types.TuningValidationDataset(gcs_uri=validation_uri),
        # epoch_count=3, adapter_size=..., learning_rate_multiplier=1.0,   # start with the defaults; see README §4
    )
    return client.tunings.tune(
        base_model=BASE,
        training_dataset=types.TuningDataset(gcs_uri=train_uri),
        config=config,
    )


def wait(client: genai.Client, job):
    """Poll until the job leaves the running states. Returns the final job object."""
    # TODO(learner): the get-by-name call for tuning jobs in google-genai 2.33.0 is not in the map; confirm it
    # (expected shape: client.tunings.get(name=job.name)) and the terminal state names, then loop with a 60 s sleep.
    raise NotImplementedError


if __name__ == "__main__":
    train_uri = upload("train.jsonl")
    validation_uri = upload("validation.jsonl")
    client = genai.Client(
        vertexai=True,
        project=PROJECT,
        location=LOCATION,
        http_options={"api_version": "v1beta1"},
    )
    job = start_job(client, train_uri, validation_uri)
    print("job", job.name, getattr(job, "state", None))
    job = wait(client, job)
    print("state:", job.state)
    print(
        "tuned endpoint:", job.tuned_model.endpoint
    )  # map G4: use this as the model string in agent.py (G9)
    print(
        "Next: export TUNED_ENDPOINT=<that path>, then adk eval base and tuned on the G05 evalset."
    )
