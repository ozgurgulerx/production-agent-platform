"""Connect a Strands agent to the MCP server on Runtime with a Cognito bearer token and ask a ticket question.

Proves: to the agent a Runtime-hosted MCP server is an ordinary streamable-HTTP server; the only AgentCore-specific
parts are the URL shape and the token. Run: python consume_from_strands.py
"""

import sys
from pathlib import Path

from strands import Agent
from strands.tools.mcp import MCPClient

from _common import MODEL_ID, need

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01-identity-inbound"))
from tokens import client_credentials_token  # noqa: E402

SYSTEM = "You are the UK card-team ticket assistant. Use tools; quote ticket ids; refunds follow the refund policy."


def main() -> None:
    token = client_credentials_token()
    server = MCPClient(url=need("TICKET_MCP_URL"), headers={"Authorization": f"Bearer {token}"})
    with server:
        tools = server.list_tools_sync()
        print("tools:", [t.tool_name for t in tools])
        agent = Agent(model=MODEL_ID, tools=tools, system_prompt=SYSTEM)
        print(agent("Ticket 1042 was charged twice for £40. What does policy say, and can you refund it?"))
        print(agent("And refund ticket 1043 £400 please."))     # expect REFUSED (closed) or ESCALATE


if __name__ == "__main__":
    main()
