"""Two ways to get a bearer token from the lab Cognito pool. Imported by the other labs."""

import base64
import os

import httpx

from _common import need, session


def user_token() -> str:
    """USER_PASSWORD_AUTH: an id/access token that carries the user (sub, username)."""
    idp = session().client("cognito-idp")
    r = idp.initiate_auth(
        ClientId=need("COGNITO_CLIENT_ID"), AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": need("COGNITO_TEST_USERNAME"), "PASSWORD": need("COGNITO_TEST_PASSWORD"),
                        "SECRET_HASH": _secret_hash(need("COGNITO_TEST_USERNAME"))},
    )
    return r["AuthenticationResult"]["AccessToken"]


def client_credentials_token(scope: str = "tickets/invoke") -> str:
    """client_credentials: a machine token with the resource-server scope, no user."""
    basic = base64.b64encode(f"{need('COGNITO_CLIENT_ID')}:{need('COGNITO_CLIENT_SECRET')}".encode()).decode()
    r = httpx.post(f"{need('COGNITO_DOMAIN')}/oauth2/token", headers={"Authorization": f"Basic {basic}"},
                   data={"grant_type": "client_credentials", "scope": scope}, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]


def _secret_hash(username: str) -> str:
    import hashlib, hmac
    key = need("COGNITO_CLIENT_SECRET").encode()
    msg = (username + need("COGNITO_CLIENT_ID")).encode()
    return base64.b64encode(hmac.new(key, msg, hashlib.sha256).digest()).decode()


if __name__ == "__main__":
    print("user token:", user_token()[:40], "...")
    print("m2m token :", client_credentials_token()[:40], "...")
