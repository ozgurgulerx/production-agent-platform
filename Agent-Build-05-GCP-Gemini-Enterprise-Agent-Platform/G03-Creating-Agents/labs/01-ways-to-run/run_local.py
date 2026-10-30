"""Way 1: the Runner in your own process. Two turns, InMemorySessionService, events printed (B5).

Run:  python run_local.py        (from 01-ways-to-run, shared venv active, .env at the track root)
Proof: turn 2 refuses the out-of-policy refund and cites the policy document.
"""

from __future__ import annotations

import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from ticket_agent.agent import root_agent

APP_NAME = "ticket-agent"
USER_ID = "customer-1"
SESSION_ID = "local-1"

TURNS = [
    "My card was charged twice for order 8841. Ticket 1042.",
    "Can you also refund £80 as a goodwill gesture for the inconvenience?",
]


async def main() -> None:
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=InMemorySessionService(),
        auto_create_session=True,  # B5
    )
    for text in TURNS:
        print(f"\n> {text}")
        message = types.Content(role="user", parts=[types.Part(text=text)])
        async for event in runner.run_async(
            user_id=USER_ID, session_id=SESSION_ID, new_message=message
        ):
            # TODO(learner): print function calls (event.get_function_calls()) and the final text
            # (event.is_final_response()) so the proof checklist can be ticked from this output alone.
            pass


if __name__ == "__main__":
    asyncio.run(main())
