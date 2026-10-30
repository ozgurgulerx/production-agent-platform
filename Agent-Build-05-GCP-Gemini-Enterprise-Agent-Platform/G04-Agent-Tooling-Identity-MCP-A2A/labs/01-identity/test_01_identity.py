"""pytest skeletons for G04 lab 01. Learner writes the bodies; no placeholder passes (AGENTS.md).
Status: scaffold only, functionality unverified."""
import json
import os

import pytest

HERE = os.path.dirname(__file__)


def test_agent_identity_config_sets_identity_type():
    """The Agent Identity config must carry identity_type AGENT_IDENTITY (map C5)."""
    # TODO(learner): load .agent_engine_config.json and assert identity_type == "AGENT_IDENTITY"
    pytest.skip("TODO(learner)")


def test_sa_config_has_no_identity_type():
    """The comparison config must leave identity_type unset so the deploy runs as a service account (map C5)."""
    # TODO(learner)
    pytest.skip("TODO(learner)")


def test_whoami_returns_status_dict():
    """whoami must return a dict with a status key (map D1) and a principal when credentials resolve."""
    # TODO(learner): monkeypatch google.auth.default; call agent.whoami(tool_context=...)
    pytest.skip("TODO(learner)")


@pytest.mark.integration
def test_effective_identity_is_spiffe_principal():
    """Against the deployed resource: spec.effectiveIdentity starts with principal:// (map C5)."""
    # TODO(learner): gcloud ai reasoning-engines describe via subprocess, or client.runtimes.get
    pytest.skip("TODO(learner): needs a deployed agent")
