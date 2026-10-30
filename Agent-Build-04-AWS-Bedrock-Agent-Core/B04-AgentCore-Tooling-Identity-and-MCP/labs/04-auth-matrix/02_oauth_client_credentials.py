"""Row OAUTH / CLIENT_CREDENTIALS (2LO): a CustomOauth2 provider from a discovery URL plus client id/secret (the
lab Cognito pool works as the IdP), attached to the OpenAPI target with grantType CLIENT_CREDENTIALS and the
`tickets/invoke` scope. Downstream sees: a token for the agent's client, no user. Writes TICKETS_OAUTH_PROVIDER_ARN.

Run: python 02_oauth_client_credentials.py [--cleanup]   (uses COGNITO_* unless OAUTH_* are set)
"""

import argparse
import os

from _common import control, need, write_env

NAME = "tickets-oauth-m2m"


def main(cleanup: bool) -> None:
    cp = control()
    if cleanup:
        cp.delete_oauth2_credential_provider(name=NAME); print("deleted"); return
    r = cp.create_oauth2_credential_provider(
        name=NAME, credentialProviderVendor="CustomOauth2",
        oauth2ProviderConfigInput={"customOauth2ProviderConfig": {
            "oauthDiscovery": {"discoveryUrl": os.environ.get("OAUTH_DISCOVERY_URL") or need("COGNITO_DISCOVERY_URL")},
            "clientId": os.environ.get("OAUTH_CLIENT_ID") or need("COGNITO_CLIENT_ID"),
            "clientSecret": os.environ.get("OAUTH_CLIENT_SECRET") or need("COGNITO_CLIENT_SECRET"),
            "clientAuthenticationMethod": "CLIENT_SECRET_BASIC",
            # "clientSecretSource": "EXTERNAL", "clientSecretConfig": {"secretId": "<secrets manager arn>"}  # Jul 2026 option
        }},
    )
    arn = r["credentialProviderArn"]
    print("provider", arn, "| callbackUrl (for 3LO rows):", r.get("callbackUrl"))
    write_env("TICKETS_OAUTH_PROVIDER_ARN", arn)
    tid, gid = os.environ.get("TICKETS_API_TARGET_ID"), os.environ.get("TICKET_GATEWAY_ID")
    if tid and gid:
        t = cp.get_gateway_target(gatewayIdentifier=gid, targetId=tid)
        cp.update_gateway_target(gatewayIdentifier=gid, targetId=tid, name=t["name"], targetConfiguration=t["targetConfiguration"],
                                 credentialProviderConfigurations=[{"credentialProviderType": "OAUTH", "credentialProvider": {
                                     "oauthCredentialProvider": {"providerArn": arn, "scopes": ["tickets/invoke"],
                                                                 "grantType": "CLIENT_CREDENTIALS"}}}])
        print("attached (2LO) to", t["name"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--cleanup", action="store_true"); main(p.parse_args().cleanup)
