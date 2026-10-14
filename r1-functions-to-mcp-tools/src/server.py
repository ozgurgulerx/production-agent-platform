# import the server building class
from mcp.server.fastmcp import FastMCP
import functions

# Create a server object
mcp = FastMCP("support-tickets")


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
    mcp.run(transport="stdio")
