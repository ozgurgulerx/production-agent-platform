# S03: AI Agents Tools and MCP

This section follows a Python function from a direct call to an MCP tool, then
to a tool an LLM agent can select. It is the current starting point in the
[AI Production Systems curriculum](../README.md).

## Learning order

| Subsection | What it covers |
| --- | --- |
| [S03.01: Python Functions](S03.01-Python-Functions/README.md) | Read ticket data and practise lookup, filtering, and aggregation |
| [S03.02: Functions to MCP Tools](S03.02-Functions-to-MCP-Tools/README.md) | Expose functions through FastMCP, test the MCP interface, inspect calls, and connect an OpenAI Agents SDK agent |
| [S03.03: MCP + OAuth 2.1](S03.03-MCP-OAuth2.1/README.md) | Add authentication and authorization with Keycloak, authorization-code flow with PKCE, token validation, and permission scopes |

Start with S03.01, then continue to S03.02 and S03.03. Each project has its own source,
fixtures, tests, manifest, and lockfile. Detailed explanations, commands, and
Inspector screenshots stay in the project READMEs.

## Running the projects

Run commands from the subsection folder. From S03.02, for example:

```bash
../../.venv/bin/python -m pytest -v
```

The shared root `.venv` is two levels above either project. The MCP server and
agent still expect their working directory to be S03.02, where `data/` and `src/`
are located. See the [environment instructions](#python-environment)
for installation.

## Python environment

The existing local workflow uses the shared root `.venv`. The
[requirements.txt](../requirements.txt) file lists the SDKs and development tools.
From the repository root:

```bash
uv pip install --python .venv/bin/python -r requirements.txt
source .venv/bin/activate
cd S03-AI-Agents-Tools-and-MCP/S03.02-Functions-to-MCP-Tools
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

Alternatively, from either subsection folder use `../../.venv/bin/python`
explicitly. Plain `uv run` selects the subsection's environment instead. The root
package list is unpinned; subsection manifests and lockfiles remain available for
isolated checks. S03.02's own manifest does not yet include the OpenAI Agents SDK,
so its isolated environment is not sufficient for the agent example.

## Current limits

S03.02 includes one successful live agent run, but automated agent tests remain
pending. The existing coverage gap, lint issues, and missing subsection-local
agent dependency still need attention. See each subsection's README for details.
