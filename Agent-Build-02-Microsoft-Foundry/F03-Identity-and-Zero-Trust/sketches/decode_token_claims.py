"""Decode a JWT's header and payload for inspection. Untested sketch.

Shows the claims F03 Section 2 asks you to annotate (iss, tid, aud, oid, sub, azp/appid,
scp, roles, ver, exp) without pasting a token into a website. It performs NO validation:
no signature check, no issuer or audience check. Never use it as authentication.

Usage:
    python decode_token_claims.py            # reads the token from stdin
    python decode_token_claims.py < token.txt
The token is read from stdin on purpose so it does not land in shell history.
"""

from __future__ import annotations

import base64
import datetime as dt
import json
import sys

EXPLAIN = {
    "iss": "issuer; must be the tenant you trust",
    "tid": "tenant ID; pair with iss",
    "aud": "audience; must be THIS API or the token is rejected",
    "oid": "object ID of the caller in the tenant (user, SP, MI, agent identity)",
    "sub": "subject; pairwise per app for users, equals oid for service principals",
    "azp": "client application ID (v2)",
    "appid": "client application ID (v1)",
    "scp": "delegated scopes, space-separated; the user's authority narrowed by the app's grant",
    "roles": "app roles; application permissions (app-only) or assigned user roles",
    "ver": "token version; 1.0 or 2.0 claim rules",
    "exp": "expiry (unix seconds)",
    "nbf": "not before",
    "iat": "issued at",
    "idtyp": "'app' for app-only tokens when the API opted in to the claim",
    "xms_mirid": "Azure resource ID of a managed identity, when present",
}


def _b64url_decode(segment: str) -> bytes:
    padding = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + padding)


def decode(token: str) -> tuple[dict, dict]:
    parts = token.strip().split(".")
    if len(parts) != 3:
        raise ValueError("expected a compact JWS with three segments")
    header = json.loads(_b64url_decode(parts[0]))
    payload = json.loads(_b64url_decode(parts[1]))
    return header, payload


def annotate(payload: dict) -> list[str]:
    lines = []
    for key, value in payload.items():
        note = EXPLAIN.get(key, "")
        if key in {"exp", "nbf", "iat"} and isinstance(value, int):
            when = dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat()
            value = f"{value} ({when})"
        lines.append(f"{key:12} {value!s:60.60} {note}")
    kind = "app-only (roles, no scp)" if "roles" in payload and "scp" not in payload else (
        "delegated (scp present)" if "scp" in payload else "no permission claims"
    )
    lines.append(f"\nshape: {kind}")
    lines.append("reminder: nothing above has been validated; signature, iss and aud were not checked")
    return lines


def main() -> int:
    token = sys.stdin.read()
    header, payload = decode(token)
    print("header:", json.dumps(header))
    print()
    print("\n".join(annotate(payload)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
