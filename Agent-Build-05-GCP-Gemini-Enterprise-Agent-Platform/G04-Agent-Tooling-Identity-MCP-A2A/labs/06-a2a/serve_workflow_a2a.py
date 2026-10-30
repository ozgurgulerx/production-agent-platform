"""Serve the workflow agent over A2A on port 8001 with to_a2a (map C7). Card at /.well-known/agent-card.json.
Status: scaffold only, functionality unverified."""
import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))

from google.adk.a2a.utils.agent_to_a2a import to_a2a  # noqa: E402

try:  # prefer the real G03 workflow agent when the chapter exists
    from G03_workflow import root_agent  # TODO(learner): import path to G03 lab 03's agent
except ImportError:
    from workflow_agent import root_agent

app = to_a2a(root_agent, port=8001)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
