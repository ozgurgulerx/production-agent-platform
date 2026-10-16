"""Pure policy for the simulated GBP refund tool."""
from decimal import Decimal, InvalidOperation


def check_refund_policy(principal, ticket, amount):
    try:
        value = Decimal(str(amount))
        if not value.is_finite() or value <= 0 or value.as_tuple().exponent < -2:
            raise ValueError('invalid_amount')
    except InvalidOperation:
        raise ValueError('invalid_amount') from None
    if value > 500:
        raise ValueError('execution_limit_exceeded')
    if not principal.get('team') or principal['team'] != ticket.get('team'):
        raise ValueError('team_mismatch')
    if ticket.get('currency') != 'GBP':
        raise ValueError('unsupported_currency')
    try:
        balance = Decimal(str(ticket.get('refundable_balance')))
    except InvalidOperation:
        raise ValueError('invalid_balance') from None
    if not balance.is_finite() or balance < 0:
        raise ValueError('invalid_balance')
    if value > balance:
        raise ValueError('insufficient_balance')
    return value
