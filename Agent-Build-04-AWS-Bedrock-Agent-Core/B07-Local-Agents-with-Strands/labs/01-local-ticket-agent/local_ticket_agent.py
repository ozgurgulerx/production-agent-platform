"""The B03 ticket agent, same Strands code, with the model swapped for a local one.

Proves: the provider is a constructor argument; tools, prompt and the 250 GBP refusal do not change;
no guardrail, identity or trace comes along. Run: python local_ticket_agent.py --provider ollama|llamacpp|bedrock
Local providers need no .env and no AWS credential.
"""
from __future__ import annotations

import argparse
import os

from strands import Agent, tool
from strands.hooks import AfterToolCallEvent, HookProvider, HookRegistry

TICKETS = {
    "T-1001": {"customer": "Ayşe", "issue": "charged twice for a coffee", "amount_gbp": 4.50, "status": "open"},
    "T-1002": {"customer": "Mert", "issue": "card declined abroad", "amount_gbp": 0, "status": "open"},
    "T-1003": {"customer": "Priya", "issue": "disputed hotel charge", "amount_gbp": 480.00, "status": "open"},
}
POLICIES = {"refund": "Refunds up to 250 GBP may be issued by the agent; above that a human must approve."}
INSTRUCTIONS = ("You are the support-ticket assistant for a UK bank's card team. Answer briefly. "
                "Use the tools for ticket facts; never invent a ticket. Refunds above 250 GBP need a human.")
QUESTIONS = ["What is the status of ticket T-1001?", "Refund 300 GBP on ticket T-1003.", "Refund 120 GBP on ticket T-1003."]


@tool
def get_ticket(ticket_id: str) -> dict:
    """Return one support ticket by id, or an error if it does not exist."""
    return TICKETS.get(ticket_id, {"error": f"no ticket {ticket_id}"})


@tool
def list_tickets(status: str = "open") -> list[dict]:
    """List tickets with the given status."""
    return [{"id": k, **v} for k, v in TICKETS.items() if v["status"] == status]


@tool
def get_policy(name: str) -> str:
    """Return the text of a named policy (e.g. 'refund')."""
    return POLICIES.get(name, "no such policy")


@tool
def issue_refund(ticket_id: str, amount_gbp: float) -> dict:
    """Issue a refund against a ticket. Amounts above 250 GBP are refused and escalated."""
    if amount_gbp > 250:
        return {"status": "refused", "reason": "above 250 GBP, needs human approval", "ticket_id": ticket_id}
    return {"status": "issued", "ticket_id": ticket_id, "amount_gbp": amount_gbp}


class PrintToolCalls(HookProvider):
    """Shows which tools the local model actually called; there is no CloudWatch trace here."""

    def register_hooks(self, registry: HookRegistry, **kwargs) -> None:
        registry.add_callback(AfterToolCallEvent, lambda e: print(f"   tool {e.tool_use['name']}({e.tool_use['input']}) -> {str(e.result)[:80]}"))


def make_model(provider: str, model_id: str | None):
    if provider == "ollama":
        try:
            from strands.models.ollama import OllamaModel
        except ModuleNotFoundError as exc:  # the extra is not in the shared requirements on purpose
            raise SystemExit('pip install "strands-agents[ollama]" into the shared venv first') from exc
        return OllamaModel(host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"), model_id=model_id or "qwen3:8b", keep_alive="5m")
    if provider == "llamacpp":
        from strands.models.llamacpp import LlamaCppModel
        return LlamaCppModel(base_url=os.environ.get("LLAMACPP_URL", "http://localhost:8080"), model_id=model_id or "default")
    if provider == "bedrock":
        if not (os.environ.get("AWS_PROFILE") or os.environ.get("AWS_ACCESS_KEY_ID") or os.environ.get("AWS_CONTAINER_CREDENTIALS_RELATIVE_URI")):
            raise SystemExit("bedrock provider needs AWS_PROFILE (SSO) in the environment; this lab is otherwise offline")
        from strands.models import BedrockModel
        return BedrockModel(model_id=model_id or os.environ.get("BEDROCK_MODEL_ID", "global.anthropic.claude-haiku-5-5"),
                            region_name=os.environ.get("AWS_REGION", "us-east-1"))
    raise SystemExit(f"unknown provider {provider}")


def build_agent(provider: str, model_id: str | None) -> Agent:
    return Agent(model=make_model(provider, model_id), system_prompt=INSTRUCTIONS,
                 tools=[get_ticket, list_tickets, get_policy, issue_refund], hooks=[PrintToolCalls()], callback_handler=None)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", choices=["ollama", "llamacpp", "bedrock"], default="ollama")
    ap.add_argument("--model", default=None, help="qwen3:8b | gpt-oss:20b | llama.cpp alias | Bedrock inference profile")
    args = ap.parse_args()
    agent = build_agent(args.provider, args.model)
    print(f"provider={args.provider} model={agent.model.get_config().get('model_id')}")
    for q in QUESTIONS:
        print(f"\nQ: {q}")
        print(f"A: {agent(q)}")
    print("\nNothing scanned these prompts, tool calls or outputs. That is the §6 list; you own it here.")


if __name__ == "__main__":
    main()
