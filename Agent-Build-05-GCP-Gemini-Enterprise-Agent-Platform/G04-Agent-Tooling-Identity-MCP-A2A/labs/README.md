# G04 labs — identity, tools, MCP Toolbox, Apigee, Registry, A2A for the ticket agent

Runnable proofs for the G04 chapter. Setup is shared: [`../../labs-setup/`](../../labs-setup/) (activate `../../labs-setup/.venv`, `.env` at the track root). These labs assume the agents from G03 labs 01–03 exist (`ticket-agent`, `ticket-agent-workflow`) and `AGENT_RUNTIME_RESOURCE` is set in `.env`. Each lab README ends with a **proof checklist**. Facts cite the reading map ([`../../reference/reading-map-gcp-agents-2026-10-25.md`](../../reference/reading-map-gcp-agents-2026-10-25.md)).

```
labs/
├── 01-identity/               Agent Identity vs service account; read spec.effectiveIdentity
├── 02-mcp-tool/               McpToolset over stdio to a local Toolbox; tool_filter; refund-policy before_tool_callback
├── 03-mcp-toolbox/            tools.yaml + schema.sql; Toolbox on Cloud Run with Google auth; produces TICKET_MCP_URL
├── 04-auth-matrix-apigee/     one agent per AuthCredentialTypes row; OAuth consent; Apigee MCP variant
├── 05-registry-and-gateway/   register agent and MCP server in Agent Registry; Agent Gateway default-deny + CEL
└── 06-a2a/                    to_a2a on the workflow agent; RemoteA2aAgent in ticket-agent; 0.3 compat note
```

| Lab | Chapter section | Creates | Time |
|---|---|---|---|
| 01 | §1 Agent identity | a second deploy of `ticket-agent` with `identity_type=AGENT_IDENTITY`, a comparison deploy with a service account, both described | 40 min |
| 02 | §4 tool kinds, §2 auth | a local Toolbox over stdio, `McpToolset` with `tool_filter`, the refund `before_tool_callback` | 45 min |
| 03 | §5 Toolbox | Cloud SQL `tickets` table, secret `tools`, Cloud Run service `ticket-mcp`, `TICKET_MCP_URL` in `.env` | 60 min |
| 04 | §2 auth matrix, §3 OAuth, §6 Apigee | `auth_matrix.py` output: which rows answered and what the server saw; optional Apigee run | 60 min |
| 05 | §6 Registry and Gateway | `ticket-agent` and `ticket-mcp` in Agent Registry; a gateway with one allowed tool | 45 min |
| 06 | §7 A2A | `ticket-agent-workflow` served over A2A, consumed from `ticket-agent` as `RemoteA2aAgent` | 45 min |

Order: 01 → 02 → 03 → 04 → 05 → 06. Session 3 is 01–03, session 4 is 04–06 (labs-setup README). Lab 02 can run before lab 03 because it talks to the Toolbox over stdio against a local Postgres loaded with `03-mcp-toolbox/schema.sql`; labs 04–06 need `TICKET_MCP_URL` from lab 03.

```bash
source ../../labs-setup/.venv/bin/activate
set -a; source ../../.env; set +a
cd 01-identity && cat README.md
```

Folder layout: each lab keeps its agent in an identifier-named package `ticket_agent/` (`__init__.py` + `agent.py`), because `adk web`, `adk run` and `adk deploy` import the agent folder as a Python package and `02-mcp-tool` is not an importable name (map B6). Run `adk web` from the lab folder and pick `ticket_agent`; deploy with `adk deploy agent_engine ticket_agent`.

Rules every lab follows (labs-setup README): ADC only, `GOOGLE_GENAI_USE_VERTEXAI=TRUE`, `McpToolset` declared synchronously in `agent.py`, one built-in tool per agent, `identity_type=AGENT_IDENTITY` on every Agent Runtime deploy except the lab 01 comparison row, model ids from `.env`, delete test agents when done.

Status on 25 Oct 2026: scaffold only, functionality unverified. Learner writes the tool functions, callbacks and tests at every `# TODO(learner)`.

Next chapter: [`../../G05-Evals-and-Observability/labs/`](../../G05-Evals-and-Observability/labs/).
