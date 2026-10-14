# production-agent-platform

A hands-on Python-to-agent engineering learning path. The learner writes every function and test; scaffolds provide contracts, synthetic data, and reproducible environments.

- [R0 — Python recap: functions](r0-python-recap-functions/README.md): ready to start.
- [R1 — Functions to MCP tools](r1-functions-to-mcp-tools/README.md): using FastMCP to expose python functions as explorable tools...

Each stage is self-contained. Start in R0 and follow its README. Empty source files and test folders are intentional: passing scaffold checks does not verify functionality.

The future roadmap is R2 bounded agent, R3 retrieval and evals, R4 orchestration and human approval, R5 API and OAuth, R6 observability, R7 Azure deployment, R8 architecture and governance, R9 release, and R10 Bedrock. These stages are planned, with no folders or implementations yet.

## Python packages

[requirements.txt](requirements.txt) lists OpenAI Agents SDK, Microsoft Agent Framework, FastMCP, MCP, Pydantic, and our testing and linting tools. Install them into the root virtual environment from this folder:

```bash
uv pip install --python .venv/bin/python -r requirements.txt
```

Activate the shared environment from the repository root:

```bash
source .venv/bin/activate
cd r1-functions-to-mcp-tools  # or r0-python-recap-functions
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

The environment stays active when you change folders. Use `python` and `python -m pytest` while it is active; plain `uv run` inside a stage selects that stage's environment instead. Run `deactivate` to exit.

This is an unpinned package list for the shared local environment. Each stage retains its `pyproject.toml` and `uv.lock` for isolated CI checks.
