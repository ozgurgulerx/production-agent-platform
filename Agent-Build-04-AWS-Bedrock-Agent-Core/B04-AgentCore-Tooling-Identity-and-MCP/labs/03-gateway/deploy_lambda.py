"""Zip lambda_tools/handler.py and create (or update) the `ticket-tools` Lambda on python3.13 / arm64, plus a minimal
execution role. Writes TICKET_TOOLS_LAMBDA_ARN. Run: python deploy_lambda.py [--cleanup]"""

import argparse
import io
import json
import time
import zipfile
from pathlib import Path

from _common import need, session, write_env

FN, ROLE = "ticket-tools", "ticket-tools-lambda-role"


def main(cleanup: bool) -> None:
    s = session(); lam, iam = s.client("lambda"), s.client("iam")
    if cleanup:
        lam.delete_function(FunctionName=FN); iam.detach_role_policy(RoleName=ROLE, PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"); iam.delete_role(RoleName=ROLE); print("deleted"); return
    trust = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}
    try:
        role = iam.create_role(RoleName=ROLE, AssumeRolePolicyDocument=json.dumps(trust))["Role"]["Arn"]
        iam.attach_role_policy(RoleName=ROLE, PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"); time.sleep(10)
    except iam.exceptions.EntityAlreadyExistsException:
        role = iam.get_role(RoleName=ROLE)["Role"]["Arn"]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.write(Path(__file__).parent / "lambda_tools" / "handler.py", "handler.py")
    try:
        arn = lam.create_function(FunctionName=FN, Runtime="python3.13", Architectures=["arm64"], Role=role, Handler="handler.handler",
                                  Code={"ZipFile": buf.getvalue()}, Timeout=30)["FunctionArn"]
    except lam.exceptions.ResourceConflictException:
        arn = lam.update_function_code(FunctionName=FN, ZipFile=buf.getvalue())["FunctionArn"]
    write_env("TICKET_TOOLS_LAMBDA_ARN", arn)
    _ = need  # keep import for symmetry with other scripts


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--cleanup", action="store_true"); main(p.parse_args().cleanup)
