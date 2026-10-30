"""G04 lab 01: ticket-agent with a `whoami` tool that reports the principal the runtime gave it.
Deployed twice (Agent Identity, then service account) so spec.effectiveIdentity can be compared (map C5, D10).
Status: scaffold only, functionality unverified."""
import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")

INSTRUCTION = (
    "You are the support-ticket agent. When asked who you are running as, call the whoami tool and report "
    "its result verbatim. Never issue refunds; you may only describe refund policy."
)


def whoami(tool_context: ToolContext) -> dict:
    """Report the identity this agent runs as: the principal from the metadata server and whether the
    access token is bound (a `cnf` claim, map D10). Returns a dict with a `status` key (map D1)."""
    # TODO(learner): credentials, _ = google.auth.default(); refresh; decode the token header/claims without
    # verifying; return {"status": "success", "principal": ..., "token_bound": bool, "identity_kind": "agent_identity"|"service_account"}
    return {"status": "error", "message": "TODO(learner): implement whoami"}


root_agent = LlmAgent(
    name="ticket_agent",
    model=GEMINI_MODEL,
    description="Support-ticket agent; lab 01 variant with a whoami tool.",
    instruction=INSTRUCTION,
    tools=[whoami],
)
