"""Tests for lab 05. Scaffold only: every test is TODO(learner). Empty or skipped collection is not a pass.

Set AGENT_SEARCH_DATASTORE (any well-formed value) before importing agent.py in unit tests.
"""

from __future__ import annotations

import pytest


def test_built_in_tool_is_alone_in_policy_agent(monkeypatch):
    """policy_agent.tools is exactly one VertexAiSearchTool and nothing else (D4 one-built-in-tool rule)."""
    # TODO(learner): monkeypatch.setenv("AGENT_SEARCH_DATASTORE", "projects/p/locations/global/collections/default_collection/dataStores/d");
    # import agent; assert len(agent.policy_agent.tools) == 1 and isinstance(..., VertexAiSearchTool)
    pytest.skip("TODO(learner)")


def test_root_agent_has_no_built_in_tool_directly(monkeypatch):
    """ticket_agent.tools contains function tools and an AgentTool, never a VertexAiSearchTool (D4)."""
    # TODO(learner)
    pytest.skip("TODO(learner)")


def test_datastore_id_shape(monkeypatch):
    """AGENT_SEARCH_DATASTORE matches projects/*/locations/global/collections/default_collection/dataStores/* (B9)."""
    # TODO(learner)
    pytest.skip("TODO(learner)")


@pytest.mark.integration
async def test_answer_cites_a_policy_document():
    """Against the real data store: the goodwill-refund question is answered with a document id and section."""
    # TODO(learner)
    pytest.skip("TODO(learner)")
