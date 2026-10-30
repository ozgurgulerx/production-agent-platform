"""Enable the Activity protocol endpoint on a Foundry prompt agent so Copilot Studio can add it as a connected agent.

Proves: the 400 from the Connected agents dialog is a Foundry-side switch (reading map B4), set through the
Foundry project REST API, not the portal. Reads the Foundry track's .env read-only when present, otherwise
FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_AGENT_NAME. Auth: DefaultAzureCredential (az login). The exact request
path and body are taken from the Learn page and marked verify until run.
"""
import argparse
import os
from pathlib import Path

import httpx
from azure.identity import DefaultAzureCredential
from dotenv import dotenv_values

from _common import _TRACK_ROOT, show

FOUNDRY_ENV = _TRACK_ROOT.parent / "Agent-Build-02-Microsoft-Foundry" / ".env"   # read-only, if the Foundry track is set up
API_VERSION = "2026-10-01-preview"          # verify: api-version on the "enable Activity protocol" page (B4)
SCOPE = "https://ai.azure.com/.default"


def settings() -> tuple[str, str]:
    vals = dotenv_values(FOUNDRY_ENV) if FOUNDRY_ENV.exists() else {}
    endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT") or vals.get("FOUNDRY_PROJECT_ENDPOINT", "")
    name = os.environ.get("FOUNDRY_AGENT_NAME") or vals.get("FOUNDRY_AGENT_NAME", "ticket-agent-prompt")
    if not endpoint:
        raise SystemExit("set FOUNDRY_PROJECT_ENDPOINT (or set up the Foundry track .env)")
    return endpoint.rstrip("/"), name


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--disable", action="store_true")
    a = ap.parse_args()
    endpoint, name = settings()
    token = DefaultAzureCredential().get_token(SCOPE).token
    h = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    with httpx.Client(timeout=60) as c:
        cur = c.get(f"{endpoint}/agents/{name}?api-version={API_VERSION}", headers=h)
        show("agent", {"status": cur.status_code, "protocols": cur.json().get("protocols") if cur.status_code < 400 else cur.text[:200]})
        # verify: field name. The page describes enabling the "activity" protocol endpoint alongside "responses".
        body = {"protocols": ["responses"] if a.disable else ["responses", "activity"]}
        r = c.patch(f"{endpoint}/agents/{name}?api-version={API_VERSION}", headers=h, json=body)
        show("patch", {"status": r.status_code, "body": r.text[:300]})
        if r.status_code < 400:
            print(f"\nActivity endpoint {'disabled' if a.disable else 'enabled'} on {name}. "
                  "Now add the agent in Copilot Studio → Connected agents → Foundry agent with the project endpoint and agent id.")
        else:
            print("\nIf 404/400: confirm the agent was created in the new Foundry portal (legacy agents are not eligible, B4).")


if __name__ == "__main__":
    main()
