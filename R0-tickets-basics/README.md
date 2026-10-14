# R0 — tickets basics (rung 0, 25 minutes, no AI during the timer)

## What you are doing
Four small functions over a list of support tickets read from a JSON file. No classes, no
pydantic, no validation. Plain Python: open a file, loop over a list, count things, filter
things, add things up.

One of the four is already written for you (`count_by_priority`) so you can see the shape.
You write the other three. The tests tell you exactly what each must return.

## Rules
- 25 minutes on a timer. Editor, pytest and docs.python.org only. No AI while the timer runs.
- When the timer ends (green or not): commit on branch `r0/tickets-basics`, then — and only then —
  ask Claude Code to review your diff and explain one thing you were unsure of (15 min).
  That review is your AI-dev block for the day.
- Log in Python Daily: start time, time to first `pytest` run, time to green (or "not green"),
  the one thing you looked up.

## Steps
1. `cd R0-tickets-basics`, `pip install pytest` (or `uv sync`), `pytest -q` → 3 fail, 2 pass.
   Start the timer.
2. Open `src/tickets.py`. Read `count_by_priority` — it is the pattern for all three.
3. Write `open_ticket_ids`, `total_disputed`, `tickets_for_customer`. Run `pytest -q` after each.
4. Green → commit → log → Claude Code review.

## The data (tickets.json, 8 rows, all valid)
```json
{"id": "T-1001", "customer_id": "C-42", "created_at": "2026-10-01T09:15:00+00:00",
 "priority": "high", "status": "open", "subject": "Card declined twice",
 "tags": ["payments", "card"], "amount_disputed": 120.5}
```
`tags` and `amount_disputed` are sometimes missing. Use `.get()` with a default.

## Hints (read only if stuck)
- `json.load(f)` on an open file gives you the list.
- A list comprehension with an `if` is a filter: `[t["id"] for t in tickets if ...]`.
- `sum(... for t in tickets)` adds things up; `t.get("amount_disputed", 0)` handles the missing key.
