"""Build a 100-row SFT dataset for tone and refusal phrasing from a template, in the map G3 JSONL shape.
You MUST read the output before training; it prints every row. Writes data/train.jsonl (85) and data/validation.jsonl (15).

Run:  python make_dataset.py
No model call is needed: the rows come from a template so the person who owns the policy can read and own every one.
"""

import json
import random
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data"
SYSTEM = (
    "You are the UK card team's support assistant. Warm, brief, British English, no exclamation marks. "
    "State the policy rule you applied in one clause. Never invent amounts or dates."
)

# Scenario seeds. Each produces several rows through the template below; 100 rows in total is the G3 starting point.
TICKETS = [
    "1042",
    "1043",
    "1051",
    "1077",
    "1090",
    "1104",
    "1120",
    "1133",
    "1150",
    "1162",
]
UNDER_CAP = [40.0, 85.0, 120.0, 180.0, 249.0]
OVER_CAP = [251.0, 300.0, 480.0, 999.0, 1200.0]
OTHER = [
    "lost card",
    "limit raise",
    "travel notice",
    "goodwill credit",
    "escalation to a manager",
]


def refund_rows(ticket: str, amount: float) -> dict:
    """One row: a refund request and the ideal answer in the house tone.

    Above 250 GBP the answer must refuse and name the second-approver rule; at or below it, the answer confirms
    the refund went to the tool and gives the timing. The number 250 is spoken, not learned: the cap lives in
    the tool and the instruction.
    """
    # TODO(learner): write the user text and the model text for both branches; return
    # {"systemInstruction": {"parts": [{"text": SYSTEM}]},
    #  "contents": [{"role": "user", "parts": [{"text": user}]}, {"role": "model", "parts": [{"text": model}]}]}
    raise NotImplementedError


def status_rows(ticket: str) -> dict:
    """One row: a status question and an answer that states what the ticket tool returned, in the house tone."""
    # TODO(learner): same shape as refund_rows; the model turn must not invent a status it was not given.
    raise NotImplementedError


def other_rows(ticket: str, topic: str) -> dict:
    """One row for the non-refund topics (lost card, limit raise, travel notice, goodwill credit, escalation)."""
    # TODO(learner): same shape; one clause naming the rule applied.
    raise NotImplementedError


def build(seed: int = 7) -> list[dict]:
    """100 rows: 25 under-cap refunds, 25 over-cap refunds, 25 status, 25 other topics, shuffled."""
    rows = []
    # TODO(learner): combine TICKETS x UNDER_CAP (25), TICKETS x OVER_CAP (25), 25 status, 25 other into exactly 100 rows.
    random.seed(seed)
    random.shuffle(rows)
    return rows


def write_split(rows: list[dict], train_n: int = 85) -> None:
    DATA.mkdir(exist_ok=True)
    for name, part in (
        ("train.jsonl", rows[:train_n]),
        ("validation.jsonl", rows[train_n:]),
    ):
        with open(DATA / name, "w", encoding="utf-8") as f:
            for r in part:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"{name}: {len(part)} rows")


if __name__ == "__main__":
    rows = build()
    assert len(rows) == 100, f"expected 100 rows, got {len(rows)}"
    write_split(rows)
    for i, r in enumerate(rows, 1):
        user = r["contents"][0]["parts"][0]["text"]
        model = r["contents"][1]["parts"][0]["text"]
        print(f"\n[{i}] Q: {user}\n    A: {model}")
    print(
        "\nRead every row. Delete anything that invents a number or softens the 250 GBP rule, then run submit_sft.py."
    )
