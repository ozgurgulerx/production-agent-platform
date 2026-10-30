"""Row OAUTH / TOKEN_EXCHANGE (on-behalf-of, Apr 2026): the inbound Entra JWT is exchanged (RFC 8693) for a
downstream token for the same user, no consent screen. Uses the built-in MicrosoftOauth2 vendor with
onBehalfOfTokenExchangeConfig; the tool then calls Microsoft Graph as the user.

NEEDS an Entra app registration (ENTRA_TENANT_ID, ENTRA_CLIENT_ID, ENTRA_CLIENT_SECRET) and the agent's inbound
authorizer pointed at Entra. Shape-exact against botocore 1.43.118; not run. Run: python 04_obo_token_exchange.py [--cleanup]
"""

import argparse
import asyncio

import httpx
from bedrock_agentcore.identity import requires_access_token

from _common import control, need, write_env

NAME = "entra-obo"


def create_provider(cleanup: bool) -> None:
    cp = control()
    if cleanup:
        cp.delete_oauth2_credential_provider(name=NAME); print("deleted"); return
    r = cp.create_oauth2_credential_provider(
        name=NAME, credentialProviderVendor="MicrosoftOauth2",
        oauth2ProviderConfigInput={"microsoftOauth2ProviderConfig": {
            "clientId": need("ENTRA_CLIENT_ID"), "clientSecret": need("ENTRA_CLIENT_SECRET"), "tenantId": need("ENTRA_TENANT_ID")}},
        # For a non-Microsoft IdP use customOauth2ProviderConfig + onBehalfOfTokenExchangeConfig:
        #   {"grantType": "TOKEN_EXCHANGE", "tokenExchangeGrantTypeConfig": {"actorTokenContent": "M2M"}}      # verify
    )
    write_env("ENTRA_OBO_PROVIDER_ARN", r["credentialProviderArn"])


@requires_access_token(provider_name=NAME, scopes=["https://graph.microsoft.com/User.Read"],
                       auth_flow="ON_BEHALF_OF_TOKEN_EXCHANGE")           # exchanges the caller's inbound JWT
async def graph_me(*, access_token: str) -> str:
    r = await httpx.AsyncClient(timeout=30).get("https://graph.microsoft.com/v1.0/me", headers={"Authorization": f"Bearer {access_token}"})
    return f"{r.status_code} {r.text[:200]}"          # downstream sees: the Entra user, via the agent as actor


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--cleanup", action="store_true"); p.add_argument("--call", action="store_true")
    a = p.parse_args()
    if a.call:
        print(asyncio.run(graph_me()))
    else:
        create_provider(a.cleanup)
