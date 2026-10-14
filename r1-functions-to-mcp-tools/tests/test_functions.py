from functions import get_ticket
from functions import get_policy
from functions import list_tickets

def test_get_ticket_found():
    ticket = get_ticket("T-1001")
    assert ticket["id"] == "T-1001"


def test_get_policy():
    policy = get_policy("POL-DATA-01")
    assert policy["id"] == "POL-DATA-01"



def test_list_open_tickets():
      result = list_tickets(status="open")

      assert len(result) == 4

      for ticket in result:
          assert ticket["status"] == "open"
