from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl
from mcp.server.fastmcp import FastMCP
import functions


class DenyAllTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        return None
    
# Create a server object and enable TokenVerifier on it 
mcp = FastMCP(
    "support-tickets",
    token_verifier=DenyAllTokenVerifier(),
    auth=AuthSettings(
        issuer_url=AnyHttpUrl("http://127.0.0.1:9000/realms/s03-mcp"),
        resource_server_url=AnyHttpUrl("http://127.0.0.1:8000/mcp"),
        required_scopes=[],
    ),
)


# Register each individual function as an mcp tool


@mcp.tool()
def get_ticket(ticket_id: str) -> dict:
    """Get the full details of the ticket by its id."""
    return functions.get_ticket(ticket_id)

@mcp.tool()
def get_policy(policy_id: str) -> dict:
    """Get the full details of the policy by its id."""
    return functions.get_policy(policy_id)

@mcp.tool()
def list_tickets(
    status: str | None = None,
    customer_id: str | None = None,
) -> list[dict]:
    """List ticket summaries, optionally filtered by status and customer ID."""
    return functions.list_tickets(status=status, customer_id=customer_id)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
