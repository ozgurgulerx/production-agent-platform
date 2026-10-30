"""sdk_map.py: which package owns which call, old surface next to new (map A5, C1, C2, A2).

Runnable shape, not a program: `python sdk_map.py` prints the import map and exits. Nothing is
deployed. The one place in this track where the old `vertexai.agent_engines` surface is shown.
Status 25 Oct 2026: scaffold only, functionality unverified.
"""

from __future__ import annotations

import importlib
import os

from dotenv import load_dotenv

load_dotenv()  # walks up to the track-root .env (labs-setup)

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]

# Package -> (import you actually write, what it is for). Pins from map "Pinned versions".
SDK_MAP = {
    "google-adk": (
        "from google.adk.agents import LlmAgent; from google.adk.runners import Runner",
        "agent code, adk CLI",
    ),
    "google-cloud-agentplatform": (
        "from google.cloud import agentplatform  # Client().runtimes",
        "deploy, revisions, sessions, memory_banks (A5)",
    ),
    "google-cloud-aiplatform": (
        "import vertexai  # vertexai.agent_engines, legacy",
        "pinned only because adk deploy writes it (C2)",
    ),
    "google-genai": (
        "from google import genai  # Client().models / .tunings",
        "model calls, tuning jobs (G4)",
    ),
}


def show_map() -> None:
    for pkg, (imp, job) in SDK_MAP.items():
        print(f"{pkg:28} {job}\n{'':28} {imp}")


def has_runtimes_surface() -> bool:
    """Mirror the check adk deploy performs: it needs client.runtimes, not agent_engines (C2).

    TODO(learner): instantiate agentplatform.Client(project=PROJECT, location=LOCATION) and return
    hasattr(client, "runtimes"). Keep it import-guarded so the sketch prints on a bare machine.
    """
    try:
        importlib.import_module("google.cloud.agentplatform")
    except ImportError:
        return False
    raise NotImplementedError("TODO(learner)")


def old_surface_for_contrast() -> str:
    """The pre-2.0.1 call, kept for reading only (C1). Do not use in new code."""
    return (
        "vertexai.Client(project=P, location=L).agent_engines.create("
        "agent=AdkApp(agent=root_agent), config={'requirements': [...], 'staging_bucket': 'gs://...',"
        " 'identity_type': types.IdentityType.AGENT_IDENTITY})"
    )


def new_surface() -> str:
    """The 2.x call (A5, I7). `agentplatform.frameworks.AdkApp` import is unverified (map Gaps)."""
    return (
        "agentplatform.Client(project=P, location=L, http_options=dict(api_version='v1beta1'))"
        ".runtimes.create(agent=app, config={'requirements': [...], 'identity_type': 'AGENT_IDENTITY',"
        " 'agent_framework': 'google-adk', 'env_vars': {...}})"
    )


if __name__ == "__main__":
    show_map()
    print("\nold:", old_surface_for_contrast())
    print("new:", new_surface())
