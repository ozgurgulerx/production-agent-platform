import pytest
from src.check_refund_policy import check_refund_policy

def test_refund_at_execution_limit_is_allowed():
    check_refund_policy(None,None,500)
