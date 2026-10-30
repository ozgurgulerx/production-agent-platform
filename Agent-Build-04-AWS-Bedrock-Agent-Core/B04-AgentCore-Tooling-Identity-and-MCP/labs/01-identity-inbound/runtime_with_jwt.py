"""Create `ticket-agent-jwt`: the same code zip as B03 lab 01's ticket agent, but with a customJWTAuthorizer so
only holders of a token from the lab Cognito pool (and only the lab client) can invoke it. Writes TICKET_AGENT_JWT_ARN.

Proves: inbound auth is a property of the Runtime, chosen at create time, SigV4 *or* JWT.
Run: python runtime_with_jwt.py [--cleanup]
"""

import argparse
import time

from _common import control, need, write_env

NAME = "ticket_agent_jwt"


def main(cleanup: bool) -> None:
    cp = control()
    if cleanup:
        rid = need("TICKET_AGENT_JWT_ARN").split("/")[-1]
        cp.delete_agent_runtime(agentRuntimeId=rid)
        print("deleted", rid)
        return

    code_uri = need("TICKET_AGENT_CODE_S3_URI")          # written by B03 lab 01 (the zip it uploaded)
    r = cp.create_agent_runtime(
        agentRuntimeName=NAME,
        roleArn=need("AGENTCORE_RUNTIME_ROLE_ARN"),
        agentRuntimeArtifact={"codeConfiguration": {"code": {"s3": {"uri": code_uri}},  # verify: s3 sub-shape keys
                                                    "runtime": "PYTHON_3_13", "entryPoint": ["main.py"]}},
        networkConfiguration={"networkMode": "PUBLIC"},
        protocolConfiguration={"serverProtocol": "HTTP"},
        authorizerConfiguration={"customJWTAuthorizer": {
            "discoveryUrl": need("COGNITO_DISCOVERY_URL"),
            "allowedClients": [need("COGNITO_CLIENT_ID")],
            # "allowedWorkloadConfiguration": {"workloadIdentities": [<gateway workload identity arn>]}  # lab 06
        }},
        environmentVariables={"BEDROCK_MODEL_ID": need("BEDROCK_MODEL_ID")},
    )
    arn, rid = r["agentRuntimeArn"], r["agentRuntimeId"]
    while (st := cp.get_agent_runtime(agentRuntimeId=rid)["status"]) in ("CREATING", "UPDATING"):
        print("  status", st); time.sleep(10)
    print("status", st)
    write_env("TICKET_AGENT_JWT_ARN", arn)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--cleanup", action="store_true")
    main(p.parse_args().cleanup)
