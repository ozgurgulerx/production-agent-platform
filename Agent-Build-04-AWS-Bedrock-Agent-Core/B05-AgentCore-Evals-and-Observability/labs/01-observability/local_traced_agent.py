"""Proves: a Strands agent emits gen_ai.* spans you can read, locally (console) or in CloudWatch (OTLP).

Default: console exporter, so you see the span tree without any infrastructure.
With --otlp: OTLP exporter configured from the standard OTEL_* env vars, the same path ADOT uses on Runtime
(set OTEL_EXPORTER_OTLP_ENDPOINT / headers from the chapter, section 7, before running).
"""
import sys
from strands import Agent, tool
from strands.models import BedrockModel
from strands.telemetry import StrandsTelemetry
from _common import MODEL_ID, REGION, session

TICKETS = {"T-1001": {"customer": "Ayşe", "amount": 120.0, "status": "open", "card_country": "GB"},
           "T-1002": {"customer": "Mert", "amount": 400.0, "status": "open", "card_country": "GB"}}


@tool
def get_ticket(ticket_id: str) -> dict:
    """Return the support ticket with the given id."""
    return TICKETS.get(ticket_id, {"error": "not found"})


@tool
def issue_refund(ticket_id: str, amount: float) -> str:
    """Refund the ticket. Policy: at most 250 GBP, GB cards only; otherwise escalate."""
    t = TICKETS.get(ticket_id)
    if not t or amount > 250 or t["card_country"] != "GB":
        return "REFUSED: outside policy, escalate to the UK card team"
    return f"refunded {amount} GBP on {ticket_id}"


telemetry = StrandsTelemetry()
if "--otlp" in sys.argv:
    telemetry.setup_otlp_exporter()      # reads OTEL_EXPORTER_OTLP_* env; ADOT does the same on Runtime
else:
    telemetry.setup_console_exporter()   # prints spans to stdout

agent = Agent(
    name="ticket-agent-local",
    model=BedrockModel(model_id=MODEL_ID, boto_session=session(), region_name=REGION),
    system_prompt="You are the UK support-ticket assistant. Use the tools. Never refund above policy.",
    tools=[get_ticket, issue_refund],
    trace_attributes={"lab": "B05-01", "session.id": "b05-local-demo"},
)
result = agent("Refund ticket T-1002 in full, please.")
print("\nANSWER:", str(result))
print("expect spans: invoke_agent -> execute_event_loop_cycle -> chat (gen_ai.usage.*) -> Tool: get_ticket, Tool: issue_refund (gen_ai.tool.name)")
