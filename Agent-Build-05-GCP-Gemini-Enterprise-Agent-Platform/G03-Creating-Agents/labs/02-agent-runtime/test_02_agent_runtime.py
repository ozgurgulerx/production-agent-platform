"""Tests for lab 02. Scaffold only: every test is TODO(learner). Empty or skipped collection is not a pass."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

HERE = Path(__file__).parent


def test_agent_engine_config_declares_agent_identity():
    """.agent_engine_config.json sets identity_type AGENT_IDENTITY and no service_account (C5)."""
    cfg = json.loads((HERE / ".agent_engine_config.json").read_text())
    # TODO(learner): assert cfg["identity_type"] == "AGENT_IDENTITY" and "service_account" not in cfg
    pytest.skip("TODO(learner)")


def test_get_or_create_does_not_create_twice(monkeypatch):
    """With a fake client whose list returns a ticket-agent, deploy_sdk.find_by_display_name returns it and create is never called."""
    # TODO(learner): build a stub client with .runtimes.list() and .runtimes.create(); assert create not called
    pytest.skip("TODO(learner)")


def test_write_env_sets_agent_runtime_resource(tmp_path, monkeypatch):
    """write_env writes AGENT_RUNTIME_RESOURCE=projects/.../reasoningEngines/... into the .env it was given."""
    # TODO(learner): monkeypatch deploy_sdk.ENV_PATH to tmp_path/".env", call write_env, read it back
    pytest.skip("TODO(learner)")


@pytest.mark.integration
def test_query_returns_policy_citation():
    """Against the real AGENT_RUNTIME_RESOURCE: the goodwill-refund turn is refused and cites a policy document (C3)."""
    # TODO(learner)
    pytest.skip("TODO(learner)")
