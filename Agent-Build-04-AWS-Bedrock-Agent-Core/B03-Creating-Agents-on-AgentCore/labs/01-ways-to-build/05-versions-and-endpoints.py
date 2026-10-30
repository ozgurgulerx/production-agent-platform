"""Versions and endpoints. Every UpdateAgentRuntime creates an immutable version (V1, V2, ...).
DEFAULT always tracks the latest version. A custom endpoint is a pointer you move: pin it to
V1, promote to V2, roll back to V1. There is no weighted split at the Runtime; A/B lives in
Gateway rules and Optimization (B2/B3 in the reading map).
Usage: python 05-versions-and-endpoints.py [--keep]   (needs TICKET_AGENT_RUNTIME_ARN)
"""
from __future__ import annotations

import argparse
import os
import time

from _common import control, require

require("TICKET_AGENT_RUNTIME_ARN", "AGENTCORE_RUNTIME_ROLE_ARN")
cp = control()
runtime_id = os.environ["TICKET_AGENT_RUNTIME_ARN"].rsplit("/", 1)[-1]


def wait(fn, key="status", ok=("READY",), **kw):
    while True:
        r = fn(**kw)
        if r[key] in ok:
            return r
        if "FAIL" in r[key]:
            raise SystemExit(r)
        time.sleep(8)


current = cp.get_agent_runtime(agentRuntimeId=runtime_id)
print("current version:", current["agentRuntimeVersion"], "platform:", current.get("platformVersion"))

# 1. a new version: same artifact, one env var changed (any update mints a version)
env = dict(current.get("environmentVariables", {}), AGENT_FLAVOUR="v2-tone")
cp.update_agent_runtime(
    agentRuntimeId=runtime_id, agentRuntimeArtifact=current["agentRuntimeArtifact"], roleArn=current["roleArn"],
    networkConfiguration=current["networkConfiguration"], protocolConfiguration=current.get("protocolConfiguration", {"serverProtocol": "HTTP"}),
    environmentVariables=env,
)
latest = wait(cp.get_agent_runtime, agentRuntimeId=runtime_id)
print("new version:", latest["agentRuntimeVersion"])

versions = [v["agentRuntimeVersion"] for v in cp.list_agent_runtime_versions(agentRuntimeId=runtime_id)["agentRuntimes"]]
print("versions:", versions)
v1, v2 = sorted(versions, key=int)[0], latest["agentRuntimeVersion"]

# 2. a pinned endpoint: `stable` -> V1 while DEFAULT already serves V2
names = {e["name"] for e in cp.list_agent_runtime_endpoints(agentRuntimeId=runtime_id)["runtimeEndpoints"]}
if "stable" not in names:
    cp.create_agent_runtime_endpoint(agentRuntimeId=runtime_id, name="stable", agentRuntimeVersion=v1)
ep = wait(cp.get_agent_runtime_endpoint, agentRuntimeId=runtime_id, endpointName="stable")
print("stable ->", ep["liveVersion"], "| DEFAULT ->", cp.get_agent_runtime_endpoint(agentRuntimeId=runtime_id, endpointName="DEFAULT")["liveVersion"])

# 3. promote, then roll back: the endpoint is the only thing that moves
cp.update_agent_runtime_endpoint(agentRuntimeId=runtime_id, endpointName="stable", agentRuntimeVersion=v2)
print("promoted stable ->", wait(cp.get_agent_runtime_endpoint, agentRuntimeId=runtime_id, endpointName="stable")["liveVersion"])
cp.update_agent_runtime_endpoint(agentRuntimeId=runtime_id, endpointName="stable", agentRuntimeVersion=v1)
print("rolled back stable ->", wait(cp.get_agent_runtime_endpoint, agentRuntimeId=runtime_id, endpointName="stable")["liveVersion"])

ap = argparse.ArgumentParser()
ap.add_argument("--keep", action="store_true", help="leave `stable` so 04-invoke-everything.py can call it")
if not ap.parse_args().keep:
    cp.delete_agent_runtime_endpoint(agentRuntimeId=runtime_id, endpointName="stable")
    print("deleted endpoint `stable` (versions are kept; delete the runtime to remove them all)")
