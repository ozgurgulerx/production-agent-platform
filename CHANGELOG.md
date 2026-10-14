# Changelog

All notable changes to this repo, newest first. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). One line per shipped thing; each line should be traceable to a commit or tag.

## [Unreleased]

### Added
- S0 scaffold: root uv project (ruff, mypy strict, pytest, pre-commit), CI, Dockerfile, Makefile, ADR-0001, stage table and prompts in `docs/prompts/`.
- S1 server shell in `src/pap/tools/` with 8 contract tests; tool bodies deliberately unwritten (Ozgur writes them).
- Engineering log (`docs/log/`) and this changelog.

### Changed
- `CLAUDE.md` replaced with the platform version (division of labour, workflow, standards); journal rules kept.
- R1-tickets-mcp moved into `src/pap/tools/` and `data/`; the old folder is git-ignored.

### Known gaps
- Docker image build and CI have not been run; Inspector screenshots not captured.
- `R0-tickets-basics/` still here until `python-reps` exists.

## [R0] - 2026-10-13

### Added
- R0: tickets basics, `src/tickets.py` with 5 passing pytest tests (commit `53e7b7b`).
- Root tooling: MCP Inspector pinned at 2.10.1 (`npm run inspector`).
