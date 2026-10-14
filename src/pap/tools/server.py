"""support-tickets MCP server shell (S1). Tool bodies are written by Ozgur, not Claude."""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Literal

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations
from pydantic import BaseModel

# stdout is the protocol channel over stdio, so logs go to stderr only.
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
log = logging.getLogger("support-tickets")

DATA_DIR = Path(os.environ.get("TICKETS_DATA_DIR", Path(__file__).resolve().parents[3] / "data"))


class TicketSummary(BaseModel):
    id: str
    priority: str
    status: str
    subject: str


class Ticket(BaseModel):
    id: str
    customer_id: str
    created_at: str
    priority: str
    status: str
    subject: str
    tags: list[str] | None = None
    amount_disputed: float | None = None


class Policy(BaseModel):
    id: str
    title: str
    text: str


def _load(name: str) -> list[dict[str, Any]]:
    data: list[dict[str, Any]] = json.loads((DATA_DIR / name).read_text())
    return data


TICKETS = [Ticket(**t) for t in _load("tickets.json")]
POLICIES = [Policy(**p) for p in _load("policies.json")]
log.info("loaded %d tickets and %d policies from %s", len(TICKETS), len(POLICIES), DATA_DIR)

mcp = MCPServer("support-tickets")
READ_ONLY = ToolAnnotations(read_only_hint=True)


@mcp.tool(annotations=READ_ONLY)
def list_tickets(
    status: Literal["open", "pending", "closed"] | None = None, limit: int = 10
) -> list[TicketSummary]:
    """List support tickets, optionally filtered by status.

    Use this first to discover ticket ids. Use get_ticket when you already
    have an id and need the full record. limit must be 1..50.
    """
    raise NotImplementedError("S1: Ozgur writes this body")


@mcp.tool(annotations=READ_ONLY)
def get_ticket(ticket_id: str) -> Ticket:
    """Return the full record for one ticket id such as T-1001.

    Use this when you already have an id; otherwise call list_tickets first.
    """
    raise NotImplementedError("S1: Ozgur writes this body")


@mcp.tool(annotations=READ_ONLY)
def get_policy(policy_id: str) -> Policy:
    """Return one refund, dispute or data policy by id, such as POL-REFUND-01.

    Use this to quote the rule that applies to a ticket.
    """
    raise NotImplementedError("S1: Ozgur writes this body")


if __name__ == "__main__":
    mcp.run()
