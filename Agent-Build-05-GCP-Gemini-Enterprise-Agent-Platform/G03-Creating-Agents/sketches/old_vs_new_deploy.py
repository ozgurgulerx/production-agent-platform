"""G03 way 6: the same deploy on the old and the new SDK surface. Untested sketch.

OLD  vertexai.agent_engines (C1): broken for new code by SDK 2.0.1 on 2026-09-18, which moved agents into
     google-cloud-agentplatform (A2). Shown once, here, and nowhere else in the track.
NEW  agentplatform.Client().runtimes (A5, I7): `runtimes`, `sessions`, `sandboxes`, `memory_banks`.
     `adk deploy agent_engine` calls exactly this (C2).
"""

from __future__ import annotations

import os

from ticket_agent.agent import root_agent  # the one definition every way shares

P = os.environ["GOOGLE_CLOUD_PROJECT"]
L = os.environ["GOOGLE_CLOUD_LOCATION"]
BUCKET = os.environ["AGENT_RUNTIME_STAGING_BUCKET"]
REQUIREMENTS = [
    "google-cloud-aiplatform[adk,agent_engines]>=2.2,<3",
    "google-adk[a2a]==2.13.0",
]  # what the CLI writes (C2)


def deploy_old_surface():
    """LEGACY. `pip install google-cloud-aiplatform[agent_engines,adk]>=1.112` era (C1). Do not copy."""
    import vertexai
    from vertexai import agent_engines, types

    app = agent_engines.AdkApp(agent=root_agent)
    client = vertexai.Client(project=P, location=L)
    engine = client.agent_engines.create(
        agent=app,
        config={
            "requirements": REQUIREMENTS,
            "staging_bucket": BUCKET,
            "identity_type": types.IdentityType.AGENT_IDENTITY,
        },
    )
    # async_stream_query(user_id, message) to call; delete(force=True) to remove (C1)
    return engine


def deploy_new_surface():
    """CURRENT. `google-cloud-agentplatform` 2.6.0 (A5, I7). `.agent_engine_config.json` is the CLI's view of `config`."""
    from google.cloud import agentplatform
    from agentplatform.frameworks import (
        AdkApp,
    )  # page not fetched on 25 Oct 2026: import path and kwargs unverified

    app = AdkApp(agent=root_agent)  # unverified constructor
    client = agentplatform.Client(
        project=P, location=L, http_options={"api_version": "v1beta1"}
    )  # v1beta1 for identity_type (C5)
    runtime = client.runtimes.create(
        agent=app,
        config={
            "display_name": "ticket-agent",
            "requirements": REQUIREMENTS,
            "extra_packages": ["ticket_agent"],
            "env_vars": {
                "GOOGLE_GENAI_USE_VERTEXAI": "TRUE",
                "GEMINI_MODEL": os.environ["GEMINI_MODEL"],
            },
            "identity_type": "AGENT_IDENTITY",
            "agent_framework": "google-adk",
            "gcs_dir_name": "ticket-agent",
        },
    )
    # later: client.runtimes.update(name, config) for a new revision; client.runtimes.update(traffic_config=...) to
    # move traffic; client.runtimes.revisions.list/get/delete (C4); delete(force=True) (C1).
    return runtime


if __name__ == "__main__":
    # TODO(learner): run deploy_new_surface() only. Print `runtime.name` and write it to .env as AGENT_RUNTIME_RESOURCE.
    pass
