"""Row OAUTH / AUTHORIZATION_CODE (3LO): the agent's tool gets a token *as the user*. First call prints the consent
URL (`on_auth_url`), blocks until consent, then runs; later calls hit the token vault. Needs an OAuth app whose
redirect URI is the provider's `callbackUrl` (printed by 02_...). Set OAUTH_3LO_PROVIDER to that provider name.

Run inside a Runtime (the workload token is injected) or locally with a workload identity (see run_matrix.py).
Downstream sees: the user. Consent Portal (Sep 2026) replaces the printed URL for Gateway-fronted agents.
"""

import asyncio
import os

import httpx
from bedrock_agentcore.identity import requires_access_token

PROVIDER = os.environ.get("OAUTH_3LO_PROVIDER", "tickets-oauth-m2m")
API = os.environ.get("TICKETS_API_BASE", "https://tickets.example.internal")


@requires_access_token(provider_name=PROVIDER, scopes=["tickets/invoke"], auth_flow="USER_FEDERATION",
                       on_auth_url=lambda url: print(f"\nCONSENT NEEDED → open: {url}\n"), force_authentication=False)
async def whoami(*, access_token: str) -> str:
    """Call the tickets API with the user's token; the API's /me tells us which principal it saw."""
    r = await httpx.AsyncClient(timeout=30).get(f"{API}/me", headers={"Authorization": f"Bearer {access_token}"})
    return f"{r.status_code} {r.text[:200]}"


if __name__ == "__main__":
    print(asyncio.run(whoami()))
