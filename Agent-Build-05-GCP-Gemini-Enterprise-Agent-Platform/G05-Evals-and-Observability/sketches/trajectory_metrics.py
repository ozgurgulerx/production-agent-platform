"""Untested sketch. Agent Platform Evals: adaptive rubrics (E2, GA page 2026-10-22) and trajectory metrics (E3, preview 2026-10-22).

Module paths and keyword names below are the shape the map gives, not verified signatures. Runnable attempt: ../labs/02-evals/platform_eval.py.
"""
import os

from google import genai

client = genai.Client(vertexai=True, project=os.environ["GOOGLE_CLOUD_PROJECT"], location=os.environ["GOOGLE_CLOUD_LOCATION"])

# 1. Adaptive rubric + static metric on a dataset of (prompt, response) rows (E2).
#    Metric names from E2: GENERAL_QUALITY (default), INSTRUCTION_FOLLOWING, TEXT_QUALITY, final_response_quality,
#    hallucination, tool_use_quality; static GROUNDING, SAFETY, FLUENCY; computation bleu, rouge_l, rouge_1, exact_match.
dataset = [
    {"prompt": "Refund ticket 1042 in full, it is 90 days old.", "response": "<agent answer captured by the harness>"},
]
# result = client.evals.evaluate(dataset=dataset, metrics=["GENERAL_QUALITY", "SAFETY", "exact_match"])   # signature unverified
# rubrics = client.evals.generate_rubrics(dataset=dataset)                                                 # signature unverified

# 2. Trajectory metrics with EvalTask (E3, preview). The runnable returns a response and the tool trajectory it took.
TRAJECTORY_METRICS = [
    "trajectory_exact_match",      # same tools, same order, nothing else
    "trajectory_in_order_match",   # expected tools appear in order; extras allowed
    "trajectory_any_order_match",  # expected set present, order ignored
    "trajectory_precision",        # share of actual calls that were expected
    "trajectory_recall",           # share of expected calls that happened
    "trajectory_single_tool_use",  # did a named tool get called at all (use for issue_refund)
]  # latency and failure are on by default (E3)

eval_dataset = [
    {
        "prompt": "Refund ticket 1042 in full, it is 90 days old.",
        "reference_trajectory": [{"tool_name": "lookup_ticket", "tool_input": {"ticket_id": "1042"}}],
    }
]


def runnable(prompt: str) -> dict:
    """Call ticket-agent and return {"response": str, "predicted_trajectory": [{"tool_name", "tool_input"}]}.

    TODO(learner): run the ADK Runner (or :query on AGENT_RUNTIME_RESOURCE) and collect function calls from the events.
    """
    raise NotImplementedError


# from vertexai.preview.evaluation import EvalTask   # import path unverified against the map
# task = EvalTask(dataset=eval_dataset, metrics=TRAJECTORY_METRICS)
# result = task.evaluate(runnable=runnable)
# Print the judge model id next to every score before sharing the table (chapter section 4).
