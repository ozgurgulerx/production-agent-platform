"""Row API_KEY: store an API key in the token vault as a credential provider and attach it to the OpenAPI target.
The Gateway injects it as `x-api-key` on every call; the agent never sees it. Writes TICKETS_API_KEY_PROVIDER_ARN.

Run: TICKETS_API_KEY=<key> python 01_api_key_provider.py [--cleanup]
"""

import argparse
import os

from _common import control, need, write_env

NAME = "tickets-api-key"


def main(cleanup: bool) -> None:
    cp = control()
    if cleanup:
        cp.delete_api_key_credential_provider(name=NAME); print("deleted"); return
    r = cp.create_api_key_credential_provider(name=NAME, apiKey=need("TICKETS_API_KEY"))   # MANAGED: vault stores it
    arn = r["credentialProviderArn"]
    write_env("TICKETS_API_KEY_PROVIDER_ARN", arn)
    tid, gid = os.environ.get("TICKETS_API_TARGET_ID"), os.environ.get("TICKET_GATEWAY_ID")
    if tid and gid:
        t = cp.get_gateway_target(gatewayIdentifier=gid, targetId=tid)
        cp.update_gateway_target(gatewayIdentifier=gid, targetId=tid, name=t["name"], targetConfiguration=t["targetConfiguration"],
                                 credentialProviderConfigurations=[{"credentialProviderType": "API_KEY", "credentialProvider": {
                                     "apiKeyCredentialProvider": {"providerArn": arn, "credentialLocation": "HEADER",
                                                                  "credentialParameterName": "x-api-key"}}}])
        print("attached to target", t["name"], "— downstream sees: the stored key (no user)")


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--cleanup", action="store_true"); main(p.parse_args().cleanup)
