"""Creates the two Runtimes of this lab from zips: `ticket_agent_graph` (protocol HTTP) and
`ticket_refund_a2a` (protocol A2A, port 9000). Proves that the protocol is a Runtime property, not
a code property: same create call, `serverProtocol` differs.
Usage: python deploy_multi.py [--keep] [--cleanup]
"""
from __future__ import annotations

import argparse
import io
import sys
import time
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01-ways-to-build"))
from _common import CODE_BUCKET, MODEL_ID, ROLE_ARN, control, require, session, write_env  # noqa: E402

require("AGENTCORE_RUNTIME_ROLE_ARN", "CODE_BUCKET")
HERE = Path(__file__).parent
RUNTIMES = {  # name: (folder, protocol, env key)
    "ticket_agent_graph": ("graph_agent", "HTTP", "TICKET_GRAPH_RUNTIME_ARN"),
    "ticket_refund_a2a": ("a2a_server", "A2A", "TICKET_A2A_RUNTIME_ARN"),
}
REQS = "bedrock-agentcore[strands-agents,a2a]==1.25.0\nstrands-agents==1.62.0\na2a-sdk\n"


def zip_dir(folder: Path) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(folder / "main.py", "main.py")
        z.writestr("requirements.txt", REQS)
    return buf.getvalue()


def ensure(cp, name: str, folder: str, protocol: str) -> dict:
    for rt in cp.list_agent_runtimes(maxResults=100)["agentRuntimes"]:
        if rt["agentRuntimeName"] == name:
            return cp.get_agent_runtime(agentRuntimeId=rt["agentRuntimeId"])
    key = f"agentcore/{name}.zip"
    session().client("s3").put_object(Bucket=CODE_BUCKET, Key=key, Body=zip_dir(HERE / folder))
    resp = cp.create_agent_runtime(
        agentRuntimeName=name,
        agentRuntimeArtifact={"codeConfiguration": {"code": {"s3": {"bucket": CODE_BUCKET, "prefix": key}},
                                                    "runtime": "PYTHON_3_13", "entryPoint": ["main.py"]}},
        roleArn=ROLE_ARN,
        networkConfiguration={"networkMode": "PUBLIC"},
        protocolConfiguration={"serverProtocol": protocol},
        environmentVariables={"BEDROCK_MODEL_ID": MODEL_ID},
    )
    rid = resp["agentRuntimeId"]
    while (rt := cp.get_agent_runtime(agentRuntimeId=rid))["status"] != "READY":
        print(f"  {name}: {rt['status']}")
        if "FAIL" in rt["status"]:
            raise SystemExit(rt.get("failureReason"))
        time.sleep(10)
    return rt


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--cleanup", action="store_true")
    args = ap.parse_args()
    cp = control()
    if args.cleanup:
        for rt in cp.list_agent_runtimes(maxResults=100)["agentRuntimes"]:
            if rt["agentRuntimeName"] in RUNTIMES:
                cp.delete_agent_runtime(agentRuntimeId=rt["agentRuntimeId"]); print("[cleanup]", rt["agentRuntimeName"])
        raise SystemExit(0)
    created = []
    for name, (folder, protocol, key) in RUNTIMES.items():
        rt = ensure(cp, name, folder, protocol)
        write_env(key, rt["agentRuntimeArn"]); created.append(rt)
        if key == "TICKET_A2A_RUNTIME_ARN":                       # B04 labs 05/06 read the card URL
            from urllib.parse import quote
            region = session().region_name
            write_env("TICKET_A2A_CARD_URL",                              # verify: card path through the Runtime data plane (B9)
                      f"https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{quote(rt['agentRuntimeArn'], safe='')}"
                      "/invocations/.well-known/agent-card.json?qualifier=DEFAULT")
    if not args.keep:
        for rt in created:
            cp.delete_agent_runtime(agentRuntimeId=rt["agentRuntimeId"])
