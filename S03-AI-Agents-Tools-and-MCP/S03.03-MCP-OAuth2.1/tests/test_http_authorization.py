"""Real HTTP transport, auth middleware, JWT verification, and tool dispatch."""
import importlib
import json
import time
from types import SimpleNamespace

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from starlette.testclient import TestClient

import auth
import server


@pytest.fixture
def http_server(monkeypatch):
    # FastMCP's stateful session manager is single-use; give every test a fresh app.
    app_server = importlib.reload(server)
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    monkeypatch.setattr(app_server.verifier, 'jwks_client', SimpleNamespace(
        get_signing_key_from_jwt=lambda token: SimpleNamespace(key=key.public_key())))
    with TestClient(app_server.mcp.streamable_http_app(), base_url='http://127.0.0.1:8000') as client:
        yield client, key, app_server


def token(key, scope='tickets.read policies.read', **overrides):
    now = int(time.time())
    claims = {'iss': auth.ISSUER, 'aud': auth.RESOURCE, 'sub': 'ayse-http-test',
              'azp': auth.CLIENT_ID, 'iat': now, 'exp': now + 300, 'scope': scope}
    return jwt.encode({**claims, **overrides}, key, algorithm='RS256',
                      headers={'typ': 'at+jwt', 'kid': 'http-test'})


def headers(bearer=None, session=None):
    result = {'Accept': 'application/json, text/event-stream', 'Content-Type': 'application/json'}
    if bearer:
        result['Authorization'] = f'Bearer {bearer}'
    if session:
        result['mcp-session-id'] = session
        result['MCP-Protocol-Version'] = '2025-11-25'
    return result


def parse(response):
    if response.headers.get('content-type', '').startswith('application/json'):
        return response.json()
    events = [json.loads(line[6:]) for line in response.text.splitlines() if line.startswith('data: ')]
    return events[-1]


def initialize(client, bearer):
    response = client.post('/mcp', headers=headers(bearer), json={
        'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {
            'protocolVersion': '2025-11-25', 'capabilities': {},
            'clientInfo': {'name': 'authorization-test', 'version': '1'},
        }})
    assert response.status_code == 200, response.text
    assert 'result' in parse(response)
    session = response.headers['mcp-session-id']
    response = client.post('/mcp', headers=headers(bearer, session), json={
        'jsonrpc': '2.0', 'method': 'notifications/initialized'})
    assert response.status_code == 202
    return session


def invoke(client, bearer, session, name, arguments):
    response = client.post('/mcp', headers=headers(bearer, session), json={
        'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call',
        'params': {'name': name, 'arguments': arguments}})
    assert response.status_code == 200, response.text
    return parse(response)['result']


@pytest.mark.parametrize('bad_token', ['missing', 'malformed', 'expired', 'wrong-audience'])
def test_http_rejects_bad_credentials(http_server, bad_token):
    client, key, _ = http_server
    bearer = {'missing': None, 'malformed': 'invalid', 'expired': token(key, exp=1),
              'wrong-audience': token(key, aud='another-service')}[bad_token]
    response = client.post('/mcp', headers=headers(bearer), json={
        'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {}})
    assert response.status_code == 401
    assert response.headers['www-authenticate'].startswith('Bearer')


def test_read_token_calls_real_ticket_tool(http_server):
    client, key, _ = http_server
    bearer = token(key)
    result = invoke(client, bearer, initialize(client, bearer), 'get_ticket', {'ticket_id': 'T-1003'})
    assert not result['isError']
    ticket = json.loads(result['content'][0]['text'])
    assert ticket['id'] == 'T-1003'
    assert 'error' not in ticket
    assert ticket['subject'] == 'Refund not received'


def test_ayse_refund_is_denied_before_business_logic(http_server, monkeypatch):
    client, key, app_server = http_server
    monkeypatch.setattr(app_server, 'refund_inputs', lambda *a: pytest.fail('Scope check must run first'))
    bearer = token(key)
    result = invoke(client, bearer, initialize(client, bearer), 'issue_refund', {'ticket_id': 'T-1003', 'amount': '10'})
    assert result['isError']
    assert 'tickets.refund' in result['content'][0]['text']


def test_policy_requires_own_scope(http_server):
    client, key, _ = http_server
    bearer = token(key, scope='tickets.read')
    result = invoke(client, bearer, initialize(client, bearer), 'get_policy', {'policy_id': 'POL-REFUND-03'})
    assert result['isError']
    assert 'policies.read' in result['content'][0]['text']


def test_refund_without_elicitation_support_never_executes(http_server):
    client, key, app_server = http_server
    bearer = token(key, scope='tickets.refund', sub='60e1641b-48cb-4886-a0ef-10c742cfebe8')
    result = invoke(client, bearer, initialize(client, bearer), 'issue_refund', {'ticket_id':'T-1003','amount':'10','confirmed':True})
    assert result['isError']
    assert app_server.ledger.records == ()
