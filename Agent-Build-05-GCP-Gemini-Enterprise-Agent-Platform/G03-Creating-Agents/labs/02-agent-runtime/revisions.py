"""Revisions and traffic on AGENT_RUNTIME_RESOURCE. Preview (v1beta1) on 25 Oct 2026 (C4).

    python revisions.py list
    python revisions.py pin <revision-id>     # trafficSplitManual, 100 % to that ACTIVE revision = rollback
    python revisions.py latest                # trafficSplitAlwaysLatest (default)
    python revisions.py delete <revision-id>  # archived, unrecoverable (C4)

Facts (C4): a revision is created on create and on every versioned-field change; there is no rollback verb;
changing an Agent Gateway binding archives prior revisions. Limits (A10): 950 per agent, 6,000 per
project-region, not adjustable. Methods: client.runtimes.revisions.list/get/delete and
client.runtimes.update(traffic_config=...). The traffic_config payload shape is unverified.
"""

from __future__ import annotations

import os
import sys

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))
RESOURCE = os.environ["AGENT_RUNTIME_RESOURCE"]


def client():
    from google.cloud import agentplatform

    return agentplatform.Client(
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location=os.environ["GOOGLE_CLOUD_LOCATION"],
        http_options={"api_version": "v1beta1"},
    )


def list_revisions(c):
    # TODO(learner): for r in c.runtimes.revisions.list(name=RESOURCE): print id, state (active/archived), create time
    raise NotImplementedError


def pin(c, revision_id: str):
    # TODO(learner): c.runtimes.update(name=RESOURCE, traffic_config={...manual, 100 % to revision_id...})  # shape unverified
    raise NotImplementedError


def latest(c):
    # TODO(learner): c.runtimes.update(name=RESOURCE, traffic_config={...always latest...})
    raise NotImplementedError


def delete_revision(c, revision_id: str):
    # TODO(learner): c.runtimes.revisions.delete(...). Refuse if it currently receives traffic.
    raise NotImplementedError


if __name__ == "__main__":
    c = client()
    cmd, *args = sys.argv[1:] or ["list"]
    {
        "list": lambda: list_revisions(c),
        "pin": lambda: pin(c, args[0]),
        "latest": lambda: latest(c),
        "delete": lambda: delete_revision(c, args[0]),
    }[cmd]()
