"""Tests for lab 03. Scaffold only: every test is TODO(learner). Empty or skipped collection is not a pass."""

from __future__ import annotations

import pytest

from ticket_agent_workflow import agent as wf


def test_root_agent_is_sequential_with_three_steps():
    """root_agent is a SequentialAgent named ticket_agent_workflow with sub_agents triage, lookup, reply in that order (B2)."""
    # TODO(learner): assert type, name, and [a.name for a in wf.root_agent.sub_agents]
    pytest.skip("TODO(learner)")


def test_output_keys_match_placeholders():
    """triage.output_key appears as {category} in lookup.instruction; lookup.output_key as {facts} in reply.instruction (B2)."""
    # TODO(learner)
    pytest.skip("TODO(learner)")


def test_only_lookup_has_tools():
    """triage and reply carry no tools; lookup carries get_ticket and check_refund_policy."""
    # TODO(learner)
    pytest.skip("TODO(learner)")


@pytest.mark.integration
async def test_workflow_refuses_goodwill_refund_with_citation():
    """Runner over root_agent: final reply contains a refusal and the policy_doc id; session.state has category and facts."""
    # TODO(learner)
    pytest.skip("TODO(learner)")
