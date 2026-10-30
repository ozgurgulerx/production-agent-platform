"""pytest gate for lab 02 and for sketches/cloudbuild_eval_gate.yaml. The learner writes the tests; none pass by construction.

Run from this folder with the shared venv and .env loaded: pytest test_02_evals.py -q
"""
import json
import pathlib

import pytest

HERE = pathlib.Path(__file__).parent


@pytest.mark.skip(reason="TODO(learner): implement")
def test_evalset_has_six_cases_with_trajectories():
    """Load evalsets/ticket.evalset.json; assert 6 eval_cases and that every case has intermediate_data.tool_uses (a list)."""
    data = json.loads((HERE / "evalsets" / "ticket.evalset.json").read_text())
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(learner): implement; needs ADC, TICKET_MCP_URL and the platform for any judge criteria")
@pytest.mark.asyncio
async def test_evalset_passes_thresholds():
    """await AgentEvaluator.evaluate(agent_module="agent", eval_dataset_file_path_or_dir=str(HERE / "evalsets")) (map E1).
    It raises on a missed threshold from test_config.json; that exception is the CI gate."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(learner): implement")
def test_harness_table_has_one_row_per_case_and_model():
    """eval_harness.to_markdown on a two-model fixture returns 12 data rows."""
    raise NotImplementedError
