"""Call AGENT_RUNTIME_RESOURCE through :query and :streamQuery (C3) with ADC.

    python query.py "My card was charged twice for order 8841. Ticket 1042."

REST form, from the deploy page (C3):
  POST https://{L}-aiplatform.googleapis.com/v1/projects/{P}/locations/{L}/reasoningEngines/{ID}:query
  POST .../reasoningEngines/{ID}:streamQuery
The request body for an ADK agent is not on a fetched page; the keys below follow the old quickstart's
`async_stream_query(user_id, message)` (C1) and are unverified.
"""

from __future__ import annotations

import os
import sys

import google.auth
import google.auth.transport.requests
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))

RESOURCE = os.environ[
    "AGENT_RUNTIME_RESOURCE"
]  # projects/P/locations/L/reasoningEngines/ID
LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]
BASE = f"https://{LOCATION}-aiplatform.googleapis.com/v1/{RESOURCE}"


def token() -> str:
    creds, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    creds.refresh(google.auth.transport.requests.Request())
    return creds.token


def query(message: str, user_id: str = "customer-1") -> dict:
    body = {
        "class_method": "async_stream_query",
        "input": {"user_id": user_id, "message": message},
    }  # unverified
    # TODO(learner): POST to f"{BASE}:query" with Authorization: Bearer token(); return r.json()
    raise NotImplementedError


def stream_query(message: str, user_id: str = "customer-1"):
    # TODO(learner): POST to f"{BASE}:streamQuery?alt=sse" (parameter unverified) with stream=True and yield lines
    raise NotImplementedError


if __name__ == "__main__":
    text = (
        sys.argv[1] if len(sys.argv) > 1 else "Ticket 1042: my card was charged twice."
    )
    print(query(text))
