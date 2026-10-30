"""Call the JWT runtime over raw HTTPS. First with a bad token (expect 401 + WWW-Authenticate with
resource_metadata, RFC 9728), then with a real Cognito token (expect 200 and an answer).

Proves: a JWT Runtime is not reachable through `invoke_agent_runtime`; the token, the session header and the URL
shape are the whole contract. Run: python invoke_with_bearer.py [--m2m]
"""

import argparse
import json

import httpx

from _common import need, new_session_id, runtime_invocations_url
from tokens import client_credentials_token, user_token


def call(url: str, token: str, prompt: str) -> httpx.Response:
    return httpx.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json",
                 "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id": new_session_id()},
        json={"prompt": prompt}, timeout=120,
    )


def main(m2m: bool) -> None:
    url = runtime_invocations_url(need("TICKET_AGENT_JWT_ARN"))
    print("URL", url)

    r = call(url, "not-a-token", "status of ticket 1042?")
    print("\n[1] bad token →", r.status_code, "| WWW-Authenticate:", r.headers.get("www-authenticate"))
    assert r.status_code == 401, "expected 401 with a bad token"

    token = client_credentials_token() if m2m else user_token()
    r = call(url, token, "What is the status of ticket 1042?")
    print(f"\n[2] {'m2m' if m2m else 'user'} token →", r.status_code)
    try:
        print(json.dumps(r.json(), indent=2)[:800])
    except ValueError:
        print(r.text[:800])                       # text/event-stream when the agent streams


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--m2m", action="store_true", help="use a client-credentials token instead of the test user")
    main(p.parse_args().m2m)
