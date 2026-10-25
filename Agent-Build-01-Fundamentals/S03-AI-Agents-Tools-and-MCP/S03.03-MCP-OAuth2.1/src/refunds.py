"""Process-local simulated ledger. Restarting the server resets all refunds."""
from dataclasses import dataclass
from decimal import Decimal
from threading import Lock
from uuid import uuid4

from check_refund_policy import check_refund_policy


@dataclass(frozen=True)
class Refund:
    id: str
    ticket_id: str
    subject: str
    amount: Decimal


class RefundLedger:
    def __init__(self):
        self._records: tuple[Refund, ...] = ()
        self._lock = Lock()

    @property
    def records(self):
        return self._records

    def _current_ticket(self, ticket):
        spent = sum((r.amount for r in self._records if r.ticket_id == ticket['id']), Decimal('0'))
        return {**ticket, 'refundable_balance': str(Decimal(str(ticket['refundable_balance'])) - spent)}

    def check(self, principal, ticket, amount):
        with self._lock:
            return check_refund_policy(principal, self._current_ticket(ticket), amount)

    def execute(self, subject, principal, ticket, amount):
        # Recheck under the same lock as recording: confirmations may overlap.
        with self._lock:
            current = self._current_ticket(ticket)
            value = check_refund_policy(principal, current, amount)
            record = Refund(str(uuid4()), ticket['id'], subject, value)
            self._records = (*self._records, record)
            return {
                'status': 'simulated_refund', 'refund_id': record.id,
                'ticket_id': ticket['id'], 'amount': f'{value:.2f}', 'currency': 'GBP',
                'remaining_balance': f"{Decimal(current['refundable_balance']) - value:.2f}",
            }
