-- G04 lab 03: the tickets table the ticketing MCP server reads. Used by lab 02 (local Postgres) and lab 03 (Cloud SQL).
CREATE TABLE IF NOT EXISTS tickets (
    id         INTEGER PRIMARY KEY,
    customer   TEXT        NOT NULL,   -- matches the `sub` claim of the signed-in user for my_open_tickets (map D7)
    status     TEXT        NOT NULL CHECK (status IN ('open', 'pending', 'closed')),
    amount     NUMERIC(10, 2) NOT NULL DEFAULT 0,
    opened_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO tickets (id, customer, status, amount, opened_at) VALUES
    (1001, 'cust-alpha', 'closed',  19.99, now() - interval '70 days'),
    (1002, 'cust-alpha', 'open',    42.00, now() - interval '3 days'),
    (1003, 'cust-beta',  'open',   250.00, now() - interval '12 days'),
    (1004, 'cust-beta',  'pending', 35.50, now() - interval '45 days'),
    (1005, 'cust-gamma', 'open',     9.00, now() - interval '1 day'),
    -- rows the G05 lab 02 evalset and G06 lab 01 assume: outside and inside the 30-day refund window
    (1042, 'cust-delta', 'open',    59.00, now() - interval '90 days'),
    (1043, 'cust-delta', 'open',    24.00, now() - interval '10 days')
ON CONFLICT (id) DO NOTHING;
