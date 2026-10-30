"""pytest skeleton for lab 01. Scaffold only, functionality unverified: every test is TODO(learner).

Run:  pytest -q     (from this folder, shared venv active)
"""

import json
from pathlib import Path

import pytest

DATA = Path(__file__).parent / "data"


def _rows(name: str) -> list[dict]:
    path = DATA / name
    if not path.exists():
        pytest.skip(f"{name} not written yet; run make_dataset.py")
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_split_sizes():
    """train.jsonl has 85 rows and validation.jsonl 15 (README §3: start at 100, map G3)."""
    # TODO(learner)
    pytest.skip("TODO(learner)")


def test_row_shape_matches_map_g3():
    """Every row has contents with roles user then model, text parts, and a systemInstruction with parts."""
    # TODO(learner)
    pytest.skip("TODO(learner)")


def test_over_cap_rows_refuse():
    """Every row whose user turn asks for more than 250 GBP has a model turn that refuses and names the second approver."""
    # TODO(learner): parse the amount from the user text you generated; assert on the model text.
    pytest.skip("TODO(learner)")


def test_no_row_exceeds_example_token_limit():
    """No single row is anywhere near 131,072 tokens (map G2); a character-count upper bound is enough here."""
    # TODO(learner)
    pytest.skip("TODO(learner)")


def test_agent_module_uses_endpoint_path_when_set(monkeypatch):
    """With TUNED_ENDPOINT set, agent.root_agent.model is the projects/.../endpoints/... string (map G9)."""
    # TODO(learner): monkeypatch.setenv then importlib.reload(agent).
    pytest.skip("TODO(learner)")
