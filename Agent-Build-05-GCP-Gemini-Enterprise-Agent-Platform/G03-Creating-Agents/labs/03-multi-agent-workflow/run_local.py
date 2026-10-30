"""Run ticket-agent-workflow in-process and print each step's output_key (B2, B5).

Run:  python run_local.py
Proof: category, facts, and a final reply that refuses the goodwill refund with a policy citation.
"""

from __future__ import annotations

import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from ticket_agent_workflow.agent import root_agent

APP_NAME = "ticket-agent-workflow"
MESSAGE = "My card was charged twice for order 8841 (ticket 1042). Also, can I have £80 goodwill for the hassle?"


async def main() -> None:
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
        auto_create_session=True,
    )
    content = types.Content(role="user", parts=[types.Part(text=MESSAGE)])
    async for event in runner.run_async(
        user_id="customer-1", session_id="wf-1", new_message=content
    ):
        # TODO(learner): print f"[{event.author}] ..." for each final text so the three steps are visible.
        pass
    # TODO(learner): fetch the session and print session.state["category"] and session.state["facts"] (B2).


if __name__ == "__main__":
    asyncio.run(main())
