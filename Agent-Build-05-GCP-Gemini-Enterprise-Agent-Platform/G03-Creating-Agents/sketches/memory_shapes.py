"""G03 section 5: three session/memory shapes for the same Runner. Untested sketch.

- tests: InMemorySessionService (B5)
- one conversation on the platform: VertexAiSessionService, needs an Agent Runtime resource (B5)
- across conversations: Memory Bank, wired by URI on Cloud Run (`--memory_service_uri`, B7) and by
  `agentengine://` inside the Agent Runtime container (C2). The ADK class name for the Memory Bank
  service is on no fetched page and is marked unverified below.
Sessions and Memory Bank: GA on us/eu/global since 2026-06-17 (A2); 100 session writes, 100 memory writes,
300 memory reads per minute (A10).
"""

from __future__ import annotations

import os

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

APP = "ticket-agent"
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
RESOURCE = os.environ.get(
    "AGENT_RUNTIME_RESOURCE", ""
)  # projects/P/locations/L/reasoningEngines/ID

root_agent = Agent(
    name="ticket_agent",
    model=MODEL,
    instruction="Support-ticket assistant. Remember the customer's preferred contact channel.",
)


def runner_for_tests() -> Runner:
    """Shape 1: everything in memory; `auto_create_session=True` saves a create_session call (B5)."""
    return Runner(
        agent=root_agent,
        app_name=APP,
        session_service=InMemorySessionService(),
        auto_create_session=True,
    )


def runner_with_platform_sessions() -> Runner:
    """Shape 2: Sessions on the platform. `google-adk[gcp]`; the service needs the Agent Runtime resource (B5)."""
    from google.adk.sessions import VertexAiSessionService

    session_service = VertexAiSessionService(
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location=os.environ["GOOGLE_CLOUD_LOCATION"],
        agent_engine_id=RESOURCE.rsplit("/", 1)[
            -1
        ],  # kwarg name unverified; check the B5 page
    )
    return Runner(agent=root_agent, app_name=APP, session_service=session_service)


def runner_with_memory_bank() -> Runner:
    """Shape 3: Memory Bank across conversations.

    On Cloud Run:      adk deploy cloud_run ... --memory_service_uri agentengine://<ID>   (B7)
    On Agent Runtime:  the container already runs api_server with agentengine:// session and memory URIs (C2)
    In code:           the memory service class is unverified (no fetched page names it).
    """
    # TODO(learner): import the Memory Bank memory service once you have confirmed its name on adk.dev,
    # pass it as `memory_service=` to the Runner, and ensure the agent calls the memory tool on turn one of
    # a new session. Proof: session B answers "preferred channel?" correctly after session A set it.
    raise NotImplementedError("memory service class unverified on 25 Oct 2026")
