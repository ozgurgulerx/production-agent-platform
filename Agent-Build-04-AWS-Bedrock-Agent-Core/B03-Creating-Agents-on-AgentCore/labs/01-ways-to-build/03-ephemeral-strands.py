"""Way 5, ephemeral: the same ticket agent in this process, calling Bedrock directly.
Proves that no AgentCore resource is needed to run the loop; it also proves what you give up
(no session isolation, no versions, no managed identity, tracing only if you wire ADOT yourself).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "agent"))
from _common import MODEL_ID, session  # noqa: E402
from main import INSTRUCTIONS, get_policy, get_ticket, issue_refund, list_tickets  # noqa: E402
from strands import Agent  # noqa: E402
from strands.models import BedrockModel  # noqa: E402

model = BedrockModel(model_id=MODEL_ID, boto_session=session(), max_tokens=600)
agent = Agent(model=model, system_prompt=INSTRUCTIONS, tools=[get_ticket, list_tickets, get_policy, issue_refund])

for prompt in [
    "What is ticket T-1001 about?",
    "Refund the 4.50 on T-1001.",
    "Refund the full 480 on T-1003.",  # must be refused by the tool rule, not by the model's mood
]:
    print(f"\n> {prompt}")
    print(agent(prompt))

print("\nmetrics:", agent.event_loop_metrics.get_summary()["accumulated_usage"])
