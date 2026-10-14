FROM ghcr.io/astral-sh/uv:0.9-python3.12-bookworm-slim AS build
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project
COPY src ./src
COPY data ./data
RUN uv sync --frozen --no-dev

FROM python:3.12-slim-bookworm
RUN useradd --create-home app
WORKDIR /app
COPY --from=build --chown=app:app /app /app
ENV PATH="/app/.venv/bin:$PATH" TICKETS_DATA_DIR=/app/data PYTHONUNBUFFERED=1
USER app
# Stdio MCP server: attach with `docker run -i`; logs go to stderr.
CMD ["python", "-m", "pap.tools.server"]
