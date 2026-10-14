"""Contract tests for the support-tickets MCP server (SPEC section 6)."""

import pytest
from mcp import Client

from pap.tools.server import mcp

# One in-memory client per test, opened inside the test so setup and teardown
# share a task (an async-generator fixture trips anyio's cancel-scope check).


async def test_lists_exactly_three_tools():
    async with Client(mcp) as client:
        result = await client.list_tools()
        assert {t.name for t in result.tools} == {"list_tickets", "get_ticket", "get_policy"}
        for tool in result.tools:
            assert tool.annotations.read_only_hint is True
            assert tool.input_schema
            assert tool.output_schema


async def test_list_tickets_filters_by_status_and_limit():
    async with Client(mcp) as client:
        open_result = await client.call_tool("list_tickets", {"status": "open"})
        assert len(open_result.structured_content["result"]) == 4
        limited = await client.call_tool("list_tickets", {"limit": 2})
        assert len(limited.structured_content["result"]) == 2


@pytest.mark.parametrize("limit", [-1, 0, 51])
async def test_list_tickets_rejects_out_of_range_limit(limit):
    async with Client(mcp) as client:
        result = await client.call_tool("list_tickets", {"limit": limit})
        assert result.is_error
        assert "limit must be 1..50" in result.content[0].text
        assert "Traceback" not in result.content[0].text


@pytest.mark.parametrize("limit, expected_count", [(1, 1), (50, 8)])
async def test_list_tickets_accepts_limit_boundaries(limit, expected_count):
    async with Client(mcp) as client:
        result = await client.call_tool("list_tickets", {"limit": limit})
        assert not result.is_error
        assert len(result.structured_content["result"]) == expected_count


async def test_list_tickets_preserves_file_order_and_summary_fields():
    async with Client(mcp) as client:
        all_result = await client.call_tool("list_tickets", {})
        assert [ticket["id"] for ticket in all_result.structured_content["result"]] == [
            f"T-{ticket_id}" for ticket_id in range(1001, 1009)
        ]
        result = await client.call_tool("list_tickets", {"status": "open", "limit": 2})
        tickets = result.structured_content["result"]
        assert [ticket["id"] for ticket in tickets] == ["T-1001", "T-1003"]
        assert all(set(ticket) == {"id", "priority", "status", "subject"} for ticket in tickets)


async def test_list_tickets_rejects_unknown_status():
    async with Client(mcp) as client:
        result = await client.call_tool("list_tickets", {"status": "unknown"})
        assert result.is_error


async def test_get_ticket_returns_full_ticket():
    async with Client(mcp) as client:
        result = await client.call_tool("get_ticket", {"ticket_id": "T-1001"})
        assert result.structured_content["priority"] == "high"
        assert result.structured_content["customer_id"] == "C-42"
        assert result.structured_content["tags"] == ["payments", "card"]
        assert result.structured_content["amount_disputed"] == 120.5


async def test_get_ticket_unknown_id_is_a_readable_error():
    async with Client(mcp) as client:
        result = await client.call_tool("get_ticket", {"ticket_id": "nope"})
        assert result.is_error
        assert "unknown ticket id; call list_tickets first" in result.content[0].text
        assert "Traceback" not in result.content[0].text


async def test_get_policy_returns_text():
    async with Client(mcp) as client:
        result = await client.call_tool("get_policy", {"policy_id": "POL-REFUND-03"})
        assert "500" in result.structured_content["text"]


async def test_get_policy_unknown_id_is_a_readable_error():
    async with Client(mcp) as client:
        result = await client.call_tool("get_policy", {"policy_id": "nope"})
        assert result.is_error
        assert "unknown policy id; ids look like POL-REFUND-01" in result.content[0].text
        assert "Traceback" not in result.content[0].text


async def test_unknown_tool_returns_error_result():
    # SDK 2.3 reports an unknown tool as an isError result, not a -32602 MCPError
    # (SPEC section 6, test 6, assumed the latter).
    async with Client(mcp) as client:
        result = await client.call_tool("does_not_exist", {})
        assert result.is_error
        assert "does_not_exist" in result.content[0].text
