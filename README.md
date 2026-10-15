# AI Production Systems

`production-agent-platform` is a hands-on learning repository for building and
understanding production AI systems. Work is grouped by subject area. The section
numbers organize the curriculum; they do not require completing every topic in
numerical order. Our current starting point is S03.

## Curriculum

| Section | Topic | Status |
| --- | --- | --- |
| [S00](S00-Enterprise-AI-and-Solution-Discovery/README.md) | Enterprise AI and Solution Discovery | Planned |
| [S01](S01-Production-AI-Application-Architecture/README.md) | Production AI Application Architecture | Planned |
| [S02](S02-LLMs/README.md) | LLMs | Planned |
| [S03](S03-AI-Agents-Tools-and-MCP/README.md) | AI Agents Tools and MCP | Started |
| [S04](S04-AI-Agents-Evals/README.md) | AI Agents Evals | Planned |
| [S05](S05-Agentic-Workflows-and-Harnesses/README.md) | Agentic Workflows and Harnesses | Planned |
| [S06](S06-RAG-Systems/README.md) | RAG Systems | Planned |
| [S07](S07-AI-Agents-Governance/README.md) | AI Agents Governance | Planned |
| [S08](S08-AI-Agents-Security/README.md) | AI Agents Security | Planned |
| [S09](S09-AI-Agents-Observability/README.md) | AI Agents Observability | Planned |

All ten sections have folders and landing READMEs. S03 contains the current
projects; the other sections are marked planned and have no exercises or code
yet. This subject-based index replaces the earlier R0–R10 roadmap.

## Start with S03

1. [S03.01: Python Functions](S03-AI-Agents-Tools-and-MCP/S03.01-Python-Functions/README.md)
   covers the Python foundation using ticket fixtures.
2. [S03.02: Functions to MCP Tools](S03-AI-Agents-Tools-and-MCP/S03.02-Functions-to-MCP-Tools/README.md)
   exposes functions through MCP, tests them, and connects a simple LLM agent.

Each subsection keeps its source, tests, fixtures, dependency manifest, and
lockfile together. Subsections do not import one another. Some code and tests
were developed with agent assistance; verification status is recorded in the
subsection documentation.

## Python environment

The existing local workflow uses the shared root `.venv`. The
[requirements.txt](requirements.txt) file lists the SDKs and development tools.
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

## Naming migration

| Previous project | Current location |
| --- | --- |
| `r0-python-recap-functions` (R0) | `S03-AI-Agents-Tools-and-MCP/S03.01-Python-Functions` |
| `r1-functions-to-mcp-tools` (R1) | `S03-AI-Agents-Tools-and-MCP/S03.02-Functions-to-MCP-Tools` |

The directory move preserves the existing code and evidence. Earlier log entries
using R0 and R1 refer to these same projects. Ignored environments and caches
remain at their old local locations to preserve local state; those old folders
are not part of the published structure. Use the shared root environment for the
commands above. Local vendor references remain in the ignored `documentation/`
folder at the repository root.
