"""Foundry Agent Service: an agent with an `mcp` tool and the approval loop.

Shows the shape of (a) the tool definition the service executes
(`server_url`, `server_label`, `allowed_tools`, `require_approval`,
`project_connection_id`) and (b) the Responses-style loop in which the
service returns an `mcp_approval_request` item and the client answers with an
`mcp_approval_response` linked by `previous_response_id`.

Field names follow the Microsoft Learn pages crawled on 23 Oct 2026
(reading map B1, B2, A4). Untested; check against the pinned SDK before use.
"""

from __future__ import annotations

from typing import Any

TICKETS_MCP = {
    "type": "mcp",
    "server_label": "tickets_uk",
    "server_url": "https://tickets-uk.example.com/mcp",
    # None/omitted means every tool the server lists; pin an allow-list.
    "allowed_tools": ["get_ticket", "list_tickets", "get_policy", "issue_refund"],
    # Default is "always". Reads can skip approval; the money move cannot.
    "require_approval": {"never": ["get_ticket", "list_tickets", "get_policy"]},
    # Credentials live on the project connection, never in the prompt.
    "project_connection_id": "conn-tickets-uk-oauth",
}


def run_with_approvals(client: Any, agent_ref: dict, user_text: str, approve) -> Any:
    """Drive one request until no approval is pending.

    `approve(item) -> bool` is host code: it checks the exact arguments
    (ticket, amount, currency) against task state, not the model's summary.
    """
    response = client.responses.create(
        input=user_text,
        extra_body={"agent": agent_ref},
        stream=False,
    )
    while True:
        pending = [o for o in response.output if o.type == "mcp_approval_request"]
        if not pending:
            return response
        answers = [
            {
                "type": "mcp_approval_response",
                "approval_request_id": item.id,
                "approve": bool(approve(item)),
            }
            for item in pending
        ]
        response = client.responses.create(
            input=answers,
            previous_response_id=response.id,
            extra_body={"agent": agent_ref},
        )
