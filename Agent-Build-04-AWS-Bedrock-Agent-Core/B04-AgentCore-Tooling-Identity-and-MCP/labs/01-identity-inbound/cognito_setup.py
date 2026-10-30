"""Create the Cognito user pool the JWT labs use: one app client with a secret (client-credentials for
machine callers) plus a resource server scope, and one test user for USER_PASSWORD_AUTH. Writes COGNITO_* to .env.

Proves: where the `discoveryUrl`, `allowedClients` and the bearer token for a customJWTAuthorizer come from.
Run: python cognito_setup.py [--cleanup]
"""

import argparse
import secrets

from _common import REGION, need, session, write_env

POOL_NAME = "agentcore-labs"
DOMAIN_PREFIX = "agentcore-labs-" + secrets.token_hex(3)


def main(cleanup: bool) -> None:
    idp = session().client("cognito-idp")
    if cleanup:
        pool_id = need("COGNITO_USER_POOL_ID")
        domain = idp.describe_user_pool(UserPoolId=pool_id)["UserPool"].get("Domain")
        if domain:
            idp.delete_user_pool_domain(Domain=domain, UserPoolId=pool_id)
        idp.delete_user_pool(UserPoolId=pool_id)
        print("deleted", pool_id)
        return

    pool = idp.create_user_pool(PoolName=POOL_NAME, AutoVerifiedAttributes=[], MfaConfiguration="OFF")["UserPool"]
    pool_id = pool["Id"]
    idp.create_user_pool_domain(Domain=DOMAIN_PREFIX, UserPoolId=pool_id)       # needed for the token endpoint
    idp.create_resource_server(                                                  # scopes for client-credentials tokens
        UserPoolId=pool_id, Identifier="tickets", Name="tickets",
        Scopes=[{"ScopeName": "invoke", "ScopeDescription": "call the ticket agent and gateway"}],
    )
    client = idp.create_user_pool_client(
        UserPoolId=pool_id, ClientName="agentcore-labs-client", GenerateSecret=True,
        ExplicitAuthFlows=["ALLOW_USER_PASSWORD_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"],
        AllowedOAuthFlows=["client_credentials"], AllowedOAuthScopes=["tickets/invoke"],
        AllowedOAuthFlowsUserPoolClient=True, SupportedIdentityProviders=["COGNITO"],
    )["UserPoolClient"]
    username, password = "ayse", "Tmp-" + secrets.token_urlsafe(12) + "1!"
    idp.admin_create_user(UserPoolId=pool_id, Username=username, MessageAction="SUPPRESS")
    idp.admin_set_user_password(UserPoolId=pool_id, Username=username, Password=password, Permanent=True)

    discovery = f"https://cognito-idp.{REGION}.amazonaws.com/{pool_id}/.well-known/openid-configuration"
    write_env("COGNITO_USER_POOL_ID", pool_id)
    write_env("COGNITO_CLIENT_ID", client["ClientId"])
    write_env("COGNITO_CLIENT_SECRET", client["ClientSecret"])      # local .env only; never commit
    write_env("COGNITO_DOMAIN", f"https://{DOMAIN_PREFIX}.auth.{REGION}.amazoncognito.com")
    write_env("COGNITO_DISCOVERY_URL", discovery)
    write_env("COGNITO_TEST_USERNAME", username)
    write_env("COGNITO_TEST_PASSWORD", password)
    print("\ndiscovery URL:", discovery)
    print("allowedClients:", client["ClientId"])


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--cleanup", action="store_true")
    main(p.parse_args().cleanup)
