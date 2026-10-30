"""Tests for lab 01. Scaffold only: every test is TODO(learner). Empty or skipped collection is not a pass."""

from __future__ import annotations

import pytest

from ticket_agent import agent as ticket_agent


def test_root_agent_shape():
    """root_agent is named ticket_agent, has two tools, and its model id is not hard-coded (comes from .env)."""
    # TODO(learner): assert on ticket_agent.root_agent.name, len(root_agent.tools), and that MODEL == os.environ value
    pytest.skip("TODO(learner)")


def test_get_ticket_known_and_unknown():
    """get_ticket returns a dict with status for a known id and status not_found otherwise (D1 return shape)."""
    # TODO(learner)
    pytest.skip("TODO(learner)")


def test_refund_policy_outside_policy_names_document():
    """check_refund_policy for an £80 goodwill refund returns inside_policy False and a policy_doc string."""
    # TODO(learner)
    pytest.skip("TODO(learner)")


@pytest.mark.asyncio
async def test_runner_two_turns_refuses_out_of_policy_refund():
    """Runner + InMemorySessionService: turn 2 final response contains a refusal and the policy doc id (B5).

    This test calls the model and needs ADC and GOOGLE_GENAI_USE_VERTEXAI=TRUE; mark it integration if you
    want unit runs to stay offline.
    """
    # TODO(learner)
    pytest.skip("TODO(learner)")
