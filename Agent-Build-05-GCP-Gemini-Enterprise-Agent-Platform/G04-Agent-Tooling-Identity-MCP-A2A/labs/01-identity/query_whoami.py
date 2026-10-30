"""Call :query on a deployed reasoning engine and print the whoami tool result (map C3, A5).
Usage: python query_whoami.py <REASONING_ENGINE_ID>. Status: scaffold only, functionality unverified."""
import os
import sys

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))


def main(engine_id: str) -> None:
    # TODO(learner): from agentplatform import Client (google-cloud-agentplatform 2.6.0, map A5);
    # client.runtimes.get(name=f"projects/{P}/locations/{L}/reasoningEngines/{engine_id}");
    # stream_query(user_id="lab01", message="Who are you running as?") and print every tool response event.
    raise SystemExit("TODO(learner): implement query_whoami")


if __name__ == "__main__":
    main(sys.argv[1])
