"""G03 section 2: the ways to run one `root_agent`, as a table in code. Untested sketch, not a program.

Each entry names the host, what the definition is, where the loop runs, whether a `ReasoningEngine`
resource exists, and the map letter. The commands are the ones on the cited pages; nothing here runs.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Way:
    n: int
    name: str
    definition_lives: str
    loop_runs: str
    resource: str  # "none" | "Cloud Run service" | "ReasoningEngine"
    command: str
    status: str
    map_ref: str


WAYS = [
    Way(
        1,
        "Runner in code",
        "agent.py",
        "your process",
        "none",
        "python run_local.py",
        "GA (ADK 2.13.0)",
        "B5",
    ),
    Way(
        2,
        "adk web / adk run",
        "agent.py",
        "your process",
        "none",
        "adk web --port 8000 ; adk run ticket_agent --save_session",
        "GA",
        "B6",
    ),
    Way(
        3,
        "adk api_server",
        "agent.py",
        "your process (REST)",
        "none",
        "adk api_server --a2a --with_ui",
        "GA",
        "B6",
    ),
    Way(
        4,
        "Cloud Run",
        "agent.py in your container",
        "Cloud Run",
        "Cloud Run service",
        "adk deploy cloud_run --project P --region L --service_name ticket-agent --with_ui ticket_agent",
        "GA",
        "B7",
    ),
    Way(
        5,
        "Agent Runtime via CLI",
        "agent.py packaged by the CLI",
        "Agent Runtime",
        "ReasoningEngine",
        "adk deploy agent_engine --project P --region L --display_name ticket-agent --otel_to_cloud ticket_agent",
        "GA",
        "C2, C3",
    ),
    Way(
        6,
        "Agent Runtime via SDK",
        "agent.py, pickled or from source",
        "Agent Runtime",
        "ReasoningEngine",
        "agentplatform.Client().runtimes.create(agent=app, config={...})",
        "GA (vertexai.agent_engines legacy)",
        "A5, I7",
    ),
    Way(
        7,
        "Custom container",
        "Dockerfile or image in Artifact Registry",
        "Agent Runtime",
        "ReasoningEngine",
        "runtimes.create(config={'container_spec': {'image_uri': ...}, 'agent_framework': 'custom'})",
        "GA (2026-04-22); container contract unverified",
        "A2, A5, I7",
    ),
    Way(
        8,
        "Agent Garden via Agents CLI",
        "Google sample, then yours",
        "Agent Runtime",
        "ReasoningEngine",
        "uvx google-agents-cli create ... ; agents-cli deploy --agent-identity",
        "Agent Garden preview (2026-10-22)",
        "A7, I12, C5",
    ),
    Way(
        9,
        "Registered in Gemini Enterprise",
        "the ReasoningEngine from 5 or 6",
        "Agent Runtime",
        "ReasoningEngine",
        "POST .../engines/APP_ID/assistants/default_assistant/agents  (adkAgentDefinition.provisionedReasoningEngine)",
        "GA",
        "C8",
    ),
]


def governable(way: Way) -> bool:
    """Revisions, Agent Identity and Gemini Enterprise registration all hang off the resource path (C4, C5, C8)."""
    return way.resource == "ReasoningEngine"


if __name__ == "__main__":
    for w in WAYS:
        print(
            f"{w.n}. {w.name:34} resource={w.resource:18} governable={governable(w)!s:5} [{w.map_ref}]"
        )
    # TODO(learner): add a column for "can be an A2A target" (C7, C10) and check which ways qualify.
