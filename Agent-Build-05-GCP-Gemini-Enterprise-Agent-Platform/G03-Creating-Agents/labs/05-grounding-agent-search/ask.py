"""Ask ticket-agent one question that needs a policy citation; print the answer and the raw grounding events.

python ask.py "Is a £80 goodwill refund allowed for a duplicate-charge complaint? Cite the policy."
python ask.py --no-policy-agent "..."      # negative control: ticket_agent without AgentTool(policy_agent)
"""

from __future__ import annotations

import asyncio
import sys

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

import agent as lab


def pick_agent(no_policy_agent: bool) -> Agent:
    if not no_policy_agent:
        return lab.root_agent
    # TODO(learner): return a copy of ticket_agent with only the two function tools (no AgentTool), same instruction
    raise NotImplementedError


async def main(question: str, no_policy_agent: bool) -> None:
    runner = Runner(
        agent=pick_agent(no_policy_agent),
        app_name="ticket-agent",
        session_service=InMemorySessionService(),
        auto_create_session=True,
    )
    content = types.Content(role="user", parts=[types.Part(text=question)])
    async for event in runner.run_async(
        user_id="customer-1", session_id="ground-1", new_message=content
    ):
        # TODO(learner): print function calls (expect policy_agent), any grounding metadata on the event
        # (field names unverified; print the raw event once), and the final text.
        pass


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--no-policy-agent"]
    asyncio.run(
        main(
            args[0] if args else "Is a £80 goodwill refund allowed? Cite the policy.",
            "--no-policy-agent" in sys.argv,
        )
    )
