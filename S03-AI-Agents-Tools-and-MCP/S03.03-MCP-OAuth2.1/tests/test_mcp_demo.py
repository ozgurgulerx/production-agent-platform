import asyncio
from contextlib import asynccontextmanager
from types import SimpleNamespace

import pytest
from mcp import types

import mcp_demo


def request(schema=None):
    return types.ElicitRequestFormParams(message='Refund GBP 100 for ticket T1003?', requestedSchema=schema or {
        'title': 'RefundConfirmation', 'type': 'object',
        'properties': {'confirm': {'title': 'Confirm', 'type': 'boolean'}},
        'required': ['confirm'],
    })


@pytest.mark.parametrize('answer,action', [('YES', 'accept'), ('yes', 'decline'), (' YES', 'decline'), ('', 'decline'), ('no', 'decline')])
def test_confirmation_requires_explicit_exact_yes(monkeypatch, answer, action):
    prompts = []
    def respond(prompt):
        prompts.append(prompt)
        return answer
    monkeypatch.setattr('builtins.input', respond)
    result = asyncio.run(mcp_demo.confirm_refund(None, request()))
    assert result.action == action
    assert result.content == ({'confirm': True} if action == 'accept' else None)
    assert 'Refund GBP 100 for ticket T1003?' in prompts[0]


def test_eof_cancels(monkeypatch):
    def eof(prompt):
        raise EOFError
    monkeypatch.setattr('builtins.input', eof)
    assert asyncio.run(mcp_demo.confirm_refund(None, request())).action == 'cancel'


@pytest.mark.parametrize('schema', [
    {'type': 'object', 'properties': {}},
    {'type': 'object', 'properties': {'confirm': {'type': 'string'}}, 'required': ['confirm']},
    {'type': 'object', 'properties': {'confirm': {'type': 'boolean'}, 'secret': {'type': 'string'}}, 'required': ['confirm']},
    {'type': 'object', 'properties': {'confirm': {'type': 'boolean'}}, 'required': []},
    {'type': 'array', 'properties': {'confirm': {'type': 'boolean'}}, 'required': ['confirm']},
])
def test_unknown_schema_cancels_without_prompt(monkeypatch, schema):
    monkeypatch.setattr('builtins.input', lambda p: pytest.fail('Must not prompt'))
    assert asyncio.run(mcp_demo.confirm_refund(None, request(schema))).action == 'cancel'


def test_unknown_mode_cancels(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda p: pytest.fail('Must not prompt'))
    params = types.ElicitRequestURLParams(message='Open URL', url='https://example.com', elicitationId='e1')
    assert asyncio.run(mcp_demo.confirm_refund(None, params)).action == 'cancel'


@pytest.mark.parametrize('is_error', [False, True])
def test_call_tool_uses_bearer_and_initializes(monkeypatch, is_error):
    events = []
    @asynccontextmanager
    async def transport(url, headers):
        assert url == mcp_demo.RESOURCE
        assert headers == {'Authorization': 'Bearer fake-test-token'}
        events.append('transport')
        yield ('read', 'write', lambda: 'session')
    class Session:
        def __init__(self, read, write, elicitation_callback):
            assert (read, write) == ('read', 'write')
            assert elicitation_callback is mcp_demo.confirm_refund
        async def __aenter__(self):
            return self
        async def __aexit__(self, *args):
            events.append('close')
        async def initialize(self):
            events.append('initialize')
        async def call_tool(self, name, arguments):
            assert name == 'get_ticket'
            assert arguments == {'ticket_id': 'T1003'}
            events.append('call')
            return types.CallToolResult(content=[types.TextContent(type='text', text='demo')], isError=is_error)
    monkeypatch.setattr(mcp_demo, 'streamablehttp_client', transport)
    monkeypatch.setattr(mcp_demo, 'ClientSession', Session)
    result = asyncio.run(mcp_demo.call_tool('fake-test-token', 'get_ticket', {'ticket_id': 'T1003'}))
    assert result['isError'] is is_error
    assert events == ['transport', 'initialize', 'call', 'close']
