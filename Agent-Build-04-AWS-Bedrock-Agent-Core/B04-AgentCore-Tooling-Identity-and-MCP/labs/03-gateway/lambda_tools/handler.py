"""Ticket tools as one Lambda behind a Gateway MCP target. The Gateway passes the tool name in the client context
(`bedrock-agentcore-tool-name`, formatted `<targetName>___<toolName>`) and the arguments as the event.
Logs the caller so lab 04 can show which principal each credential type produces."""

import json

TICKETS = {"1042": {"customer": "Ayşe", "status": "open", "issue": "charged twice for a £40 order"},
           "1043": {"customer": "Mert", "status": "closed", "issue": "late delivery"}}
POLICIES = {"refund": "Refund duplicate charges in full. Above £250 a human must approve. Never refund closed tickets."}


def handler(event, context):
    cc = getattr(context, "client_context", None)
    custom = (getattr(cc, "custom", None) or {}) if cc else {}
    tool = custom.get("bedrock-agentcore-tool-name", "").split("___")[-1]   # verify: header name per Gateway docs
    print(json.dumps({"tool": tool, "event": event, "identity": getattr(context, "identity", None) and vars(context.identity)}))
    if tool == "get_ticket":
        return TICKETS.get(event["ticket_id"], {"error": "no such ticket"})
    if tool == "list_tickets":
        return [{"id": k, **v} for k, v in TICKETS.items() if v["status"] == event.get("status", "open")]
    if tool == "get_policy":
        return POLICIES.get(event.get("name", "refund"), "no policy")
    if tool == "issue_refund":
        t = TICKETS.get(event["ticket_id"])
        if not t:
            return {"error": "no such ticket"}
        if t["status"] == "closed":
            return {"result": "REFUSED", "why": "closed"}
        if float(event["amount"]) > 250:
            return {"result": "ESCALATE", "why": "above £250"}
        return {"result": "REFUNDED", "amount": event["amount"], "ticket_id": event["ticket_id"]}
    return {"error": f"unknown tool {tool!r}"}
