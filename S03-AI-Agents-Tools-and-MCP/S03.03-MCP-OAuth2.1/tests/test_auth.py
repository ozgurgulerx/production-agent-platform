import asyncio
import time
from types import SimpleNamespace

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from mcp.server.auth.provider import AccessToken
from mcp.server.fastmcp.exceptions import ToolError

import auth


@pytest.fixture
def signing_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


@pytest.fixture
def claims():
    now = int(time.time())
    return {'iss': auth.ISSUER, 'aud': auth.RESOURCE, 'sub': 'user-123',
            'azp': auth.CLIENT_ID, 'exp': now + 300, 'iat': now,
            'scope': 'openid tickets.read policies.read'}


def verify(key, claims, headers=None, signing_key=None):
    verifier = auth.KeycloakTokenVerifier()
    verifier.jwks_client = SimpleNamespace(
        get_signing_key_from_jwt=lambda token: SimpleNamespace(key=key.public_key()))
    token = jwt.encode(claims, signing_key or key, algorithm='RS256',
                       headers={'typ': 'at+jwt', 'kid': 'test', **(headers or {})})
    return asyncio.run(verifier.verify_token(token))


def test_valid_token(signing_key, claims):
    result = verify(signing_key, claims)
    assert isinstance(result, auth.VerifiedAccessToken)
    assert result.subject == 'user-123'
    assert result.scopes == ['openid', 'tickets.read', 'policies.read']
    assert result.resource == auth.RESOURCE
    assert result.client_id == auth.CLIENT_ID


@pytest.mark.parametrize('field,value', [
    ('exp', 1), ('aud', 'other-service'), ('iss', 'https://evil.example'),
    ('sub', ''), ('sub', 123), ('azp', 'other-client'), ('iat', 9999999999),
    ('nbf', 9999999999), ('scope', ['tickets.refund']), ('scope', None),
    ('scope', 'tickets.read\ntickets.refund'), ('scope', 'tickets.read\ttickets.refund'),
    ('scope', 'tickets.read  tickets.refund'), ('exp', '9999999999'),
    ('iat', '123'), ('exp', True),
])
def test_invalid_claims(signing_key, claims, field, value):
    assert verify(signing_key, {**claims, field: value}) is None


@pytest.mark.parametrize('field', ['exp', 'iat', 'iss', 'aud', 'sub', 'azp', 'scope'])
def test_missing_claim(signing_key, claims, field):
    assert verify(signing_key, {k: v for k, v in claims.items() if k != field}) is None


@pytest.mark.parametrize('typ', ['JWT', 'ID', 'Bearer', ''])
def test_reject_id_token_header(signing_key, claims, typ):
    assert verify(signing_key, claims, {'typ': typ}) is None


def test_wrong_signature(signing_key, claims):
    other = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    assert verify(signing_key, claims, signing_key=other) is None


def test_malformed_token():
    assert asyncio.run(auth.KeycloakTokenVerifier().verify_token('garbage')) is None


def test_wrong_algorithm(claims):
    token = jwt.encode(claims, 'a-long-test-secret-at-least-32bytes', algorithm='HS256',
                       headers={'typ': 'at+jwt'})
    assert asyncio.run(auth.KeycloakTokenVerifier().verify_token(token)) is None


def test_jwks_unavailable(signing_key, claims):
    verifier = auth.KeycloakTokenVerifier()
    def fail(token):
        raise jwt.PyJWKClientConnectionError('offline')
    verifier.jwks_client = SimpleNamespace(get_signing_key_from_jwt=fail)
    token = jwt.encode(claims, signing_key, algorithm='RS256', headers={'typ': 'at+jwt'})
    assert asyncio.run(verifier.verify_token(token)) is None


def test_explicit_empty_scope(signing_key, claims):
    result = verify(signing_key, {**claims, 'scope': ''})
    assert result.scopes == []


def test_require_scope(signing_key, claims, monkeypatch):
    result = verify(signing_key, claims)
    monkeypatch.setattr(auth, 'get_access_token', lambda: result)
    assert auth.require_scope('tickets.read') is result
    with pytest.raises(ToolError, match='tickets.refund'):
        auth.require_scope('tickets.refund')


def test_require_scope_expired(signing_key, claims, monkeypatch):
    result = verify(signing_key, claims)
    monkeypatch.setattr(auth, 'get_access_token', lambda: result)
    monkeypatch.setattr(auth.time, 'time', lambda: claims['exp'])
    with pytest.raises(ToolError, match='expired'):
        auth.require_scope('tickets.read')


@pytest.mark.parametrize('token', [None, AccessToken(token='unverified', client_id='client', scopes=['tickets.refund'])])
def test_require_scope_needs_verified_token(monkeypatch, token):
    monkeypatch.setattr(auth, 'get_access_token', lambda: token)
    with pytest.raises(ToolError, match='Authentication required'):
        auth.require_scope('tickets.refund')
