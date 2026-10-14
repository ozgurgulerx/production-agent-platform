"""Contract tests for the support-tickets MCP server (SPEC section 6)."""

import pytest
from mcp import Client

from pap.tools.server import mcp

# S1 tool bodies are written by Ozgur (prompt P1). Remove this marker once they pass.
pytestmark = pytest.mark.xfail(reason="S1 tool bodies not written yet", strict=False)

# One in-memory client per test, opened inside the test so setup and teardown
# share a task (an async-generator fixture trips anyio's cancel-scope check).


async def test_lists_exactly_three_tools():
    async with Client(mcp) as client:
        result = await client.list_tools()
        assert {t.name for t in result.tools} == {"list_tickets", "get_ticket", "get_policy"}


async def test_list_tickets_filters_by_status_and_limit():
    async with Client(mcp) as client:
        open_result = await client.call_tool("list_tickets", {"status": "open"})
        assert len(open_result.structured_content["result"]) == 4
        limited = await client.call_tool("list_tickets", {"limit": 2})
        assert len(limited.structured_content["result"]) == 2


async def test_list_tickets_rejects_out_of_range_limit():
    async with Client(mcp) as client:
        result = await client.call_tool("list_tickets", {"limit": 0})
        assert result.is_error
        assert "1..50" in result.content[0].text


async def test_get_ticket_returns_full_ticket():
    async with Client(mcp) as client:
        result = await client.call_tool("get_ticket", {"ticket_id": "T-1001"})
        assert result.structured_content["priority"] == "high"


async def test_get_ticket_unknown_id_is_a_readable_error():
    async with Client(mcp) as client:
        result = await client.call_tool("get_ticket", {"ticket_id": "nope"})
        assert result.is_error
        assert "list_tickets" in result.content[0].text


async def test_get_policy_returns_text():
    async with Client(mcp) as client:
        result = await client.call_tool("get_policy", {"policy_id": "POL-REFUND-03"})
        assert "500" in result.structured_content["text"]


async def test_get_policy_unknown_id_is_a_readable_error():
    async with Client(mcp) as client:
        result = await client.call_tool("get_policy", {"policy_id": "nope"})
        assert result.is_error
        assert "POL-REFUND-01" in result.content[0].text


async def test_unknown_tool_returns_error_result():
    # SDK 2.3 reports an unknown tool as an isError result, not a -32602 MCPError
    # (SPEC section 6, test 6, assumed the latter).
    async with Client(mcp) as client:
        result = await client.call_tool("does_not_exist", {})
        assert result.is_error
        assert "does_not_exist" in result.content[0].text
