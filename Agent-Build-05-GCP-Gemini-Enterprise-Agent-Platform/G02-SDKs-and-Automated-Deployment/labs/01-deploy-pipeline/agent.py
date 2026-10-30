"""ticket-agent: the S03 support-ticket agent, deployable by adk deploy, SDK or Terraform.

ADK 2.13 (map B1, D1, D3). Model id from .env, never hard-coded. McpToolset is defined synchronously
here (D3) and only when TICKET_MCP_URL is set; otherwise the stub tool answers so `adk run .` works
before G04 lab 03 exists. Status 25 Oct 2026: scaffold only, functionality unverified.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent

load_dotenv()

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")  # .env; default is the quickstart id (map C1)
TICKET_MCP_URL = os.environ.get("TICKET_MCP_URL", "")

INSTRUCTION = """You answer customer support tickets for a UK bank.
Look tickets up with the tool before answering. Cite the policy document you relied on.
Refuse any refund outside policy and say which rule applies. Never invent ticket data."""


def lookup_ticket(ticket_id: str) -> dict:
    """Return the ticket record for ticket_id, or status=not_found.

    Stub used when TICKET_MCP_URL is empty. TODO(learner): return a small fixed table of tickets
    (id, customer, amount_gbp, opened) and a `status` key (D1).
    """
    raise NotImplementedError("TODO(learner)")


def refund_policy(amount_gbp: float, days_since_purchase: int) -> dict:
    """Decide whether a refund is inside policy. The refusal lives here, not in the prompt.

    TODO(learner): encode the S03 policy (threshold and window), return {"status": "ok"|"refused",
    "rule": "<policy clause>"}.
    """
    raise NotImplementedError("TODO(learner)")


def _tools() -> list:
    if not TICKET_MCP_URL:
        return [lookup_ticket, refund_policy]
    # D3: McpToolset over Streamable HTTP to the Toolbox on Cloud Run (G04 lab 03).
    from google.adk.tools.mcp_tool import McpToolset
    from google.adk.tools.mcp_tool.mcp_session_manager import (
        StreamableHTTPConnectionParams,
    )

    # TODO(learner): auth_scheme/auth_credential for the Cloud Run invoker token (D5); tool_filter
    # to the ticket tools only.
    return [
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(url=TICKET_MCP_URL)
        ),
        refund_policy,
    ]


root_agent = LlmAgent(
    name="ticket_agent",
    model=MODEL,
    description="Answers support tickets, refuses out-of-policy refunds, cites policy.",
    instruction=INSTRUCTION,
    tools=_tools(),
)
