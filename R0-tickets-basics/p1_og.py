import json 
import string 
total_disputed = 0

def load_tickets():
    with open("tickets.json") as file:
        tickets = json.load(file)
    return(tickets)

def open_tickets(tickets):
    open_ticket_ids = []
    for ticket in tickets:
        if (ticket["status"] == "open"):
            open_ticket_ids.append(ticket["id"])
    return open_ticket_ids

def total_disputed(tickets):
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
            ticket_ids_for_customer.append(ticket["id"])
    return ticket_ids_for_customer



print(open_tickets(load_tickets()))
print(total_disputed(load_tickets()))
print(tickets_for_customer(load_tickets(), "C-42"))






        
        

