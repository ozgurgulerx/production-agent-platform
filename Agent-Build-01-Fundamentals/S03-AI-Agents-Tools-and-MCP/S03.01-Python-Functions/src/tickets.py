"""S03.01 — tickets basics. Plain Python over a list of dicts."""
import json
from pathlib import Path


def load_tickets(path):
    """Read the JSON file at `path` and return the list of ticket dicts."""
    with open(Path(path)) as f:
        return json.load(f)


def count_by_priority(tickets):
    """WORKED EXAMPLE. {"high": 3, "low": 2, ...} — how many tickets per priority."""
    counts = {}
    for t in tickets:
        p = t["priority"]
        counts[p] = counts.get(p, 0) + 1
    return counts


def open_ticket_ids(tickets):
    """Return the ids (strings) of tickets whose status is "open", in file order."""
    open_ticket_ids = []
    for ticket in tickets:
        if (ticket["status"] == "open"):
            open_ticket_ids.append(ticket["id"])
    return open_ticket_ids


def total_disputed(tickets):
    """Sum of amount_disputed over all tickets; a ticket without the key counts as 0."""
    total_disputed_sum = 0
    for ticket in tickets:
        if "amount_disputed" in ticket:
            total_disputed_sum += ticket["amount_disputed"]
    return total_disputed_sum

def tickets_for_customer(tickets, customer_id):
    ticket_ids_for_customer=[]
    for ticket in tickets:
        print(ticket)
        if (ticket["customer_id"]== customer_id):
            ticket_ids_for_customer.append(ticket)
    return ticket_ids_for_customer