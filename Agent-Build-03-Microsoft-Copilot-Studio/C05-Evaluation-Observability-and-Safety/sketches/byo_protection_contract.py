"""Shape of a "bring your own protection" webhook for Copilot Studio (reading map F12, preview).

The platform calls your HTTPS endpoint before every tool invocation in the environment, waits at most one second,
and ALLOWS on timeout. Authentication is a federated identity credential (the platform presents an Entra token; you
validate issuer and audience). Request and response field names below follow the Learn page's description and are
marked ``# verify`` where the exact JSON was not shown. Shape only; the runnable version is labs/03-safety/byo_protection/.
"""
from fastapi import FastAPI, Request

app = FastAPI()

REQUEST_SHAPE = {                                   # verify: exact envelope on external-security-provider page
    "agentId": "<bot GUID>",
    "environmentId": "<env GUID>",
    "conversationId": "<GUID>",
    "user": {"id": "<aad object id>", "tenantId": "<tenant>"},
    "tool": {"name": "issue_refund", "kind": "mcp", "arguments": {"ticket_id": "T-1002", "amount_gbp": 400}},
    "plan": {"step": 2, "of": 3},
}
ALLOW = {"decision": "allow"}
BLOCK = {"decision": "block", "reason": "refund above 250 GBP requires the UK card team"}   # reason is shown to the agent

@app.post("/protect")
async def protect(req: Request) -> dict:
    body = await req.json()                          # keep it local: no outbound calls inside the 1 s budget
    tool = body.get("tool", {})
    if tool.get("name") == "issue_refund" and float(tool.get("arguments", {}).get("amount_gbp", 0)) > 250:
        return BLOCK
    return ALLOW
