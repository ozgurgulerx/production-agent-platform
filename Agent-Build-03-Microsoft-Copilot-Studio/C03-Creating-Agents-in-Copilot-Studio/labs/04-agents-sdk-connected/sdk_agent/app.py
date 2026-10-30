"""A Microsoft 365 Agents SDK agent (Python, aiohttp) that Copilot Studio can add as a connected agent (B5, C7).

Proves: the Activity protocol on /api/messages is the contract; the loop and the refusal rule live in your code;
auth is federated credentials or managed identity from environment variables (no secrets in files). With no
connection configured the app runs anonymously for local curl tests only.
"""
from __future__ import annotations

import os
import re

from aiohttp import web
from microsoft_agents.activity import ActivityTypes
from microsoft_agents.hosting.aiohttp import CloudAdapter, start_agent_process
from microsoft_agents.hosting.core import AgentApplication, AgentAuthConfiguration, MemoryStorage, TurnContext, TurnState

TICKETS = {
    "T-2041": {"customer": "A. Khan", "country": "UK", "amount_gbp": 400, "issue": "charged twice at a petrol station"},
    "T-2042": {"customer": "M. Rossi", "country": "IT", "amount_gbp": 60, "issue": "card declined abroad"},
}
FACTS = {"sla": "P1 tickets are acknowledged within 1 hour and resolved within 24 hours; P2 within 3 working days."}
REFUND_CAP = 250


ANONYMOUS = not os.environ.get("CONNECTIONS__SERVICE_CONNECTION__SETTINGS__CLIENTID")


def _connection_manager():
    """Federated credentials / managed identity from CONNECTIONS__SERVICE_CONNECTION__SETTINGS__* env vars.

    With no client id the connection is anonymous: fine for local curl tests, never for a registered bot.
    """
    from microsoft_agents.authentication.msal import MsalConnectionManager
    if ANONYMOUS:
        cfg = AgentAuthConfiguration(anonymous_allowed=True)
    else:
        cfg = AgentAuthConfiguration(
            auth_type=os.environ.get("CONNECTIONS__SERVICE_CONNECTION__SETTINGS__AUTHTYPE", "federated_credentials"),
            client_id=os.environ["CONNECTIONS__SERVICE_CONNECTION__SETTINGS__CLIENTID"],
            tenant_id=os.environ.get("CONNECTIONS__SERVICE_CONNECTION__SETTINGS__TENANTID"),
            federated_client_id=os.environ.get("CONNECTIONS__SERVICE_CONNECTION__SETTINGS__FEDERATEDCLIENTID"),
        )
    return MsalConnectionManager(connections_configurations={"SERVICE_CONNECTION": cfg})


CONNECTIONS = _connection_manager()
ADAPTER = CloudAdapter(connection_manager=CONNECTIONS)
APP = AgentApplication[TurnState](storage=MemoryStorage(), adapter=ADAPTER, connection_manager=CONNECTIONS)


def answer(text: str) -> str:
    t = text.lower()
    m = re.search(r"\b(t-\d{4})\b", t)
    if "refund" in t:
        amount = re.search(r"(\d+(?:\.\d+)?)\s*(?:gbp|£|pounds?)", t)
        amt = float(amount.group(1)) if amount else (TICKETS.get(m.group(1).upper(), {}).get("amount_gbp", 0) if m else 0)
        if amt > REFUND_CAP:
            return f"Refunds above {REFUND_CAP} GBP need a human. {amt:.0f} GBP exceeds my limit; I have flagged it for the card team."
        return f"Refund of {amt:.0f} GBP can be issued on {m.group(1).upper() if m else 'the ticket'}."
    if m and m.group(1).upper() in TICKETS:
        tk = TICKETS[m.group(1).upper()]
        return f"{m.group(1).upper()}: {tk['customer']} ({tk['country']}), {tk['amount_gbp']} GBP, {tk['issue']}."
    if "sla" in t or "p1" in t:
        return FACTS["sla"]
    return "I handle ticket lookups, SLAs and refunds up to 250 GBP. Give me a ticket id like T-2041."


@APP.conversation_update("membersAdded")
async def on_members_added(context: TurnContext, state: TurnState) -> None:
    await context.send_activity("Ticket SDK agent ready. Ask about a ticket id, the SLA, or a refund.")


@APP.message(re.compile(r".*"))
async def on_message(context: TurnContext, state: TurnState) -> None:
    await context.send_activity(answer(context.activity.text or ""))


async def messages(request: web.Request) -> web.Response:
    return await start_agent_process(request, APP, ADAPTER)


def main() -> None:
    app = web.Application()
    app.router.add_post("/api/messages", messages)
    app.router.add_get("/health", lambda r: web.json_response({"status": "ok", "anonymous": ANONYMOUS}))
    port = int(os.environ.get("PORT", "3978"))
    print(f"ticket-sdk-agent on :{port} ({'anonymous: local tests only' if ANONYMOUS else 'authenticated'})")
    web.run_app(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
