"""pytest skeletons for G08 lab 01. Every test is TODO(learner); none passes by construction.
Run: pytest -q   (shared venv active). Needs .env with AGENT_SEARCH_DATASTORE after provision_kb.py.
"""
import os

import pytest

pytestmark = pytest.mark.skipif(not os.environ.get("AGENT_SEARCH_DATASTORE"), reason="run provision_kb.py first")


def test_agent_definition_has_one_built_in_tool_per_agent():
    """policy_knowledge holds exactly one tool (VertexAiSearchTool); ticket_agent holds an AgentTool, not the search tool (D4)."""
    # TODO(learner): import agent; assert on agent.policy_knowledge.tools and agent.root_agent.tools.
    raise NotImplementedError


def test_refund_question_cites_refund_policy():
    """Run the root agent with Runner + InMemorySessionService (B5); final text ends with 'Source: refund-policy'."""
    # TODO(learner)
    raise NotImplementedError


def test_card_question_cites_card_policy():
    # TODO(learner)
    raise NotImplementedError


def test_uncovered_question_is_refused_without_source():
    """'refunds in Peru' -> refusal and no 'Source:' line. This is the test that catches invented citations (chapter §6)."""
    # TODO(learner)
    raise NotImplementedError


def test_grounding_metadata_present_on_direct_genai_call():
    """google-genai call with Tool(retrieval=Retrieval(vertex_ai_search=VertexAISearch(datastore=...))) (H12).
    Record the real grounding-metadata field names in the assertion; the map does not give them."""
    # TODO(learner)
    raise NotImplementedError
