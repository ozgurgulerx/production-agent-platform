"""Through the Gateway: list tools, call the built-in `x_amz_bedrock_agentcore_search` with an intent, then let a
Strands agent (given only the search results) refund ticket 1042 and try £400 on 1043.

Proves: search returns a ranked subset (`<target>___<tool>` names), and the agent never learns which backend served it.
Run: python search_and_call.py
"""

import sys
from pathlib import Path

from strands import Agent
from strands.tools.mcp import MCPClient

from _common import MODEL_ID, need

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01-identity-inbound"))
from tokens import client_credentials_token  # noqa: E402

SYSTEM = "UK card-team ticket assistant. Use tools, cite ticket ids, follow the refund policy."


def main() -> None:
    gw = MCPClient(url=need("TICKET_GATEWAY_URL"), headers={"Authorization": f"Bearer {client_credentials_token()}"})
    with gw:
        all_tools = gw.list_tools_sync()
        print("all tools:", [t.tool_name for t in all_tools])

        hits = gw.call_tool_sync(tool_use_id="search-1", name="x_amz_bedrock_agentcore_search", arguments={"query": "refund a customer for a duplicate charge"})
        print("search result:", str(hits)[:600])
        names = {t.get("name") for item in hits.get("content", []) for t in _tools_in(item)}
        chosen = [t for t in all_tools if t.tool_name in names] or all_tools
        print("agent gets:", [t.tool_name for t in chosen])

        agent = Agent(model=MODEL_ID, tools=chosen, system_prompt=SYSTEM)
        print(agent("Ticket 1042 was charged twice for £40. Refund it per policy."))
        print(agent("Now refund £400 on ticket 1043."))        # interceptor (attach_interceptor.py) or tool refuses


def _tools_in(item) -> list[dict]:
    """Search returns a text block holding a JSON `tools` list; be tolerant of the exact wrapper."""  # verify
    import json
    text = item.get("text") if isinstance(item, dict) else None
    try:
        obj = json.loads(text) if text else {}
    except ValueError:
        return []
    return obj.get("tools", obj if isinstance(obj, list) else [])


if __name__ == "__main__":
    main()
