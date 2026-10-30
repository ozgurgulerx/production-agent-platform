"""Run one ADK evalset against N model ids and print one comparison table. Reused by G06 for tuned vs base.

Run:  EVAL_MODELS="gemini-3.5-flash,gemini-4-argon" python eval_harness.py --evalset evalsets/ticket.evalset.json --out results/
Each model: set EVAL_MODEL (agent/agent.py reads it), evaluate with AgentEvaluator (map E1), save results/<model>.json.
Columns: tool_trajectory_avg_score, response_match_score, tool_call_count_v1, inference_call_count_v1, token_usage_v1, invocation_duration_v1.
"""
import argparse
import asyncio
import json
import os
import pathlib

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))

COLUMNS = [
    "tool_trajectory_avg_score", "response_match_score",            # quality, can fail a case (E1)
    "tool_call_count_v1", "inference_call_count_v1", "token_usage_v1", "invocation_duration_v1",  # efficiency, never fail (E1)
]


async def evaluate_model(model: str, evalset: str, config: str) -> dict:
    """Return {eval_id: {column: value}} for one model.

    TODO(learner): os.environ["EVAL_MODEL"] = model; from google.adk.evaluation.agent_evaluator import AgentEvaluator
    (module path unverified; E1 names the class); call AgentEvaluator.evaluate(agent_module="agent",
    eval_dataset_file_path_or_dir=evalset) and collect per-case metrics. The import must happen after EVAL_MODEL is set.
    """
    raise NotImplementedError


def to_markdown(results: dict[str, dict]) -> str:
    """results = {model: {eval_id: {column: value}}} → one Markdown table, one row per (case, model).

    TODO(learner): header `| case | model | ` + COLUMNS; sort by case then model so the two models sit next to each other.
    """
    raise NotImplementedError


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--evalset", required=True)
    p.add_argument("--config", default="test_config.json")
    p.add_argument("--out", default="results/")
    a = p.parse_args()
    models = [m.strip() for m in os.environ.get("EVAL_MODELS", os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")).split(",") if m.strip()]
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    results = {}
    for m in models:
        results[m] = asyncio.run(evaluate_model(m, a.evalset, a.config))
        (out / (m.replace("/", "_") + ".json")).write_text(json.dumps(results[m], indent=2))
    table = to_markdown(results)
    (out / "comparison.md").write_text(table)
    print(table)
