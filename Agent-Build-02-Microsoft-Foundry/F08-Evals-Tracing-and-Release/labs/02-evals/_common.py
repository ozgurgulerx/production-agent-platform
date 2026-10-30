"""Shared bits for the evals folder. Uses its own venv (azure-ai-projects>=2.9)."""
import os
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=False) or find_dotenv(usecwd=True))  # .env at the track root (walks up)
PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"].rstrip("/")
MODEL = os.environ.get("FOUNDRY_MODEL", "gpt-5-mini")
EVAL_MODEL = os.environ.get("FOUNDRY_EVAL_MODEL", MODEL)       # judge model deployment
AGENT_NAME = os.environ.get("EVAL_AGENT_NAME", "ticket-agent-prompt")   # any agent: prompt (01), hosted (02), workflow (12)
AGENT_VERSION = os.environ.get("EVAL_AGENT_VERSION")              # None = latest
DATASET = Path(__file__).parent / "data" / "ticket_queries.jsonl"


def project_client(**kw) -> AIProjectClient:
    return AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential(), **kw)


def agent_version(project: AIProjectClient) -> str:
    return AGENT_VERSION or str(project.agents.get(agent_name=AGENT_NAME).versions.latest.version)
