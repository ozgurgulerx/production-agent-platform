"""pytest skeletons for G04 lab 03. Learner writes the bodies; no placeholder passes (AGENTS.md).
Status: scaffold only, functionality unverified."""
import pytest


def test_tools_yaml_tools_name_a_source_and_statement():
    """Every kind: tool manifest has type, source, description, statement (map D7)."""
    # TODO(learner): yaml.safe_load_all(open("tools.yaml"))
    pytest.skip("TODO(learner)")


def test_my_open_tickets_requires_google_auth_and_binds_sub():
    """authRequired lists google-user and the customer parameter has authServices field sub (map D7)."""
    pytest.skip("TODO(learner)")


def test_schema_has_expected_columns():
    """schema.sql defines id, customer, status, amount, opened_at."""
    pytest.skip("TODO(learner)")


@pytest.mark.integration
def test_cloud_run_rejects_anonymous_and_accepts_id_token():
    """GET/POST to TICKET_MCP_URL/mcp: 401/403 without a token, 200 with an ID token for the service URL (map D8)."""
    pytest.skip("TODO(learner): needs TICKET_MCP_URL")
