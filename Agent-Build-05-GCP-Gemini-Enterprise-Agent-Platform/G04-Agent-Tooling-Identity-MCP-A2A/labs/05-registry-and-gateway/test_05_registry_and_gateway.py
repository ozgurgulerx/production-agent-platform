"""pytest skeletons for G04 lab 05. Learner writes the bodies; no placeholder passes (AGENTS.md).
Status: scaffold only, functionality unverified."""
import pytest


def test_agent_has_no_client_side_tool_filter():
    """The deny must come from the gateway (chapter §6); the toolset carries no tool_filter."""
    pytest.skip("TODO(learner)")


def test_cel_condition_names_only_the_two_read_tools():
    """Parse the condition string used in README step 3 and assert refund_ticket is absent (map F7)."""
    pytest.skip("TODO(learner)")


@pytest.mark.integration
def test_gateway_denies_refund_ticket_after_enforce():
    pytest.skip("TODO(learner): needs the gateway")
