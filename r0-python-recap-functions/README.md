# R0 — Python recap: functions

Practise file reading, lists, dictionaries, filtering, validation, exceptions, and tests with synthetic support tickets and policies. This stage is ready to start; `src/functions.py` is deliberately empty and you write every function and test. No solution or test implementation is supplied.

## Start

From this folder, run `source ../.venv/bin/activate` to use the shared root environment (see the root README for installation). Write tests in `tests/`, implement the contracts below, and run `python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80`. Imports resolve from `src`, so tests can import `functions`. Run `python -m ruff check .` and `python -m ruff format --check .` before recording progress.

## Function contracts

Write these four functions yourself in `src/functions.py`. Only `load_json` accepts a fixture path; the other functions accept loaded records. Keep filesystem locations out of the business logic. Use UTF-8 and do not modify files or input records.

- `load_json(path)` reads a JSON file and returns a list of dictionaries in file order, preserving all fields. An empty list is valid. Let `FileNotFoundError` identify a missing file and `json.JSONDecodeError` identify malformed JSON. Raise `ValueError` if the top-level value is not a list or any item is not an object.
- `list_tickets(tickets, status=None, limit=10)` returns a new list of summaries containing exactly `id`, `priority`, `status`, and `subject`. With no status, include all tickets; otherwise filter by exactly `open`, `pending`, or `closed`. Filter before limiting and preserve file order. Accept integer limits from 1 through 50 inclusive; reject booleans, non-integers, out-of-range limits, and unsupported statuses with `ValueError`. Fewer matches return fewer results; no matches return an empty list.
- `get_ticket(tickets, ticket_id)` returns an independent copy of the entire matching record, including optional and nested fields such as `tags`. Editing a nested field in the result must not change the input record. Require a nonblank string ID; invalid IDs raise `ValueError`. Match IDs exactly without trimming or changing case. An unknown ID raises `KeyError` with a readable message. Fixture IDs are unique.
- `get_policy(policies, policy_id)` follows the same ID and missing-record rules and returns the full policy record (`id`, `title`, `text`) as an independent copy.

For examples, the supplied tickets filtered to `open` with limit 2 produce summaries for `T-1001` then `T-1003`. Looking up `T-1001` includes its `tags` and `amount_disputed`. Looking up `POL-REFUND-01` returns its title and complete policy text. `T-9999` and `POL-UNKNOWN` are missing records.

## Tests to write

Cover both fixture files and temporary files: empty lists, missing files, malformed JSON, wrong top-level types, and non-object items. Check default listing, every status, file order, filtering before limiting, exact summary keys, limits 1 and 50, and invalid limits (including `True`) and statuses. Check full records with optional fields, exact IDs, invalid IDs, unknown IDs, empty inputs, and that returned results do not change the original records when edited.

Finish when your own tests pass with at least 80% coverage and lint/format checks pass. Until you write tests, pytest exits 5: scaffold only—functionality unverified. Continue to R1 after completing this stage.
