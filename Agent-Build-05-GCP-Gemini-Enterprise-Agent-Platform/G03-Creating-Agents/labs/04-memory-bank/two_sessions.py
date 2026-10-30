"""Two sessions, one user: does session B know what session A was told?

    python two_sessions.py --sessions-only    # VertexAiSessionService only (B5): expect "do not know"
    python two_sessions.py --with-memory      # + Memory Bank: expect "SMS"

Both services hang off AGENT_RUNTIME_RESOURCE (B5). Kwarg names and the Memory Bank service class are
unverified on 25 Oct 2026; confirm on adk.dev before running.
"""

from __future__ import annotations

import asyncio
import os
import sys

from dotenv import find_dotenv, load_dotenv
from google.adk.runners import Runner
from google.genai import types

from agent import root_agent

load_dotenv(find_dotenv(usecwd=True))
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]
RESOURCE = os.environ["AGENT_RUNTIME_RESOURCE"]
ENGINE_ID = RESOURCE.rsplit("/", 1)[-1]
APP_NAME = "ticket-agent"
USER_ID = "customer-memory-1"


def build_runner(with_memory: bool) -> Runner:
    from google.adk.sessions import VertexAiSessionService

    session_service = VertexAiSessionService(
        project=PROJECT, location=LOCATION, agent_engine_id=ENGINE_ID
    )  # kwargs unverified
    memory_service = None
    if with_memory:
        # TODO(learner): import and construct the Memory Bank memory service (class name unverified) for the same
        # resource, and pass it as memory_service=. On Cloud Run the equivalent is --memory_service_uri (B7); inside
        # the Agent Runtime container it is already wired via agentengine:// (C2).
        raise NotImplementedError("Memory Bank service class unverified on 25 Oct 2026")
    return Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )


async def turn(runner: Runner, session_id: str, text: str) -> str:
    content = types.Content(role="user", parts=[types.Part(text=text)])
    final = ""
    async for event in runner.run_async(
        user_id=USER_ID, session_id=session_id, new_message=content
    ):
        # TODO(learner): collect the final response text into `final`
        pass
    return final


async def main(with_memory: bool) -> None:
    runner = build_runner(with_memory)
    # TODO(learner): create session A and B through runner.session_service (or auto_create_session=True, B5)
    a = await turn(
        runner, "session-a", "For ticket 1042, please contact me by SMS from now on."
    )
    # TODO(learner): if the integration requires it, add session A to memory here before starting session B.
    b = await turn(runner, "session-b", "Which channel should you use to contact me?")
    print(f"[A] {a}\n[B] {b}")


if __name__ == "__main__":
    asyncio.run(main(with_memory="--with-memory" in sys.argv))
