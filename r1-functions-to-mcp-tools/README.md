# R1 — Functions to MCP tools

Turn your completed R0 functions into three read-only MCP tools. R1 is scaffolded and follows R0. Copy your own completed `functions.py` and relevant tests from R0 into this folder, then write `src/server.py` and all new tests yourself. Both source files start empty. This stage has its own fixture copies, environment, and lockfile; it must run without importing another stage.

## Start

From this folder, run `uv sync --frozen` using Python 3.12 or later. Keep imports from `src`; use `uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=80`, `uv run ruff check .`, and `uv run ruff format --check .`. The environment includes MCP 2.x, Pydantic, and pytest-asyncio. Learn the installed SDK's server and in-memory testing APIs before implementing the adapter.

## Function contracts

Write these four functions yourself in `src/functions.py`. Only `load_json` accepts a fixture path; the other functions accept loaded records. Keep filesystem locations out of the business logic. Use UTF-8 and do not modify files or input records.

- `load_json(path)` reads a JSON file and returns a list of dictionaries in file order, preserving all fields. An empty list is valid. Let `FileNotFoundError` identify a missing file and `json.JSONDecodeError` identify malformed JSON. Raise `ValueError` if the top-level value is not a list or any item is not an object.
- `list_tickets(tickets, status=None, limit=10)` returns a new list of summaries containing exactly `id`, `priority`, `status`, and `subject`. With no status, include all tickets; otherwise filter by exactly `open`, `pending`, or `closed`. Filter before limiting and preserve file order. Accept integer limits from 1 through 50 inclusive; reject booleans, non-integers, out-of-range limits, and unsupported statuses with `ValueError`. Fewer matches return fewer results; no matches return an empty list.
- `get_ticket(tickets, ticket_id)` returns an independent copy of the entire matching record, including optional and nested fields such as `tags`. Editing a nested field in the result must not change the input record. Require a nonblank string ID; invalid IDs raise `ValueError`. Match IDs exactly without trimming or changing case. An unknown ID raises `KeyError` with a readable message. Fixture IDs are unique.
- `get_policy(policies, policy_id)` follows the same ID and missing-record rules and returns the full policy record (`id`, `title`, `text`) as an independent copy.

For examples, the supplied tickets filtered to `open` with limit 2 produce summaries for `T-1001` then `T-1003`. Looking up `T-1001` includes its `tags` and `amount_disputed`. Looking up `POL-REFUND-01` returns its title and complete policy text. `T-9999` and `POL-UNKNOWN` are missing records.

## MCP boundary contracts

Expose exactly `list_tickets`, `get_ticket`, and `get_policy` as read-only tools. Keep the plain Python functions independently testable. The adapter loads this stage's fixtures and calls your functions; tools neither accept filesystem paths nor change records. Use typed Pydantic boundary models for inputs and structured outputs, retaining full ticket fields for lookup results. Enforce the status and limit rules at the boundary too; ensure booleans cannot pass as integer limits.

Translate expected validation, missing-record, and fixture-loading failures into readable `ToolError` responses without leaking stack traces or local paths. Log operational diagnostics to stderr, keeping stdout reserved for the MCP protocol. Advertise read-only tool annotations. Use no API keys, credentials, external accounts, or model calls.

For example, an MCP call to `list_tickets` with status `open` and limit 2 has the same ordered summaries as R0; `get_ticket` with ID `T-1001` preserves the optional fields; `get_policy` with ID `POL-REFUND-01` returns the full policy. Unknown IDs produce readable tool errors.

## Tests and manual check

Carry forward the R0 edge checks, then write in-memory client/server tests for tool discovery, input/output schemas, each successful call, invalid status, limits 0 and 51, booleans, blank/non-string IDs, unknown IDs, and fixture failures. Check that errors are usable by clients and diagnostics stay off stdout. Include a full lookup with optional fields and prove calls cannot mutate stored records. Finish with all tests passing, at least 80% coverage, and lint/format checks passing.

Use MCP Inspector against your local stdio server for a manual discovery-and-call check. Choose the Inspector launch command for the installed SDK; it should launch this stage's server from this folder and require no credentials. Record what you actually checked. Until you write tests, pytest exits 5: scaffold only—functionality unverified.
