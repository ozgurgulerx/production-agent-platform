"""Way 6: deploy ticket-agent to Agent Runtime with the new SDK surface, get-or-create by display_name.

    python deploy_sdk.py                    # reuse or create ticket-agent, write AGENT_RUNTIME_RESOURCE into .env
    python deploy_sdk.py --delete <name>    # delete(force=True) a throwaway copy (C1)

Surface: `agentplatform.Client().runtimes` from google-cloud-agentplatform 2.6.0 (A5, I7). The old
`vertexai.agent_engines` surface appears once in ../../sketches/old_vs_new_deploy.py and nowhere else.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import find_dotenv, load_dotenv, set_key

ENV_PATH = find_dotenv(usecwd=True)
load_dotenv(ENV_PATH)

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]
DISPLAY_NAME = "ticket-agent"
REQUIREMENTS = [
    "google-cloud-aiplatform[adk,agent_engines]>=2.2,<3",
    "google-adk[a2a]==2.13.0",
]  # what the CLI writes (C2)


def client():
    from google.cloud import agentplatform

    # v1beta1 is required for identity_type=AGENT_IDENTITY (C5)
    return agentplatform.Client(
        project=PROJECT, location=LOCATION, http_options={"api_version": "v1beta1"}
    )


def find_by_display_name(c, display_name: str):
    """Return the existing runtime with this display_name, or None.

    REST has projects.locations.reasoningEngines.list (I10). The SDK spelling of the list call is not on a
    fetched page; `c.runtimes.list()` is assumed, unverified.
    """
    # TODO(learner): iterate c.runtimes.list() and match on display_name; return the first match.
    raise NotImplementedError


def create(c):
    from agentplatform.frameworks import (
        AdkApp,
    )  # import path unverified (page not fetched on 25 Oct 2026)

    from ticket_agent.agent import root_agent

    app = AdkApp(agent=root_agent)  # constructor kwargs unverified
    config = {
        "display_name": DISPLAY_NAME,
        "requirements": REQUIREMENTS,
        "extra_packages": ["ticket_agent"],
        "env_vars": {
            "GOOGLE_GENAI_USE_VERTEXAI": "TRUE",
            "GEMINI_MODEL": os.environ["GEMINI_MODEL"],
        },
        "identity_type": "AGENT_IDENTITY",  # C5
        "agent_framework": "google-adk",  # I7
        "gcs_dir_name": DISPLAY_NAME,
    }
    # TODO(learner): return c.runtimes.create(agent=app, config=config) and print its .name
    raise NotImplementedError


def write_env(resource_name: str) -> None:
    """Write AGENT_RUNTIME_RESOURCE=projects/P/locations/L/reasoningEngines/ID into the track-root .env."""
    set_key(ENV_PATH, "AGENT_RUNTIME_RESOURCE", resource_name)
    print(f"[env] AGENT_RUNTIME_RESOURCE={resource_name} written to {Path(ENV_PATH)}")


def delete(c, display_name: str) -> None:
    # TODO(learner): find_by_display_name, then runtime.delete(force=True) (C1). Note D10: a recreate is a new principal.
    raise NotImplementedError


if __name__ == "__main__":
    c = client()
    if len(sys.argv) == 3 and sys.argv[1] == "--delete":
        delete(c, sys.argv[2])
        sys.exit(0)
    existing = find_by_display_name(c, DISPLAY_NAME)
    if existing is not None:
        print(f"[get-or-create] reusing {DISPLAY_NAME}: {existing.name}")
        runtime = existing
    else:
        runtime = create(c)
        print(f"[get-or-create] created {DISPLAY_NAME}: {runtime.name}")
    write_env(runtime.name)
