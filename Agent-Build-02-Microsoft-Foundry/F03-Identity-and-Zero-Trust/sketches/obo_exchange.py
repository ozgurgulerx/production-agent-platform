"""Shape of the on-behalf-of token request (F03 Section 7). Untested sketch.

A middle-tier API (the ticket API) redeems the access token it received, whose `aud`
is the ticket API itself, for a token to a downstream API as the same user.
Parameters follow the Microsoft identity platform OBO page read 30 October 2026.

In real code use `azure.identity.OnBehalfOfCredential` or MSAL; this sketch exists so
you can say what those libraries send. Never log `assertion` or the returned token.
"""

from __future__ import annotations

import httpx

TOKEN_ENDPOINT = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
JWT_BEARER = "urn:ietf:params:oauth:grant-type:jwt-bearer"


def obo_request(
    *,
    tenant: str,
    client_id: str,
    client_assertion: str,
    incoming_access_token: str,
    downstream_scope: str = "https://graph.microsoft.com/.default",
) -> dict:
    """Return the token endpoint JSON for an OBO exchange.

    Preconditions the token endpoint enforces (and that your API should check first):
    - incoming_access_token.aud == client_id  (a Graph-audience token cannot be redeemed here)
    - the subject is a user principal (app-only tokens use client credentials instead)
    - the middle tier is a confidential client (certificate assertion here, secret only in tests)
    - downstream_scope is either `.default` or named scopes, never both (AADSTS70011)
    """
    data = {
        "grant_type": JWT_BEARER,
        "client_id": client_id,
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": client_assertion,
        "assertion": incoming_access_token,
        "scope": downstream_scope,
        "requested_token_use": "on_behalf_of",
    }
    resp = httpx.post(TOKEN_ENDPOINT.format(tenant=tenant), data=data, timeout=10.0)
    if resp.status_code == 400 and resp.json().get("error") == "interaction_required":
        # downstream wants a claims challenge (for example MFA): surface 401 + WWW-Authenticate
        # to the client; do not retry with the cached token and do not fall back to app-only.
        raise PermissionError(resp.json().get("error_description", "interaction_required"))
    resp.raise_for_status()
    return resp.json()
