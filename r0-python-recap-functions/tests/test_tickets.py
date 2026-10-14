from pathlib import Path

from tickets import (count_by_priority, load_tickets, open_ticket_ids,
                     tickets_for_customer, total_disputed)

SAMPLE = Path(__file__).resolve().parent.parent / "data" / "tickets.json"


def test_load_returns_eight_dicts():
    t = load_tickets(SAMPLE)
    assert len(t) == 8 and t[0]["id"] == "T-1001"


def test_count_by_priority_worked_example():
    assert count_by_priority(load_tickets(SAMPLE)) == {"high": 3, "low": 2, "urgent": 1, "medium": 2}


def test_open_ticket_ids():
    assert open_ticket_ids(load_tickets(SAMPLE)) == ["T-1001", "T-1003", "T-1006", "T-1008"]


def test_total_disputed_treats_missing_as_zero():
    assert total_disputed(load_tickets(SAMPLE)) == 465.75


def test_tickets_for_customer():
    got = tickets_for_customer(load_tickets(SAMPLE), "C-42")
    assert [t["id"] for t in got] == ["T-1001", "T-1003", "T-1008"]
    assert tickets_for_customer(load_tickets(SAMPLE), "C-00") == []
