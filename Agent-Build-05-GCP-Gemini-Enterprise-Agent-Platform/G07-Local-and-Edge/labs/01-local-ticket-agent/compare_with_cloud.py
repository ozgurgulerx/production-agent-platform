"""Run adk eval twice on the G05 lab 02 evalset: this local agent, then the G03 cloud agent. Print both.

Map E1: adk eval <AGENT_DIR> <EVALSET>[:case] --config_file_path <criteria> --print_detailed_results;
tool_trajectory_avg_score and response_match_score run without the platform, rubric criteria do not.
Run:  EVALSET=... EVAL_CONFIG=... python compare_with_cloud.py
"""

import os
import subprocess
import sys
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))

HERE = Path(__file__).parent
TRACK = HERE.parents[2]
CLOUD_AGENT = (
    TRACK / "G03-Creating-Agents" / "labs" / "01-ways-to-run" / "ticket_agent"
)  # path as G03 lab 01 names it; adjust if it differs
EVALSET = os.environ.get("EVALSET")
EVAL_CONFIG = os.environ.get("EVAL_CONFIG")


def run_eval(agent_dir: Path, label: str) -> str:
    """Run adk eval for one agent directory and return its stdout."""
    if not EVALSET:
        raise SystemExit("set EVALSET to the G05 lab 02 *.evalset.json path")
    cmd = ["adk", "eval", str(agent_dir), EVALSET, "--print_detailed_results"]
    if EVAL_CONFIG:
        cmd += ["--config_file_path", EVAL_CONFIG]
    print(f"\n=== {label}: {' '.join(cmd)}")
    out = subprocess.run(cmd, capture_output=True, text=True)
    print(out.stdout)
    if out.returncode != 0:
        print(out.stderr, file=sys.stderr)
    return out.stdout


def summarise(local_out: str, cloud_out: str) -> None:
    """Pull the per-criterion scores out of the two outputs and print them side by side."""
    # TODO(learner): parse the adk eval table format you see (it is text, not JSON) and print
    # criterion | local | cloud for tool_trajectory_avg_score and response_match_score at least.
    print("\n(summary TODO(learner): paste the two tables into the lab README for now)")


if __name__ == "__main__":
    local = run_eval(HERE, "local gemma4 via ollama")
    cloud = run_eval(CLOUD_AGENT, "cloud gemini via ADC")
    summarise(local, cloud)
