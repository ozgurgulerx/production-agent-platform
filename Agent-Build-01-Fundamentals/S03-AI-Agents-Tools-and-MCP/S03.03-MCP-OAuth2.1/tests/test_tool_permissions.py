import time
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from mcp.server.fastmcp.exceptions import ToolError
import auth
import server
from refunds import RefundLedger


def context(elicit):
    capabilities = SimpleNamespace(elicitation=SimpleNamespace(form={}))
    session = SimpleNamespace(client_params=SimpleNamespace(capabilities=capabilities))
    return SimpleNamespace(elicit=elicit, request_context=SimpleNamespace(session=session))


@pytest.fixture
def authorized(monkeypatch):
    token = auth.VerifiedAccessToken(token='test-only', client_id=auth.CLIENT_ID, subject='60e1641b-48cb-4886-a0ef-10c742cfebe8', scopes=['tickets.refund','tickets.read','policies.read'], expires_at=int(time.time())+300, resource=auth.RESOURCE)
    monkeypatch.setattr(auth,'get_access_token',lambda:token)
    monkeypatch.setattr(server,'ledger',RefundLedger())
    return token

@pytest.mark.parametrize('action,confirm', [('decline',None),('cancel',None),('accept',False)])
async def test_no_refund_without_confirmation(authorized, action, confirm):
    data = None if confirm is None else server.RefundConfirmation(confirm=confirm)
    ctx=context(elicit=AsyncMock(return_value=SimpleNamespace(action=action,data=data)))
    result=await server.issue_refund('T-1003','100.00',ctx)
    assert result['status']=='not_executed'
    assert server.ledger.records == ()

async def test_accept_records_simulated_refund(authorized):
    ctx=context(elicit=AsyncMock(return_value=SimpleNamespace(action='accept',data=server.RefundConfirmation(confirm=True))))
    result=await server.issue_refund('T-1003','100.00',ctx)
    assert result['remaining_balance']=='200.00'
    assert len(server.ledger.records)==1

async def test_unsupported_confirmation_fails_closed(authorized):
    ctx=context(elicit=AsyncMock(side_effect=RuntimeError('unsupported')))
    with pytest.raises(ToolError,match='confirmation unavailable'):
        await server.issue_refund('T-1003','100',ctx)
    assert server.ledger.records == ()

async def test_expired_while_waiting_never_records(authorized,monkeypatch):
    async def answer(**kwargs):
        monkeypatch.setattr(auth,'get_access_token',lambda:authorized.model_copy(update={'expires_at':1}))
        return SimpleNamespace(action='accept',data=server.RefundConfirmation(confirm=True))
    with pytest.raises(ToolError,match='expired'):
        await server.issue_refund('T-1003','100',context(elicit=answer))
    assert server.ledger.records == ()

@pytest.mark.parametrize('ticket,amount,error', [('T-1010','100','team_mismatch'),('T-1009','600','execution_limit_exceeded'),('T-1003','400','insufficient_balance'),('T-1001','10','not eligible'),('missing','10','not eligible')])
async def test_policy_denied_before_prompt(authorized,ticket,amount,error):
    ctx=context(elicit=AsyncMock())
    with pytest.raises(ToolError,match=error):
        await server.issue_refund(ticket,amount,ctx)
    ctx.elicit.assert_not_called()
    assert server.ledger.records == ()

async def test_balance_rechecked_after_confirmation(authorized):
    async def answer(**kwargs):
        principal,ticket=server.refund_inputs(authorized.subject,'T-1003')
        server.ledger.execute(authorized.subject,principal,ticket,'250')
        return SimpleNamespace(action='accept',data=server.RefundConfirmation(confirm=True))
    with pytest.raises(ToolError,match='insufficient_balance'):
        await server.issue_refund('T-1003','100',context(elicit=answer))
    assert len(server.ledger.records)==1

async def test_unknown_subject_has_no_team(authorized,monkeypatch):
    monkeypatch.setattr(auth,'get_access_token',lambda:authorized.model_copy(update={'subject':'unknown'}))
    with pytest.raises(ToolError,match='trusted team'):
        await server.issue_refund('T-1003','100',context(elicit=AsyncMock()))

@pytest.mark.parametrize('name,args,scope',[('get_ticket',('T-1003',),'tickets.read'),('list_tickets',(),'tickets.read'),('get_policy',('POL-REFUND-01',),'policies.read')])
def test_read_scope_enforced(authorized,monkeypatch,name,args,scope):
    assert getattr(server,name)(*args)
    monkeypatch.setattr(auth,'get_access_token',lambda:authorized.model_copy(update={'scopes':[]}))
    with pytest.raises(ToolError,match=scope):
        getattr(server,name)(*args)

async def test_confirmed_argument_not_a_bypass(authorized):
    with pytest.raises(TypeError):
        await server.issue_refund('T-1003','100',context(elicit=AsyncMock()),confirmed=True)
    assert server.ledger.records == ()
