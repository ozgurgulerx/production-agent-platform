"""Strands hook that runs Bedrock ApplyGuardrail on every tool result (source=OUTPUT). Shape only, not run.

Why: a guardrail passed to BedrockModel sees the user turn and the model answer. A card number inside a
get_ticket result is a tool output and never reaches that guardrail. This hook closes the gap in-process;
B09 closes it at the Gateway with Guardrails-in-Policy.
"""
import json
import boto3
from strands.hooks import AfterToolCallEvent, HookProvider, HookRegistry


class ToolOutputGuardrail(HookProvider):
    def __init__(self, guardrail_id: str, guardrail_version: str, region: str):
        self.gid, self.gver = guardrail_id, guardrail_version
        self.rt = boto3.client("bedrock-runtime", region_name=region)

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(AfterToolCallEvent, self.check)

    def check(self, event: AfterToolCallEvent) -> None:
        text = json.dumps(event.result.get("content", ""), default=str)
        verdict = self.rt.apply_guardrail(
            guardrailIdentifier=self.gid, guardrailVersion=self.gver,
            source="OUTPUT", content=[{"text": {"text": text}}], outputScope="INTERVENTIONS")
        if verdict["action"] == "GUARDRAIL_INTERVENED":
            event.result["content"] = [{"text": "[tool output withheld by guardrail: "
                                               + verdict.get("actionReason", "policy") + "]"}]
            event.result["status"] = "error"

# agent = Agent(model=BedrockModel(...), tools=[get_ticket, issue_refund],
#               hooks=[ToolOutputGuardrail(GUARDRAIL_ID, GUARDRAIL_VERSION, REGION)])
