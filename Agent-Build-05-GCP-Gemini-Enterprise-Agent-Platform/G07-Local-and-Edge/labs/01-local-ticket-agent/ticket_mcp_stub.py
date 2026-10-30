"""A local stdio MCP server that stands in for the ticketing MCP Toolbox on Cloud Run (G04 lab 03).

Exposes the same two tool names the Toolbox tools.yaml defines, get_ticket and list_tickets, over stdio so both the
ADK agent (McpToolset + StdioConnectionParams, map D3) and Gemini CLI (mcpServers.command, map H6) can start it.
The MCP Python server package is not in the reading map; the import below is the learner's to confirm.

Run:  python ticket_mcp_stub.py              serve over stdio (what the clients do)
      python ticket_mcp_stub.py --selftest   print the tool names and exit
"""

import json
import sys

try:
    from mcp.server.fastmcp import (
        FastMCP,
    )  # package name unverified against the map; ships with google-adk[mcp]
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "mcp server package missing; install the shared venv (google-adk[mcp]) and confirm the import"
    ) from exc

TICKETS = {
    "1042": {
        "status": "open",
        "amount_gbp": 120.0,
        "product": "card replacement",
        "opened": "2026-10-20",
    },
    "1043": {
        "status": "closed",
        "amount_gbp": 0.0,
        "product": "limit raise",
        "opened": "2026-10-18",
    },
    "1051": {
        "status": "open",
        "amount_gbp": 300.0,
        "product": "disputed charge",
        "opened": "2026-10-23",
    },
}

server = FastMCP("tickets-stub")


@server.tool()
def get_ticket(ticket_id: str) -> dict:
    """Look up one support ticket by id. Returns status, amount_gbp, product, opened; or an error key."""
    # TODO(learner): return TICKETS[ticket_id] or {"error": "not found"}; never invent a ticket
    raise NotImplementedError


@server.tool()
def list_tickets(status: str = "open") -> list[dict]:
    """List tickets with the given status (open|closed), each with its id."""
    # TODO(learner)
    raise NotImplementedError


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print(
            json.dumps(
                {"tools": ["get_ticket", "list_tickets"], "tickets": sorted(TICKETS)}
            )
        )
        sys.exit(0)
    server.run(transport="stdio")
