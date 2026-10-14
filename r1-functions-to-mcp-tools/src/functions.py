
import json 

def load_json(path):
    #create a list of dictionaries ticket we will iterate over
    with open(path) as file:
        return json.load(file)

def list_tickets(status=None, customer_id=None):

    results = []
    tickets = load_json("data/tickets.json")
    for ticket in tickets:
        if status is not None and ticket["status"] != status:
            continue

        if customer_id is not None and ticket["customer_id"] != customer_id:
            continue

        results.append({
            "id": ticket["id"],
            "subject": ticket["subject"],
            "status": ticket["status"],
            "customer_id": ticket["customer_id"],
            "created_at": ticket["created_at"],
        })
    return results


def get_ticket(ticket_id):
   tickets = load_json("data/tickets.json")
   for ticket in tickets:
       if ticket["id"] == ticket_id:
           return ticket
   return {"error": "not_found", "id": ticket_id}

def get_policy(policy_id):
    policies = load_json("data/policies.json")
    for policy in policies:
        if policy["id"] == policy_id:
            return policy
    return {"error": "not_found", "id": policy_id}