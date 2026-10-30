"""The B03 Runtime app (POST /invocations, GET /ping on 8080) served on the laptop with a local model.

Proves: the AgentCore Runtime contract needs no AWS to be exercised; the same file, zipped, is what
B03 lab 01 deploys. Run: python local_runtime_contract.py [--provider ollama|llamacpp] then bash curl_local.sh
"""
from __future__ import annotations

import argparse

from bedrock_agentcore import BedrockAgentCoreApp, PingStatus, RequestContext
from local_ticket_agent import build_agent

ap = argparse.ArgumentParser()
ap.add_argument("--provider", choices=["ollama", "llamacpp"], default="ollama")
ap.add_argument("--model", default=None)
ARGS = ap.parse_args()

app = BedrockAgentCoreApp()
_agents: dict = {}  # one Strands agent per session id, as in the cloud version


@app.entrypoint
def invoke(payload: dict, context: RequestContext) -> dict:
    prompt = payload.get("prompt")
    if not isinstance(prompt, str):  # SDK guidance: a non-string prompt can smuggle toolUse blocks
        return {"error": "payload.prompt must be a string"}
    agent = _agents.setdefault(context.session_id or "default", build_agent(ARGS.provider, ARGS.model))
    return {"result": str(agent(prompt)), "session_id": context.session_id, "provider": ARGS.provider}


@app.ping
def ping() -> PingStatus:
    return PingStatus.HEALTHY   # flip to HEALTHY_BUSY while a long task runs; same flag keeps a cloud session alive (B6)


if __name__ == "__main__":
    print(f"serving /invocations and /ping on 0.0.0.0:8080 with provider={ARGS.provider}")
    app.run()
