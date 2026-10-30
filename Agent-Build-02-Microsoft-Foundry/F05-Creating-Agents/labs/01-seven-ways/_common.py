"""Shared helpers for the 01 scripts: env loading, project client, agent get-or-create, cleanup."""
from __future__ import annotations

import os
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=False) or find_dotenv(usecwd=True))  # .env at the track root (walks up)

PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"].rstrip("/")
MODEL = os.environ.get("FOUNDRY_MODEL", "gpt-5-mini")

SUPPORT_INSTRUCTIONS = (
    "You are the support-ticket assistant for a UK bank's card team. "
    "Answer briefly. When you do not have a tool for something, say so instead of guessing."
)


def project_client(**kwargs) -> AIProjectClient:
    """One client per script. `allow_preview=True` is only needed for preview surfaces (voice)."""
    return AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential(), **kwargs)


def get_or_create(project: AIProjectClient, agent_name: str, definition):
    """Return the existing agent if it exists, else create version 1.

    The docs say to treat 404 as terminal: `get` raising ResourceNotFoundError means
    the agent does not exist, so we create it. Anything else is a real error.
    Every `create_version` call adds an immutable version (cap 1,000 per agent), so
    scripts must not call it unconditionally on each run.
    """
    try:
        agent = project.agents.get(agent_name=agent_name)
        print(f"[get-or-create] reusing '{agent.name}' (latest version {agent.versions.latest.version})")
        return agent
    except ResourceNotFoundError:
        version = project.agents.create_version(agent_name=agent_name, definition=definition)
        print(f"[get-or-create] created '{version.name}' version {version.version}")
        return project.agents.get(agent_name=agent_name)


def delete_agent(project: AIProjectClient, agent_name: str) -> None:
    try:
        project.agents.delete(agent_name=agent_name)
        print(f"[cleanup] deleted '{agent_name}' and all its versions")
    except ResourceNotFoundError:
        pass
