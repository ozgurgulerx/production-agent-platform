import pytest
from src.check_refund_policy import check_refund_policy

def test_refund_at_execution_limit_is_allowed():
    check_refund_policy({'team': 'payments'}, {'team': 'payments', 'currency': 'GBP', 'refundable_balance': '1000.00'},500)
