"""Deploy interceptor/handler.py as a Lambda and attach it to the Gateway as a REQUEST interceptor via update_gateway
(which requires name, roleArn and authorizerType again). Run: python attach_interceptor.py [--detach]

Proves: the hook runs before any target, independent of which backend serves the tool.
"""

import argparse
import io
import zipfile
from pathlib import Path

from _common import control, need, session

FN = "ticket-gateway-interceptor"


def deploy() -> str:
    lam, iam = session().client("lambda"), session().client("iam")
    role = iam.get_role(RoleName="ticket-tools-lambda-role")["Role"]["Arn"]      # reuse lab role from deploy_lambda.py
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.write(Path(__file__).parent / "interceptor" / "handler.py", "handler.py")
    try:
        return lam.create_function(FunctionName=FN, Runtime="python3.13", Architectures=["arm64"], Role=role,
                                   Handler="handler.handler", Code={"ZipFile": buf.getvalue()}, Timeout=10)["FunctionArn"]
    except lam.exceptions.ResourceConflictException:
        return lam.update_function_code(FunctionName=FN, ZipFile=buf.getvalue())["FunctionArn"]


def main(detach: bool) -> None:
    cp, gid = control(), need("TICKET_GATEWAY_ID")
    g = cp.get_gateway(gatewayIdentifier=gid)
    base = dict(gatewayIdentifier=gid, name=g["name"], roleArn=g["roleArn"], authorizerType=g["authorizerType"],
                authorizerConfiguration=g.get("authorizerConfiguration", {}), protocolType=g["protocolType"],
                protocolConfiguration=g.get("protocolConfiguration", {}))
    if detach:
        cp.update_gateway(**base, interceptorConfigurations=[]); print("detached"); return
    arn = deploy()
    cp.update_gateway(**base, interceptorConfigurations=[{"interceptor": {"lambda": {"arn": arn}},
                                                           "interceptionPoints": ["REQUEST"],
                                                           "inputConfiguration": {"passRequestHeaders": False}}])
    print("attached", arn, "— rerun search_and_call.py: the £400 refund must now fail before the Lambda logs it")


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--detach", action="store_true"); main(p.parse_args().detach)
