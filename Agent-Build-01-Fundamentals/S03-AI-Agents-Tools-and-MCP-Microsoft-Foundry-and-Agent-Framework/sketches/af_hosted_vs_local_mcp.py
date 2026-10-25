"""Microsoft Agent Framework (Python): the same MCP server attached two ways.

Hosted marker: `client.get_mcp_tool(...)` looks like a local tool in code but
the Foundry service connects to the server and runs the call. Local client:
`MCPStreamableHTTPTool` makes your process hold the connection, the identity
header, the retries and the trust boundary. A function middleware shows where
S03.06-style checks sit for locally executed calls.

Names follow Agent Framework pages crawled on 23 Oct 2026 (reading map F5,
F6, G5). Untested; parameter names change between betas, check the pin.
"""

from __future__ import annotations

import os
from typing import Any

SERVER_URL = "https://tickets-uk.example.com/mcp"
READ_ONLY = ["get_ticket", "list_tickets", "get_policy"]


def hosted_tool(client: Any) -> Any:
    """Service-side execution. Approval follows Foundry's rules, not yours."""
    return client.get_mcp_tool(
        name="tickets_uk",
        url=SERVER_URL,
        allowed_tools=READ_ONLY + ["issue_refund"],
        approval_mode={"never_require": READ_ONLY},
    )


def local_tool(token_for_user) -> Any:
    """Client-side execution. Your process authenticates and enforces."""
    from agent_framework import MCPStreamableHTTPTool  # noqa: WPS433

    async def header_provider() -> dict[str, str]:
        return {"Authorization": f"Bearer {await token_for_user()}"}

    return MCPStreamableHTTPTool(
        name="tickets_uk",
        url=SERVER_URL,
        header_provider=header_provider,
        allowed_tools=READ_ONLY + ["issue_refund"],
        approval_mode="always_require",
        tool_name_prefix="tickets_uk_",
    )


async def refund_guard(context: Any, call_next) -> None:
    """Function middleware: the backend authorises the effect, not the model."""
    if context.function.name.endswith("issue_refund"):
        args = context.arguments or {}
        if args.get("currency") != "GBP" or float(args.get("amount", 0)) > 500:
            context.result = {"isError": True, "content": "refund outside policy"}
            return
    await call_next()


def build_agent(client: Any, token_for_user, use_hosted: bool) -> Any:
    tool = hosted_tool(client) if use_hosted else local_tool(token_for_user)
    return client.as_agent(
        name="support",
        instructions="Resolve the ticket. Never refund without a matching policy.",
        tools=[tool],
        middleware=[refund_guard],
    )


if __name__ == "__main__":
    print("hosted" if os.getenv("USE_HOSTED") else "local")
