import json

import pytest
from mcp.shared.memory import create_connected_server_and_client_session

from server import mcp


async def test_server_lists_three_tools():
    async with create_connected_server_and_client_session(mcp) as session:
        result = await session.list_tools()

        names = {tool.name for tool in result.tools}

        assert names == {"get_ticket", "get_policy", "list_tickets"}


async def test_tools_have_descriptions():
    async with create_connected_server_and_client_session(mcp) as session:
        result = await session.list_tools()

        for tool in result.tools:
            assert tool.description
            assert tool.description.strip()


async def test_tool_input_schemas():
    async with create_connected_server_and_client_session(mcp) as session:
        result = await session.list_tools()
        schemas = {tool.name: tool.inputSchema for tool in result.tools}

        for name, parameter in [("get_ticket", "ticket_id"), ("get_policy", "policy_id")]:
            schema = schemas[name]
            assert schema["type"] == "object"
            assert schema["required"] == [parameter]
            assert schema["properties"][parameter]["type"] == "string"

        schema = schemas["list_tickets"]
        assert schema["type"] == "object"
        assert not schema.get("required")
        assert set(schema["properties"]) == {"status", "customer_id"}
        for parameter in ["status", "customer_id"]:
            field = schema["properties"][parameter]
            assert field["default"] is None
            assert {option["type"] for option in field["anyOf"]} == {"string", "null"}


async def test_get_ticket_found():
    async with create_connected_server_and_client_session(mcp) as session:
        result = await session.call_tool("get_ticket", {"ticket_id": "T-1001"})
        assert not result.isError
        ticket = json.loads(result.content[0].text)
        assert ticket["id"] == "T-1001"
        assert ticket["subject"] == "Card declined twice"
        assert ticket["customer_id"] == "C-42"


async def test_get_ticket_not_found():
    async with create_connected_server_and_client_session(mcp) as session:
        result = await session.call_tool("get_ticket", {"ticket_id": "DOES-NOT-EXIST"})
        assert not result.isError
        assert json.loads(result.content[0].text) == {
            "error": "not_found", "id": "DOES-NOT-EXIST"
        }


async def test_get_policy_found():
    async with create_connected_server_and_client_session(mcp) as session:
        result = await session.call_tool("get_policy", {"policy_id": "POL-REFUND-01"})
        assert not result.isError
        policy = json.loads(result.content[0].text)
        assert policy["id"] == "POL-REFUND-01"
        assert policy["title"] == "Refund window"
        assert "30 days" in policy["text"]


async def test_get_policy_not_found():
    async with create_connected_server_and_client_session(mcp) as session:
        result = await session.call_tool("get_policy", {"policy_id": "DOES-NOT-EXIST"})
        assert not result.isError
        assert json.loads(result.content[0].text) == {
            "error": "not_found", "id": "DOES-NOT-EXIST"
        }


@pytest.mark.parametrize(
    "arguments, expected_ids",
    [
        ({}, {f"T-{number}" for number in range(1001, 1009)}),
        ({"status": "open"}, {"T-1001", "T-1003", "T-1006", "T-1008"}),
        ({"customer_id": "C-55"}, {"T-1006", "T-1007"}),
        ({"status": "open", "customer_id": "C-55"}, {"T-1006"}),
        ({"customer_id": "DOES-NOT-EXIST"}, set()),
    ],
    ids=["all", "status-filter", "customer-filter", "both-filters", "no-matches"],
)
async def test_list_tickets(arguments, expected_ids):
    async with create_connected_server_and_client_session(mcp) as session:
        result = await session.call_tool("list_tickets", arguments)
        assert not result.isError
        # This SDK returns one text content block per ticket; no matches gives no blocks.
        tickets = [json.loads(block.text) for block in result.content]
        assert {ticket["id"] for ticket in tickets} == expected_ids
        assert len(tickets) == len(expected_ids)
        for ticket in tickets:
            assert set(ticket) == {"id", "subject", "status", "customer_id", "created_at"}


async def test_get_ticket_requires_id():
    async with create_connected_server_and_client_session(mcp) as session:
        result = await session.call_tool("get_ticket", {})
        assert result.isError
