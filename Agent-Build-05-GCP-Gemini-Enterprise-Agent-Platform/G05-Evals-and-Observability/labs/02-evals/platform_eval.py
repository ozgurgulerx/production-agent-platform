"""Score the harness output with Agent Platform Evals adaptive rubrics (map E2) and print the judge id with every score.

Run:  python platform_eval.py --results results/ --judge gemini-4-argon
The call signature of client.evals.evaluate is not in the map; this script builds the dataset and stops at the call
until the learner confirms the signature in google-genai 2.33.0. Trajectory metrics (EvalTask) are preview (E3) and live
in ../../sketches/trajectory_metrics.py.
"""
import argparse
import json
import os
import pathlib

from dotenv import find_dotenv, load_dotenv
from google import genai

load_dotenv(find_dotenv(usecwd=True))

METRICS = ["GENERAL_QUALITY", "SAFETY", "tool_use_quality"]  # names from E2


def load_rows(results_dir: pathlib.Path) -> list[dict]:
    """Flatten results/<model>.json into rows {model, eval_id, prompt, response, tool_calls}.

    TODO(learner): the harness must store prompt and final response text per case for this to work; extend evaluate_model if it does not.
    """
    raise NotImplementedError


def evaluate(client: genai.Client, rows: list[dict], judge: str) -> list[dict]:
    """TODO(learner): client.evals.evaluate(dataset=rows, metrics=METRICS, ...) with the judge model; return scores per row.
    Signature unverified (map E2 names the method only)."""
    raise NotImplementedError


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--results", default="results/")
    p.add_argument("--judge", default=os.environ.get("EVAL_JUDGE_MODEL", "gemini-4-argon"))
    a = p.parse_args()
    client = genai.Client(vertexai=True, project=os.environ["GOOGLE_CLOUD_PROJECT"], location=os.environ["GOOGLE_CLOUD_LOCATION"])
    rows = load_rows(pathlib.Path(a.results))
    print(f"judge={a.judge} metrics={METRICS} rows={len(rows)}")
    for r in evaluate(client, rows, a.judge):
        print(json.dumps(r))
