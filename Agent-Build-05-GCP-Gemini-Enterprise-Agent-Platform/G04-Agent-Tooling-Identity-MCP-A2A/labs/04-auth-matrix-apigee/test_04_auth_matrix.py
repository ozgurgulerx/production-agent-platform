"""pytest skeletons for G04 lab 04. Learner writes the bodies; no placeholder passes (AGENTS.md).
Status: scaffold only, functionality unverified."""
import pytest


def test_none_row_has_no_credentials():
    pytest.skip("TODO(learner)")


def test_service_account_row_uses_id_token_with_service_url_audience():
    """audience must equal the target URL, not target + '/mcp' (map D5, D8)."""
    pytest.skip("TODO(learner)")


def test_oauth2_row_scheme_is_oauth2_and_credential_type_matches():
    """AuthCredentialTypes.OAUTH2 pairs with the OAuth2 scheme (map D5)."""
    pytest.skip("TODO(learner)")


def test_consent_loop_answers_adk_request_credential():
    """Feed a fake event with function call adk_request_credential; assert a FunctionResponse with auth_response_uri is sent."""
    pytest.skip("TODO(learner)")


@pytest.mark.integration
def test_matrix_against_live_server():
    pytest.skip("TODO(learner): needs TICKET_MCP_URL")
