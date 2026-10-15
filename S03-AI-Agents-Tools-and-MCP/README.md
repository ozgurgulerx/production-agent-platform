# S03: AI Agents Tools and MCP

This section follows a Python function from a direct call to an MCP tool, then
to a tool an LLM agent can select. It is the current starting point in the
[AI Production Systems curriculum](../README.md).

## Learning order

| Subsection | What it covers | Verification at migration |
| --- | --- | --- |
| [S03.01: Python Functions](S03.01-Python-Functions/README.md) | Read ticket data and practise lookup, filtering, and aggregation | 5 tests pass; 100% coverage; existing lint/format failures |
| [S03.02: Functions to MCP Tools](S03.02-Functions-to-MCP-Tools/README.md) | Expose functions through FastMCP, test the MCP interface, inspect calls, and connect an OpenAI Agents SDK agent | 16 tests pass; 76.47% coverage, below the required 80%; existing lint/format failures |

Start with S03.01, then continue to S03.02. Each project has its own source,
fixtures, tests, manifest, and lockfile. Detailed explanations, commands, and
Inspector screenshots stay in the project READMEs.

## Running the projects

Run commands from the subsection folder. From S03.02, for example:

```bash
../../.venv/bin/python -m pytest -v
```

The shared root `.venv` is two levels above either project. The MCP server and
agent still expect their working directory to be S03.02, where `data/` and `src/`
are located. See the [root environment instructions](../README.md#python-environment)
for installation.

## Current limits

S03.02 includes one successful live agent run, but automated agent tests remain
pending. The directory migration does not fix the existing coverage gap, lint
issues, or missing stage-local agent dependency. No model requests are needed to
verify the move.

S03.01 was previously R0 (`r0-python-recap-functions`); S03.02 was previously R1
(`r1-functions-to-mcp-tools`). Those names may appear in older learning records.
