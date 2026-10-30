"""List the tools of the ticket MCP server over Streamable HTTP before touching the Copilot Studio wizard.

Proves: the server speaks the transport Copilot Studio requires (D3) and exposes exactly four tools, so a wizard
failure afterwards is a wizard or auth problem, not a server problem. Pass --api-key when the server runs in
API-key mode. Uses the plain `mcp` client, no Copilot Studio involved.
"""
import argparse
import asyncio
import os

from mcp import ClientSession
from mcp.client.streamable_http import create_mcp_http_client, streamable_http_client

from _common import ENV_PATH  # noqa: F401  (loads .env)


async def main(url: str, api_key: str | None) -> None:
    headers = {"X-API-Key": api_key} if api_key else None
    async with create_mcp_http_client(headers=headers) as http:          # mcp 2.x: headers go on the http client
        async with streamable_http_client(url, http_client=http) as streams:
            read, write = streams[0], streams[1]
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                print("tools:", [t.name for t in tools.tools])
                r = await session.call_tool("get_ticket", {"ticket_id": "1042"})
                print("get_ticket 1042:", r.content[0].text if r.content else r)
                r = await session.call_tool("issue_refund", {"ticket_id": "1042", "amount": 400, "reason": "test"})
                print("issue_refund 400:", r.content[0].text if r.content else r)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default=os.environ.get("TICKET_MCP_URL", "http://localhost:8000/mcp"))
    ap.add_argument("--api-key", default=os.environ.get("TICKET_MCP_API_KEY"))
    a = ap.parse_args()
    asyncio.run(main(a.url, a.api_key))
