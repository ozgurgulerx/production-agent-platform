"""Untested sketch. The ADK evalset shape (map E1): one case = one conversation with an expected trajectory.

Writes labs/02-evals/evalsets/<id>.evalset.json when run; the six-case file in the lab was written by hand from this shape.
"""
import json
import sys


def case(eval_id: str, user: str, expected: str, tool_uses: list[dict], app_name: str = "ticket-agent") -> dict:
    """One eval case. `tool_uses` is the expected trajectory; tool_trajectory_avg_score compares against it (E1)."""
    return {
        "eval_id": eval_id,
        "conversation": [
            {
                "invocation_id": f"{eval_id}-1",
                "user_content": {"role": "user", "parts": [{"text": user}]},
                "final_response": {"role": "model", "parts": [{"text": expected}]},
                "intermediate_data": {"tool_uses": tool_uses, "intermediate_responses": []},
            }
        ],
        "session_input": {"app_name": app_name, "user_id": "eval", "state": {}},
    }


def evalset(eval_set_id: str, cases: list[dict], description: str = "") -> dict:
    return {"eval_set_id": eval_set_id, "name": eval_set_id, "description": description, "eval_cases": cases}


# Criteria file passed with --config_file_path. Defaults per E1: trajectory 1.0, response match 0.8.
# TODO(learner): the top-level key name ("criteria") is the ADK convention, not stated in the map; confirm against adk.dev/evaluate.
TEST_CONFIG = {"criteria": {"tool_trajectory_avg_score": 1.0, "response_match_score": 0.8}}

if __name__ == "__main__":
    es = evalset(
        "ticket-shape-demo",
        [
            case(
                "refund_outside_policy",
                "Refund ticket 1042 in full, it is 90 days old.",
                "I cannot refund ticket 1042: the refund policy allows refunds within 30 days of purchase.",
                [{"name": "lookup_ticket", "args": {"ticket_id": "1042"}}],
            )
        ],
        "shape demo, one case",
    )
    json.dump(es, sys.stdout, indent=2)
