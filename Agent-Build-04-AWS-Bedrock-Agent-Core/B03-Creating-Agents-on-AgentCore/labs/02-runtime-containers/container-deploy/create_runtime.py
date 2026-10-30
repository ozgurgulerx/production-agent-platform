"""Way 3: Runtime from a container image. Same contract as the zip deploy, different artifact:
`containerConfiguration.containerUri` instead of `codeConfiguration`. Proves the artifact is the
only thing that changes between ways 2 and 3.
Usage: python create_runtime.py --image <ecr-uri> [--keep] [--cleanup]
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "01-ways-to-build"))
from _common import MODEL_ID, ROLE_ARN, control, require, write_env  # noqa: E402

NAME = "ticket_agent_container"
require("AGENTCORE_RUNTIME_ROLE_ARN")
ap = argparse.ArgumentParser()
ap.add_argument("--image", required=False)
ap.add_argument("--keep", action="store_true")
ap.add_argument("--cleanup", action="store_true")
args = ap.parse_args()
cp = control()

existing = next((r for r in cp.list_agent_runtimes(maxResults=100)["agentRuntimes"] if r["agentRuntimeName"] == NAME), None)
if args.cleanup:
    if existing:
        cp.delete_agent_runtime(agentRuntimeId=existing["agentRuntimeId"])
        print("[cleanup] deleted")
    raise SystemExit(0)
if not existing:
    if not args.image:
        raise SystemExit("--image is required to create")
    resp = cp.create_agent_runtime(
        agentRuntimeName=NAME,
        agentRuntimeArtifact={"containerConfiguration": {"containerUri": args.image}},
        roleArn=ROLE_ARN,  # the role must also allow ecr:GetDownloadUrlForLayer/BatchGetImage on the repo
        networkConfiguration={"networkMode": "PUBLIC"},
        protocolConfiguration={"serverProtocol": "HTTP"},
        environmentVariables={"BEDROCK_MODEL_ID": MODEL_ID},
    )
    rid = resp["agentRuntimeId"]
else:
    rid = existing["agentRuntimeId"]
while (rt := cp.get_agent_runtime(agentRuntimeId=rid))["status"] != "READY":
    print("  status=", rt["status"])
    if "FAIL" in rt["status"]:
        raise SystemExit(rt.get("failureReason"))
    time.sleep(10)
print("READY", rt["agentRuntimeArn"])
write_env("TICKET_AGENT_CONTAINER_RUNTIME_ARN", rt["agentRuntimeArn"])
if not args.keep:
    cp.delete_agent_runtime(agentRuntimeId=rid)
