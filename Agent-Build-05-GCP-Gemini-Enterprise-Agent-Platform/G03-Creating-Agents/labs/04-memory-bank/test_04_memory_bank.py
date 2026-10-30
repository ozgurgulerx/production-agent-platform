"""Tests for lab 04. Scaffold only: every test is TODO(learner). Empty or skipped collection is not a pass."""

from __future__ import annotations

import pytest


def test_engine_id_is_last_path_segment():
    """two_sessions.ENGINE_ID equals the last segment of AGENT_RUNTIME_RESOURCE (projects/P/locations/L/reasoningEngines/ID)."""
    # TODO(learner): monkeypatch the env var, import two_sessions, assert
    pytest.skip("TODO(learner)")


@pytest.mark.asyncio
async def test_in_memory_two_sessions_do_not_share():
    """With InMemorySessionService and no memory service, session B cannot know session A's channel (B5)."""
    # TODO(learner): build a Runner with InMemorySessionService, run the two turns, assert B's answer lacks 'SMS'
    pytest.skip("TODO(learner)")


@pytest.mark.integration
async def test_memory_bank_recall_across_sessions():
    """With Memory Bank attached, session B answers SMS (A2: Memory Bank GA 2026-06-17)."""
    # TODO(learner)
    pytest.skip("TODO(learner)")
