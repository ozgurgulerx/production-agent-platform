"""A web app that calls the Copilot Studio ticket agent on behalf of the signed-in user (Direct-to-Engine, OBO).

Proves: the agent sees the user, not the service, because the app exchanges the user's bearer token for a
CopilotStudio.Copilots.Invoke token with msal's on-behalf-of flow, authenticating itself with a certificate
(reading map C8, C9). No client secret anywhere. Standard-harness agents only.
"""
import os
import sys
from pathlib import Path

import msal
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import StreamingResponse
from microsoft_agents.copilotstudio.client import AgentType, ConnectionSettings, CopilotClient, PowerPlatformCloud
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import AGENT_SCHEMA_NAME, ENVIRONMENT_ID, PP_API, TENANT_ID  # noqa: E402

app = FastAPI(title="Ticket agent web app")
WEBAPP_CLIENT_ID = os.environ.get("WEBAPP_CLIENT_ID", "")
CERT_PATH = os.environ.get("WEBAPP_CERT_PATH", "")
CLOUD = PowerPlatformCloud(os.environ.get("POWER_PLATFORM_CLOUD", "Prod"))
D2E_SCOPE = [f"{PP_API}/CopilotStudio.Copilots.Invoke"]


def _confidential_app() -> msal.ConfidentialClientApplication:
    if not (WEBAPP_CLIENT_ID and CERT_PATH):
        raise HTTPException(500, "set WEBAPP_CLIENT_ID and WEBAPP_CERT_PATH (certificate, never a secret)")
    pem = Path(CERT_PATH).read_text()
    thumbprint = os.environ.get("WEBAPP_CERT_THUMBPRINT", "")   # SHA-1 thumbprint of the uploaded certificate
    return msal.ConfidentialClientApplication(
        WEBAPP_CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential={"private_key": pem, "thumbprint": thumbprint})
    # Alternative without any local key material: a federated identity credential and
    # client_credential={"client_assertion": <token from your workload identity>}.


def obo_token(user_token: str) -> str:
    r = _confidential_app().acquire_token_on_behalf_of(user_assertion=user_token, scopes=D2E_SCOPE)
    if "access_token" not in r:
        raise HTTPException(401, f"OBO failed: {r.get('error_description', r)}")
    return r["access_token"]


class Chat(BaseModel):
    text: str
    conversation_id: str | None = None


@app.post("/chat")
async def chat(body: Chat, authorization: str = Header(default="")):
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "user bearer token required")
    token = obo_token(authorization.split(" ", 1)[1])
    settings = ConnectionSettings(environment_id=ENVIRONMENT_ID, agent_identifier=AGENT_SCHEMA_NAME,
                                  cloud=CLOUD, copilot_agent_type=AgentType.PUBLISHED)
    client = CopilotClient(settings, token)

    async def stream():
        if not body.conversation_id:
            async for act in client.start_conversation():
                if act.text:
                    yield act.text + "\n"
        async for act in client.ask_question(body.text, body.conversation_id):
            if act.type == "message" and act.text:
                yield act.text + "\n"
    return StreamingResponse(stream(), media_type="text/plain")


@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True, "agent": AGENT_SCHEMA_NAME, "environment": ENVIRONMENT_ID}
