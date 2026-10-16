import pytest
from src.check_refund_policy import check_refund_policy

def test_refund_above_execution_limit_is_rejected():
    with pytest.raises(ValueError, match="execution_limit_exceeded"):
        check_refund_policy(None,None,600)
    # Call your function here with an amount of 600.

