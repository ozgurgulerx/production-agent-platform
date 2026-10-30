"""A2A client: resolve the refund specialist's agent card through the Runtime URL and send one
task. Auth: SigV4 with the caller's IAM credentials (the Runtime has no JWT authorizer in this lab);
the card is served at .../invocations/.well-known/agent-card.json (D6)."""
from __future__ import annotations

import asyncio
import os
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01-ways-to-build"))
import httpx  # noqa: E402
from _common import REGION, new_session_id, require, session  # noqa: E402
from botocore.auth import SigV4Auth  # noqa: E402
from botocore.awsrequest import AWSRequest  # noqa: E402

require("TICKET_A2A_RUNTIME_ARN")
ARN = os.environ["TICKET_A2A_RUNTIME_ARN"]
BASE = f"https://bedrock-agentcore.{REGION}.amazonaws.com/runtimes/{urllib.parse.quote(ARN, safe='')}/invocations"
SESSION_ID = new_session_id()


class SigV4(httpx.Auth):
    def auth_flow(self, request: httpx.Request):
        creds = session().get_credentials().get_frozen_credentials()
        aws_req = AWSRequest(method=request.method, url=str(request.url), data=request.content,
                             headers={"X-Amzn-Bedrock-AgentCore-Runtime-Session-Id": SESSION_ID, "content-type": "application/json"})
        SigV4Auth(creds, "bedrock-agentcore", REGION).add_auth(aws_req)
        request.headers.update(dict(aws_req.headers))
        yield request


async def main() -> None:
    from a2a.client import A2ACardResolver, ClientConfig, ClientFactory
    from a2a.types import Message, Part, Role, TextPart

    async with httpx.AsyncClient(auth=SigV4(), timeout=60) as http:
        card = await A2ACardResolver(http, BASE, agent_card_path="/.well-known/agent-card.json").get_agent_card()
        print("card:", card.name, "-", card.description, "| skills:", [s.id for s in card.skills])
        client = ClientFactory(ClientConfig(httpx_client=http, streaming=False)).create(card)
        msg = Message(role=Role.user, message_id="m1", parts=[Part(root=TextPart(text="Refund 480 GBP on T-1003."))])
        async for event in client.send_message(msg):
            print(event)


if __name__ == "__main__":
    asyncio.run(main())
