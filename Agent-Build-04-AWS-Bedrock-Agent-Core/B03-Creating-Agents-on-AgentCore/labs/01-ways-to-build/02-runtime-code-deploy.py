"""Way 2: direct code deploy. Zips agent/, uploads it to S3, creates an AgentCore Runtime from the
zip (no container, no ECR), waits for READY and records the ARN. Proves that a Runtime is an
immutable version behind the DEFAULT endpoint, created from code with roleArn + entryPoint.
Usage: python 02-runtime-code-deploy.py [--keep] [--cleanup]
"""
from __future__ import annotations

import argparse
import io
import os
import time
import zipfile
from pathlib import Path

from _common import CODE_BUCKET, MODEL_ID, ROLE_ARN, control, require, session, write_env

NAME = "ticket_agent_code"  # runtime names: letters, digits, underscore
require("AGENTCORE_RUNTIME_ROLE_ARN", "CODE_BUCKET")


def zip_agent() -> bytes:
    """main.py and requirements.txt must sit at the zip root (B6)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for p in (Path(__file__).parent / "agent").iterdir():
            if p.suffix in {".py", ".txt"}:
                z.write(p, p.name)
    return buf.getvalue()


def find_runtime(cp, name: str):
    for rt in cp.list_agent_runtimes(maxResults=100).get("agentRuntimes", []):
        if rt["agentRuntimeName"] == name:
            return rt
    return None


def wait_ready(cp, runtime_id: str) -> dict:
    while True:
        rt = cp.get_agent_runtime(agentRuntimeId=runtime_id)
        print(f"  status={rt['status']}")
        if rt["status"] == "READY":
            return rt
        if rt["status"].endswith("FAILED"):
            raise SystemExit(rt.get("failureReason"))
        time.sleep(10)


def create(cp) -> dict:
    key = f"agentcore/{NAME}.zip"
    session().client("s3").put_object(Bucket=CODE_BUCKET, Key=key, Body=zip_agent())
    write_env("TICKET_AGENT_CODE_S3_URI", f"s3://{CODE_BUCKET}/{key}")   # B04 lab 01 redeploys this zip behind a JWT authorizer
    print(f"[s3] s3://{CODE_BUCKET}/{key}")
    resp = cp.create_agent_runtime(
        agentRuntimeName=NAME,
        description="B03 ticket agent, direct code deploy",
        agentRuntimeArtifact={"codeConfiguration": {
            "code": {"s3": {"bucket": CODE_BUCKET, "prefix": key}},
            "runtime": "PYTHON_3_13",
            "entryPoint": ["main.py"],
        }},
        roleArn=ROLE_ARN,
        networkConfiguration={"networkMode": "PUBLIC"},
        protocolConfiguration={"serverProtocol": "HTTP"},
        environmentVariables={"BEDROCK_MODEL_ID": MODEL_ID},
        platformVersion="V2",  # snapshot cold starts; V1 is the default (B3)
    )
    print(f"[create] {resp['agentRuntimeArn']} version {resp['agentRuntimeVersion']}")
    return wait_ready(cp, resp["agentRuntimeId"])


def cleanup(cp, runtime_id: str) -> None:
    for ep in cp.list_agent_runtime_endpoints(agentRuntimeId=runtime_id).get("runtimeEndpoints", []):
        if ep["name"] != "DEFAULT":
            cp.delete_agent_runtime_endpoint(agentRuntimeId=runtime_id, endpointName=ep["name"])
    cp.delete_agent_runtime(agentRuntimeId=runtime_id)
    print("[cleanup] runtime deleted")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", action="store_true", help="leave the runtime for 04/05 and later chapters")
    ap.add_argument("--cleanup", action="store_true")
    args = ap.parse_args()
    cp = control()
    existing = find_runtime(cp, NAME)
    if args.cleanup:
        if existing:
            cleanup(cp, existing["agentRuntimeId"])
        raise SystemExit(0)
    rt = wait_ready(cp, existing["agentRuntimeId"]) if existing else create(cp)
    write_env("TICKET_AGENT_RUNTIME_ARN", rt["agentRuntimeArn"])
    if not args.keep:
        cleanup(cp, rt["agentRuntimeId"])
