"""pytest skeleton for lab 01. Scaffold only, functionality unverified: every test is TODO(learner).

Run:  pytest -q     (from this folder, shared venv active; no Ollama needed for the first three)
"""

import pytest


def test_model_string_uses_ollama_chat_prefix():
    """agent.root_agent.model is a LiteLlm whose model string starts with ollama_chat/ (map H8)."""
    # TODO(learner): import agent; assert on agent.LOCAL_MODEL and type(agent.root_agent.model).
    pytest.skip("TODO(learner)")


def test_litellm_version_is_not_compromised():
    """Installed litellm is >= 1.84 and is neither 1.82.7 nor 1.82.8 (map H8 advisory)."""
    # TODO(learner): importlib.metadata.version("litellm").
    pytest.skip("TODO(learner)")


def test_stub_selftest_lists_both_tools():
    """python ticket_mcp_stub.py --selftest prints get_ticket and list_tickets."""
    # TODO(learner): subprocess.run([sys.executable, "ticket_mcp_stub.py", "--selftest"]) and parse the JSON.
    pytest.skip("TODO(learner)")


def test_get_ticket_unknown_id_returns_error():
    """get_ticket("9999") returns a dict with an error key and never an invented ticket."""
    # TODO(learner): call the function directly from ticket_mcp_stub once implemented.
    pytest.skip("TODO(learner)")


@pytest.mark.skipif(
    True, reason="needs Ollama with gemma4:e4b; flip when it is running"
)
def test_refund_over_cap_is_refused():
    """Running the agent on 'Refund 300 GBP on ticket 1042' yields a refusal mentioning a second approver."""
    # TODO(learner): use google.adk.runners.Runner with InMemorySessionService (map B5) and assert on the final text.
    pytest.skip("TODO(learner)")
