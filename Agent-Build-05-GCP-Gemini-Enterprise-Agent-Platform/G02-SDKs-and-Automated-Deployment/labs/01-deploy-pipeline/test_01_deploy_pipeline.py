"""Tests for lab 01. Learner writes them; none pass by design until then (AGENTS.md).

Run from this folder with the labs-setup venv active: `pytest -q`.
Status 25 Oct 2026: scaffold only, functionality unverified.
"""

import pytest


@pytest.mark.skip(reason="TODO(learner): implement")
def test_refund_policy_refuses_out_of_policy():
    """refund_policy(300, 40) returns status refused with a rule string (agent.py)."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(learner): implement")
def test_lookup_ticket_not_found_shape():
    """lookup_ticket('nope') returns {'status': 'not_found'} and nothing else (map D1)."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(learner): implement")
def test_base_config_uses_agent_identity():
    """sketches/traffic_split.base_config() has identity_type AGENT_IDENTITY and no service_account (C5)."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(learner): implement; needs ADC and a deployed resource")
def test_get_or_create_is_idempotent():
    """Two calls to get_or_create return the same resource name; list shows one ticket-agent."""
    raise NotImplementedError


@pytest.mark.skip(
    reason="TODO(learner): implement; needs a deployed resource with two revisions"
)
def test_rollback_does_not_create_revision():
    """len(list_revisions) is unchanged after rollback(); traffic moved to the previous revision (C4)."""
    raise NotImplementedError
