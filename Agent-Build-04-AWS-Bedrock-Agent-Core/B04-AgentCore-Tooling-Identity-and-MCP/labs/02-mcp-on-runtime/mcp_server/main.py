"""The ticket MCP server, the way AgentCore Runtime wants it: streamable HTTP on 0.0.0.0:8000 at /mcp, stateless.

Four tools over an in-memory ticket book. `issue_refund` refuses amounts over 250 (policy lives in the tool, the
Gateway interceptor in lab 03 and Cedar in B09 add the outer layers).
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("tickets", host="0.0.0.0", port=8000, stateless_http=True)   # stateless: platform maps Mcp-Session-Id

TICKETS = {
    "1042": {"customer": "Ayşe", "status": "open", "issue": "charged twice for a £40 order", "card_team": "UK"},
    "1043": {"customer": "Mert", "status": "closed", "issue": "late delivery", "card_team": "UK"},
}
POLICIES = {
    "refund": "Refund duplicate charges in full. Above £250 a human must approve. Never refund closed tickets.",
}


@mcp.tool()
def get_ticket(ticket_id: str) -> dict:
    """Return one support ticket by id."""
    return TICKETS.get(ticket_id, {"error": f"no ticket {ticket_id}"})


@mcp.tool()
def list_tickets(status: str = "open") -> list[dict]:
    """List tickets with the given status (open|closed)."""
    return [{"id": k, **v} for k, v in TICKETS.items() if v["status"] == status]


@mcp.tool()
def get_policy(name: str = "refund") -> str:
    """Return the text of a named policy."""
    return POLICIES.get(name, f"no policy {name}")


@mcp.tool()
def issue_refund(ticket_id: str, amount: float, reason: str = "") -> dict:
    """Refund `amount` GBP against a ticket. Returns ESCALATE above 250."""
    t = TICKETS.get(ticket_id)
    if not t:
        return {"error": f"no ticket {ticket_id}"}
    if t["status"] == "closed":
        return {"result": "REFUSED", "why": "ticket is closed"}
    if amount > 250:
        return {"result": "ESCALATE", "why": "above £250 needs a human"}
    return {"result": "REFUNDED", "ticket_id": ticket_id, "amount": amount, "reason": reason}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
