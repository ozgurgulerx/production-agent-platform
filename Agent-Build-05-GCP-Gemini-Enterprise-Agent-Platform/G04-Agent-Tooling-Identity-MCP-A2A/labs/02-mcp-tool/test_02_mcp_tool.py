"""pytest skeletons for G04 lab 02. Learner writes the bodies; no placeholder passes (AGENTS.md).
Status: scaffold only, functionality unverified."""
import pytest


def test_callback_allows_non_refund_tools():
    """refuse_refund_outside_policy returns None for lookup_ticket (map B4)."""
    # TODO(learner): build a fake tool with .name == "lookup_ticket" and assert None
    pytest.skip("TODO(learner)")


def test_callback_refuses_refund_over_limit():
    """amount > 50 is refused with a reason that names the policy."""
    pytest.skip("TODO(learner)")


def test_callback_refuses_refund_older_than_30_days():
    pytest.skip("TODO(learner)")


def test_callback_allows_refund_inside_policy():
    pytest.skip("TODO(learner)")


@pytest.mark.integration
def test_toolset_lists_filtered_tools_only():
    """Needs the toolbox binary and a Postgres: await ticketing.get_tools() and compare names to tool_filter (map D3)."""
    pytest.skip("TODO(learner): needs toolbox + Postgres")
