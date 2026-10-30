"""Zip `mcp_server/`, upload it to CODE_BUCKET, create a Runtime with serverProtocol=MCP behind the lab 01 JWT
authorizer, wait for READY, write TICKET_MCP_RUNTIME_ARN and TICKET_MCP_URL.

Proves: Runtime hosts MCP servers with the same create call as agents; only the protocol and the port differ.
Run: python deploy_mcp_runtime.py [--cleanup]
"""

import argparse
import io
import time
import zipfile
from pathlib import Path

from _common import control, need, runtime_invocations_url, session, write_env

NAME = "ticket_mcp_server"
SRC = Path(__file__).parent / "mcp_server"


def upload_zip() -> str:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for f in SRC.iterdir():
            z.write(f, f.name)                       # main.py and requirements.txt at the zip root
    key = f"code/{NAME}.zip"
    session().client("s3").put_object(Bucket=need("CODE_BUCKET"), Key=key, Body=buf.getvalue())
    return f"s3://{need('CODE_BUCKET')}/{key}"


def main(cleanup: bool) -> None:
    cp = control()
    if cleanup:
        cp.delete_agent_runtime(agentRuntimeId=need("TICKET_MCP_RUNTIME_ARN").split("/")[-1])
        print("deleted")
        return
    uri = upload_zip()
    r = cp.create_agent_runtime(
        agentRuntimeName=NAME,
        roleArn=need("AGENTCORE_RUNTIME_ROLE_ARN"),
        agentRuntimeArtifact={"codeConfiguration": {"code": {"s3": {"uri": uri}}, "runtime": "PYTHON_3_13",  # verify s3 keys
                                                    "entryPoint": ["main.py"]}},
        networkConfiguration={"networkMode": "PUBLIC"},
        protocolConfiguration={"serverProtocol": "MCP"},                       # the only line that differs from an agent
        authorizerConfiguration={"customJWTAuthorizer": {"discoveryUrl": need("COGNITO_DISCOVERY_URL"),
                                                         "allowedClients": [need("COGNITO_CLIENT_ID")]}},
    )
    rid, arn = r["agentRuntimeId"], r["agentRuntimeArn"]
    while (st := cp.get_agent_runtime(agentRuntimeId=rid)["status"]) in ("CREATING", "UPDATING"):
        print("  status", st); time.sleep(10)
    print("status", st)
    if st != "READY":
        print(cp.get_agent_runtime(agentRuntimeId=rid).get("failureReason"))   # wrong port shows up here
    write_env("TICKET_MCP_RUNTIME_ARN", arn)
    write_env("TICKET_MCP_URL", runtime_invocations_url(arn))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--cleanup", action="store_true")
    main(p.parse_args().cleanup)
