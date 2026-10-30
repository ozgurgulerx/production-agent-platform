"""Proves: the leak a model guardrail misses. get_ticket returns a card number inside the tool result; the
model guardrail never sees it. A Strands AfterToolCallEvent hook runs ApplyGuardrail(source=OUTPUT) on the
result and replaces it when the guardrail intervenes. Run with --no-hook first to see the number pass through.
"""
import json
import sys
from strands import Agent, tool
from strands.hooks import AfterToolCallEvent, HookProvider, HookRegistry
from strands.models import BedrockModel
from _common import MODEL_ID, REGION, require_guardrail, runtime, session

gid, gver = require_guardrail()


@tool
def get_ticket(ticket_id: str) -> dict:
    """Return the support ticket with the given id (this backend leaks the card number)."""
    return {"ticket": ticket_id, "customer": "Ayşe", "amount": 120.0, "card": "4111 1111 1111 1111"}


class ToolOutputGuardrail(HookProvider):
    def __init__(self):
        self.rt = runtime()

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(AfterToolCallEvent, self.check)

    def check(self, event: AfterToolCallEvent) -> None:
        text = json.dumps(event.result.get("content", ""), default=str)
        v = self.rt.apply_guardrail(guardrailIdentifier=gid, guardrailVersion=gver, source="OUTPUT",
                                    content=[{"text": {"text": text}}], outputScope="INTERVENTIONS")
        print(f"   [hook] {event.tool_use['name']} -> {v['action']} {v.get('actionReason','')}")
        if v["action"] == "GUARDRAIL_INTERVENED":
            cleaned = "".join(o.get("text", "") for o in v.get("outputs", [])) or "[tool output withheld by guardrail]"
            event.result["content"] = [{"text": cleaned}]


hooks = [] if "--no-hook" in sys.argv else [ToolOutputGuardrail()]
agent = Agent(model=BedrockModel(model_id=MODEL_ID, boto_session=session(), region_name=REGION),
              tools=[get_ticket], hooks=hooks,
              system_prompt="You are the UK support-ticket assistant. Answer with every field the tool returns.")
print("<", str(agent("Show me everything on ticket T-1001."))[:400])
print("\nexpect: --no-hook prints the card number; with the hook the number is anonymised (PII action ANONYMIZE) before the model sees it")
