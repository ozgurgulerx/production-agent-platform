"""pytest skeletons for G04 lab 06. Learner writes the bodies; no placeholder passes (AGENTS.md).
Status: scaffold only, functionality unverified."""
import pytest


def test_served_card_has_triage_skill():
    """Start the to_a2a app with a test client and GET /.well-known/agent-card.json (map C7)."""
    pytest.skip("TODO(learner)")


def test_root_agent_lists_remote_workflow_as_sub_agent():
    pytest.skip("TODO(learner)")


@pytest.mark.integration
def test_delegated_turn_returns_policy_citation():
    pytest.skip("TODO(learner): needs the A2A server running")
