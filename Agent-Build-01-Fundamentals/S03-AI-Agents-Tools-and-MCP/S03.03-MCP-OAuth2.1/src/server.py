"""Authenticated MCP tools with per-tool scopes and simulated refunds."""
import asyncio
import json
import logging
from pathlib import Path

from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from pydantic import AnyHttpUrl, BaseModel, Field, StrictBool

import functions
from auth import ISSUER, RESOURCE, KeycloakTokenVerifier, require_scope
from refunds import RefundLedger

verifier = KeycloakTokenVerifier()
ledger = RefundLedger()
PRINCIPALS = Path(__file__).resolve().parents[1] / 'data' / 'principals.json'
mcp = FastMCP(
    'support-tickets', token_verifier=verifier,
    auth=AuthSettings(
        issuer_url=AnyHttpUrl(ISSUER), resource_server_url=AnyHttpUrl(RESOURCE),
        required_scopes=[],  # Different tools require different scopes below.
    ),
)


@mcp.tool()
def get_ticket(ticket_id: str) -> dict:
    """Get a ticket; requires tickets.read."""
    require_scope('tickets.read')
    return functions.get_ticket(ticket_id)


@mcp.tool()
def get_policy(policy_id: str) -> dict:
    """Get a policy; requires policies.read."""
    require_scope('policies.read')
    return functions.get_policy(policy_id)


@mcp.tool()
def list_tickets(status: str | None = None, customer_id: str | None = None) -> list[dict]:
    """List ticket summaries; requires tickets.read."""
    require_scope('tickets.read')
    return functions.list_tickets(status=status, customer_id=customer_id)


class RefundConfirmation(BaseModel):
    confirm: StrictBool = Field(description='Approve this exact simulated refund?')


def refund_inputs(subject, ticket_id):
    # Server-owned mapping keyed by verified subject, not username or tool input.
    principals = json.loads(PRINCIPALS.read_text())
    principal = principals.get(subject)
    if not isinstance(principal, dict) or not principal.get('team'):
        raise ToolError('No trusted team mapping for this user.')
    ticket = functions.get_ticket(ticket_id)
    if 'error' in ticket or 'refundable_balance' not in ticket:
        raise ToolError('Ticket is not eligible for this refund demonstration.')
    return principal, ticket


@mcp.tool()
async def issue_refund(ticket_id: str, amount: str, ctx: Context) -> dict:
    """Simulate a GBP refund; requires tickets.refund and human elicitation.

    Supply amount as a decimal string, for example "100.00". Never auto-confirm.
    """
    token = require_scope('tickets.refund')
    principal, ticket = refund_inputs(token.subject, ticket_id)
    try:
        value = ledger.check(principal, ticket, amount)
    except ValueError as error:
        raise ToolError(str(error)) from None
    try:
        params = ctx.request_context.session.client_params
        capabilities = params.capabilities.elicitation if params else None
        if capabilities is None or capabilities.form is None:
            raise ToolError('Client does not support form confirmation.')
        answer = await asyncio.wait_for(ctx.elicit(
            message=f'Simulate refund of GBP {value:.2f} for ticket {ticket_id}? No real payment will occur.',
            schema=RefundConfirmation,
        ), timeout=120)
    except Exception:
        # Unsupported elicitation, disconnects or invalid responses never authorize.
        logging.getLogger(__name__).warning('Refund confirmation unavailable; no refund recorded.')
        raise ToolError('Human confirmation unavailable; no refund recorded.') from None
    if answer.action != 'accept' or answer.data is None or answer.data.confirm is not True:
        return {'status': 'not_executed', 'reason': 'human_confirmation_not_accepted'}
    # Login can expire while a user considers the prompt; balance may also change.
    require_scope('tickets.refund')
    try:
        return ledger.execute(token.subject, principal, ticket, amount)
    except ValueError as error:
        raise ToolError(str(error)) from None


if __name__ == '__main__':
    mcp.run(transport='streamable-http')
