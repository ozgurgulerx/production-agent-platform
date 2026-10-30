"""The F03 ticket agent, same Agent Framework code, pointed at a model served by Foundry Local.

Run:  python local_ticket_agent.py [alias]        (default alias qwen2.5-0.5b; try phi-4-mini for better tool use)
No .env, no Azure, no credential. First run downloads the model variant for this machine.
"""
import asyncio, sys
from typing import Annotated
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from foundry_local_sdk import Configuration, FoundryLocalManager   # package foundry-local-sdk 2.2.1; Learn's snippet says `foundry_local`

ALIAS = sys.argv[1] if len(sys.argv) > 1 else "qwen2.5-0.5b"
TICKETS = {"1042": {"status": "open", "amount_gbp": 120.0, "product": "card replacement"}}

def get_ticket(ticket_id: Annotated[str, "Ticket id such as 1042"]) -> dict:
    """Look up a support ticket."""
    return TICKETS.get(ticket_id, {"error": "not found"})

def issue_refund(ticket_id: Annotated[str, "Ticket id"], amount_gbp: Annotated[float, "Amount in GBP"]) -> str:
    """Refund a ticket. Policy: above 250 GBP needs a second approver (the agent must refuse)."""
    return "refused: needs second approver" if amount_gbp > 250 else f"refunded {amount_gbp:.2f} on {ticket_id}"

async def main():
    FoundryLocalManager.initialize(Configuration(app_name="python0x_f07"))
    manager = FoundryLocalManager.instance
    model = manager.get_catalog().get_model(ALIAS)              # 2.2.1: get_catalog(), not .catalog
    if model is None: raise SystemExit(f"{ALIAS} not in the catalogue; try: foundry model list")
    if not model.is_cached: model.download()
    model.load()
    print(f"{model.alias} -> {model.id}  tool calling: {model.supports_tool_calling}")
    manager.start_web_service()                      # dynamic port; never hard-code it
    base_url = f"{manager.urls[0]}/v1"
    print(f"local endpoint {base_url}  model id {model.id}")
    try:
        client = OpenAIChatClient(base_url=base_url, api_key="none", model=model.id)
        agent = Agent(client=client, name="ticket-agent-local", tools=[get_ticket, issue_refund],
                      instructions="UK card team support assistant. Use tools. Refunds above 250 GBP need a second approver: refuse and say so.")
        for q in ["What is the status of ticket 1042?", "Refund 300 GBP on ticket 1042.", "Refund 120 GBP on ticket 1042."]:
            r = await agent.run(q); print(f"\nQ: {q}\nA: {r}")
    finally:
        manager.stop_web_service(); manager.shutdown()
    print("\nNothing scanned these prompts or outputs. That is the §6 list; you own it here.")

asyncio.run(main())
