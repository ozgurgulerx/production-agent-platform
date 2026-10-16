"""Validate Keycloak access tokens and enforce tool scopes.

Discovery and token-provided URLs never determine where signing keys are fetched.
The HTTP URLs here are for this loopback-only teaching environment.
"""

import asyncio
import re
import time

import jwt
from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.fastmcp.exceptions import ToolError

ISSUER = 'http://127.0.0.1:9000/realms/s03-mcp'
RESOURCE = 'http://127.0.0.1:8000/mcp'
CLIENT_ID = 's03-mcp-client'
JWKS_URL = f'{ISSUER}/protocol/openid-connect/certs'
# OAuth scope-token syntax (RFC 6749 section 3.3), separated by one ASCII space.
SCOPE_PATTERN = re.compile(r'[\x21\x23-\x5b\x5d-\x7e]+(?: [\x21\x23-\x5b\x5d-\x7e]+)*')


class VerifiedAccessToken(AccessToken):
    """Preserve the verified user identity on MCP SDK 1.26's access token."""

    subject: str


class KeycloakTokenVerifier(TokenVerifier):
    """Accept only this demo client's signed access tokens for this MCP resource."""

    def __init__(self):
        self.jwks_client = jwt.PyJWKClient(JWKS_URL, timeout=5, lifespan=300)

    async def verify_token(self, token: str) -> VerifiedAccessToken | None:
        # PyJWKClient may fetch keys over HTTP; keep it off the event loop.
        return await asyncio.to_thread(self._verify, token)

    def _verify(self, token: str) -> VerifiedAccessToken | None:
        try:
            header = jwt.get_unverified_header(token)
            if header.get('alg') != 'RS256' or header.get('typ') != 'at+jwt':
                return None
            key = self.jwks_client.get_signing_key_from_jwt(token).key
            claims = jwt.decode(
                token, key, algorithms=['RS256'], issuer=ISSUER, audience=RESOURCE,
                options={'require': ['exp', 'iat', 'iss', 'aud', 'sub', 'azp', 'scope']},
            )
            if claims['azp'] != CLIENT_ID or not isinstance(claims['sub'], str) or not claims['sub']:
                return None
            if any(type(claims[name]) is not int for name in ('exp', 'iat')):
                return None
            scope = claims['scope']
            if not isinstance(scope, str) or (scope and not SCOPE_PATTERN.fullmatch(scope)):
                return None
            return VerifiedAccessToken(
                token=token, client_id=claims['azp'], subject=claims['sub'],
                scopes=scope.split(' ') if scope else [], expires_at=claims['exp'],
                resource=RESOURCE,
            )
        except (jwt.PyJWTError, ValueError, TypeError):
            # Fail closed without disclosing tokens or internal key-service details.
            return None


def require_scope(scope: str) -> VerifiedAccessToken:
    """Authorize a tool from the server's authenticated context, never tool input."""
    token = get_access_token()
    if not isinstance(token, VerifiedAccessToken):
        raise ToolError('Authentication required.')
    if token.expires_at is None or token.expires_at <= time.time():
        raise ToolError('Access token expired; sign in again.')
    if scope not in token.scopes:
        raise ToolError(f'Permission denied: required scope {scope}.')
    return token
