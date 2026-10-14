# R1 — Ticket functions as MCP tools (Day 1)


We will now be exposing python functions as mcp tools via an mcp server.
The larger task is (imaginary scenario) building an ops agent for a financial company and initially will be focusing on the "refunds agent."

- [ ] write the functions as per their specs below
- [ ] test the functions with pytest 
- [ ] expose the functions with mcp as tools 



### What functions we will build...
**list_tickets** — the agent’s way to find tickets without knowing an id. Takes optional filters (status, customer, maybe a tag) and returns a compact list: id, subject, status, customer, created date — enough to pick one, not the whole record, because the model will read every returned token. An empty match returns an empty list, not an error.

**get_ticket** — one ticket in full by id: the summary fields plus the refund-relevant ones (amount disputed, refund status, which policy it references). An unknown id comes back as a clean “not found” error the model can act on, never a raised exception that kills the run. Customer card and NI fields are either absent from the data this tool reads or stripped here, so no later stage can leak them.

**get_policy** — one policy document by id, returned as text with its id and title, so the agent can quote it when it answers “which policy applies”. Unknown id → the same clean error shape as get_ticket.

Ok, once done - test the functions with tests/test_functions.py

====
