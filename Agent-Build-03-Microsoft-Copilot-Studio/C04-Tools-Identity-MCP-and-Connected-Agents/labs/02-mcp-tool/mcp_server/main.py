"""The ticket MCP server, the way Copilot Studio wants it: remote, HTTPS, Streamable HTTP at /mcp, stateless.

Written against `mcp` 2.3.0 (FastMCP was renamed MCPServer in 2.x; the Foundry/AWS tracks pin 1.x).

Same four tools as the Foundry and AWS tracks (`issue_refund` returns ESCALATE above 250). Optional API-key mode:
start with `--api-key <value>` (or env TICKET_MCP_API_KEY) and every request must carry `X-API-Key`, which is
exactly what the wizard's "API key (header)" mode sends from the user's connection (reading map D3).
"""
import argparse
import os

import uvicorn
from mcp.server.mcpserver import MCPServer
from mcp.server.transport_security import TransportSecuritySettings
from starlette.responses import JSONResponse

PORT = int(os.environ.get("PORT", "8000"))
mcp = MCPServer("tickets", instructions="UK support-ticket tools; refunds above 250 GBP escalate to a human.")

TICKETS = {
    "1042": {"customer": "Ayşe", "status": "open", "issue": "charged twice for a £40 order", "card_team": "UK"},
    "1043": {"customer": "Mert", "status": "closed", "issue": "late delivery", "card_team": "UK"},
}
POLICIES = {"refund": "Refund duplicate charges in full. Above £250 a human must approve. Never refund closed tickets."}


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


class ApiKeyMiddleware:
    """Pure ASGI middleware (BaseHTTPMiddleware buffers the SSE stream and breaks the transport)."""

    def __init__(self, app, key: str):
        self.app, self.key = app, key.encode()

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope["path"].startswith("/mcp"):
            headers = dict(scope.get("headers") or [])
            if headers.get(b"x-api-key") != self.key:
                await JSONResponse({"error": "missing or wrong X-API-Key"}, status_code=401)(scope, receive, send)
                return
        await self.app(scope, receive, send)


def build_app(api_key: str | None):
    # DNS-rebinding protection is on by default and would reject the Container Apps host name; allow it explicitly
    # or disable the check for the lab (verify: set allowed_hosts=[<fqdn>] in production).
    app = mcp.streamable_http_app(stateless_http=True, host="0.0.0.0",
                                  transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False))
    if api_key:
        app.add_middleware(ApiKeyMiddleware, key=api_key)
    return app


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--api-key", default=os.environ.get("TICKET_MCP_API_KEY"))
    a = ap.parse_args()
    uvicorn.run(build_app(a.api_key), host="0.0.0.0", port=PORT)
