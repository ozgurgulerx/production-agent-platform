"""The ticket REST API behind openapi-v2.json, for the Copilot Studio REST tool (reading map D8).

Proves: the same four operations as the MCP server, this time as plain HTTP with an X-API-Key header, so the
agent's REST tool connection asks each user for the key. Run locally with `uvicorn ticket_api.app:app --port 8001`
or on Container Apps. Key defaults to `dev`; set TICKET_API_KEY in the container.
"""
import os

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Ticket API", version="1.0")
API_KEY = os.environ.get("TICKET_API_KEY", "dev")

TICKETS = {
    "1042": {"id": "1042", "customer": "Ayşe", "status": "open", "issue": "charged twice for a £40 order", "card_team": "UK"},
    "1043": {"id": "1043", "customer": "Mert", "status": "closed", "issue": "late delivery", "card_team": "UK"},
}
POLICIES = {"refund": "Refund duplicate charges in full. Above £250 a human must approve. Never refund closed tickets."}


def auth(x_api_key: str = Header(default="")) -> None:
    if x_api_key != API_KEY:
        raise HTTPException(401, "missing or wrong X-API-Key")


class RefundBody(BaseModel):
    amount: float
    reason: str = ""


@app.get("/tickets", dependencies=[Depends(auth)])
def list_tickets(status: str = "open") -> list[dict]:
    return [t for t in TICKETS.values() if t["status"] == status]


@app.get("/tickets/{ticket_id}", dependencies=[Depends(auth)])
def get_ticket(ticket_id: str) -> dict:
    if ticket_id not in TICKETS:
        raise HTTPException(404, f"no ticket {ticket_id}")
    return TICKETS[ticket_id]


@app.get("/policies/{name}", dependencies=[Depends(auth)])
def get_policy(name: str) -> dict:
    return {"name": name, "text": POLICIES.get(name, f"no policy {name}")}


@app.post("/tickets/{ticket_id}/refund", dependencies=[Depends(auth)])
def issue_refund(ticket_id: str, body: RefundBody) -> dict:
    t = TICKETS.get(ticket_id)
    if not t:
        raise HTTPException(404, f"no ticket {ticket_id}")
    if t["status"] == "closed":
        return {"result": "REFUSED", "why": "ticket is closed"}
    if body.amount > 250:
        return {"result": "ESCALATE", "why": "above £250 needs a human"}
    return {"result": "REFUNDED", "why": body.reason}
