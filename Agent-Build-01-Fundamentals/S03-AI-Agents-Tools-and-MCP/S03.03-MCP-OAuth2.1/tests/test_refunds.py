from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from check_refund_policy import check_refund_policy
from refunds import RefundLedger

PRINCIPAL = {'team': 'payments'}
TICKET = {'id': 'T-1003', 'team': 'payments', 'currency': 'GBP', 'refundable_balance': '1000.00'}

@pytest.mark.parametrize('amount,error', [('0','invalid_amount'),('-1','invalid_amount'),('NaN','invalid_amount'),('Infinity','invalid_amount'),('0.001','invalid_amount'),('501','execution_limit_exceeded')])
def test_policy_rejects_amount(amount,error):
    with pytest.raises(ValueError,match=error):
        check_refund_policy(PRINCIPAL,TICKET,amount)

def test_policy_accepts_boundary():
    assert check_refund_policy(PRINCIPAL,TICKET,'500') == Decimal('500')

@pytest.mark.parametrize('principal,ticket,error', [({},TICKET,'team_mismatch'),({'team':'accounts'},TICKET,'team_mismatch'),(PRINCIPAL,{**TICKET,'refundable_balance':'10'},'insufficient_balance'),(PRINCIPAL,{**TICKET,'currency':'USD'},'unsupported_currency')])
def test_policy_rejects_business_failures(principal,ticket,error):
    with pytest.raises(ValueError,match=error):
        check_refund_policy(principal,ticket,'20')

def test_ledger_rechecks_balance_and_records_once():
    ledger = RefundLedger()
    result = ledger.execute('subject',PRINCIPAL,{**TICKET,'refundable_balance':'100'},'70')
    assert result['remaining_balance'] == '30.00'
    with pytest.raises(ValueError,match='insufficient_balance'):
        ledger.execute('subject',PRINCIPAL,{**TICKET,'refundable_balance':'100'},'70')
    assert len(ledger.records) == 1


def test_parallel_refunds_cannot_overspend():
    from concurrent.futures import ThreadPoolExecutor
    ledger = RefundLedger()
    ticket = {**TICKET, 'refundable_balance':'100'}
    def attempt():
        try:
            return ledger.execute('subject',PRINCIPAL,ticket,'70')['status']
        except ValueError:
            return 'rejected'
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(lambda _:attempt(),range(2))) == ['rejected','simulated_refund']
    assert len(ledger.records) == 1
