"""Shape only, untested. Outbound OAuth from inside a tool, the 3LO (USER_FEDERATION) way.

`@requires_access_token` asks AgentCore Identity for a token for `provider_name`. On a vault miss it returns an
authorization URL through `on_auth_url` and polls until the user consents; on a hit it injects the token straight
into the `access_token` kwarg. `auth_flow` is one of M2M (2LO), USER_FEDERATION (3LO), ON_BEHALF_OF_TOKEN_EXCHANGE.
Signature checked against bedrock-agentcore 1.25.0 on 2026-10-25.
"""

import httpx
from bedrock_agentcore.identity import requires_access_token
from strands import tool


@tool
@requires_access_token(
    provider_name="github-tickets",            # created once with create_oauth2_credential_provider
    scopes=["repo"],
    auth_flow="USER_FEDERATION",               # the user consents once; the vault stores the token per (workload, user)
    on_auth_url=lambda url: print(f"Approve here: {url}"),
    force_authentication=False,
)
async def open_github_issue(title: str, *, access_token: str) -> str:
    """Open a GitHub issue for an escalated ticket (3LO: the issue is created as the user)."""
    r = httpx.post(
        "https://api.github.com/repos/acme/support/issues",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"title": title},
    )
    return r.json().get("html_url", r.text)


# M2M variant: no user, no consent, the agent's own client credentials
# @requires_access_token(provider_name="tickets-idp", scopes=["tickets.read"], auth_flow="M2M")

# API key variant: injects `api_key`
# from bedrock_agentcore.identity import requires_api_key
# @requires_api_key(provider_name="weather-key")
