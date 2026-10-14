.PHONY: test lint run-mcp inspector

test:
	uv run pytest -q

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy

run-mcp:
	uv run python -m pap.tools.server

inspector:
	npx @modelcontextprotocol/inspector uv run python -m pap.tools.server
