"""traffic_split.py: get-or-create, deploy a revision, split traffic, roll back, prune (map C4, A10, I7).

Revisions and traffic are preview on 22 Oct 2026 (v1beta1). Rollback is a manual split to an earlier
active revision; there is no rollback verb. 950 revisions per agent is a hard cap.

    python traffic_split.py deploy  --agent-dir ../labs/01-deploy-pipeline
    python traffic_split.py split   --new 10
    python traffic_split.py promote
    python traffic_split.py rollback
    python traffic_split.py prune   --keep 20

Status 25 Oct 2026: scaffold only, functionality unverified. Method names follow C4 and I7; the
exact `traffic_config` schema was not in the fetched page body, so it is marked unverified below.
"""

from __future__ import annotations

import argparse
import os

from dotenv import load_dotenv

load_dotenv()

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]
DISPLAY_NAME = "ticket-agent"
REVISION_CAP = 950  # A10, not adjustable


def client():
    """agentplatform client on v1beta1 (needed for Agent Identity and revisions, C5, C4)."""
    from google.cloud import agentplatform  # 2.6.0

    return agentplatform.Client(
        project=PROJECT, location=LOCATION, http_options=dict(api_version="v1beta1")
    )


def get_or_create(c, agent_dir: str):
    """Return the existing `ticket-agent` by display_name, else create it (labs-setup rule).

    TODO(learner): list c.runtimes, match display_name == DISPLAY_NAME; on miss build the AdkApp from
    agent_dir and call c.runtimes.create(agent=app, config=base_config()). Prefer AGENT_RUNTIME_RESOURCE
    from .env when set, and warn if the two disagree.
    """
    raise NotImplementedError("TODO(learner)")


def base_config() -> dict:
    """The I7 keys the lab sets. Everything else stays default."""
    return {
        "requirements": open(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "labs",
                "01-deploy-pipeline",
                "requirements.txt",
            )
        )
        .read()
        .splitlines(),
        "env_vars": {
            "GOOGLE_GENAI_USE_VERTEXAI": "TRUE",
            "TICKET_MCP_URL": os.environ.get("TICKET_MCP_URL", ""),
        },
        "identity_type": "AGENT_IDENTITY",  # C5; unset would mean a service account
        "agent_framework": "google-adk",
    }


def deploy(c, agent_dir: str):
    """New revision on an existing resource: runtimes.update(name, config) (C2 does the same)."""
    rt = get_or_create(c, agent_dir)
    # TODO(learner): c.runtimes.update(name=rt.name, agent=app, config=base_config())
    raise NotImplementedError("TODO(learner)")


def list_revisions(c, name: str) -> list:
    """c.runtimes.revisions.list(parent=name) (C4). Return newest first."""
    raise NotImplementedError("TODO(learner)")


def split(c, name: str, new_pct: int) -> None:
    """Manual split: newest revision gets new_pct, previous active gets the rest (C4).

    TODO(learner): c.runtimes.update(name=name, traffic_config=...). The traffic_config shape is
    unverified in the map; read C4 before writing it. Mode must be trafficSplitManual.
    """
    raise NotImplementedError("TODO(learner)")


def promote(c, name: str) -> None:
    """100 percent to newest, or switch back to trafficSplitAlwaysLatest (C4)."""
    split(c, name, 100)


def rollback(c, name: str) -> None:
    """Send traffic to the previous active revision. No redeploy (C4)."""
    split(c, name, 0)


def prune(c, name: str, keep: int) -> None:
    """Delete inactive revisions beyond `keep`; archived revisions are unrecoverable (C4, A10).

    TODO(learner): never delete a revision that carries traffic; stop when len(revisions) <= keep.
    """
    raise NotImplementedError("TODO(learner)")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["deploy", "split", "promote", "rollback", "prune"])
    p.add_argument(
        "--agent-dir",
        default=os.path.join(
            os.path.dirname(__file__), "..", "labs", "01-deploy-pipeline"
        ),
    )
    p.add_argument("--new", type=int, default=10)
    p.add_argument("--keep", type=int, default=20)
    a = p.parse_args()
    c = client()
    name = os.environ.get("AGENT_RUNTIME_RESOURCE", "")
    if a.cmd == "deploy":
        deploy(c, a.agent_dir)
    elif a.cmd == "split":
        split(c, name, a.new)
    elif a.cmd == "promote":
        promote(c, name)
    elif a.cmd == "rollback":
        rollback(c, name)
    else:
        prune(c, name, a.keep)
