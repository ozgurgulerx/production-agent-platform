"""pytest skeleton for lab 01. The learner writes the tests; none pass by construction.

Run from this folder with the shared venv: pytest test_01_observability.py -q
"""
import pytest


@pytest.mark.skip(reason="TODO(learner): implement")
def test_tool_callback_logs_name_and_args_not_text(caplog):
    """Call agent.agent.log_tool_call with a fake tool and args; assert the log line has tool name and args and no customer text."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(learner): implement")
def test_safety_settings_are_explicit():
    """Import agent.agent.root_agent; assert generate_content_config carries a DANGEROUS_CONTENT threshold other than OFF (map F3)."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(learner): implement; needs a deployed agent and ADC")
def test_jailbreak_blocked_under_inspect_and_block():
    """jailbreak_probe.query(JAILBREAK[0]) returns a rejection once the floor setting is INSPECT_AND_BLOCK (map F2)."""
    raise NotImplementedError
