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
| [S03.04: MCP Tool Design](S03.04-MCP-Tool-Design/README.md) | Design intent-level tools with precise descriptions, keep deterministic workflows in code, and reduce tool-selection ambiguity |
| [S03.05: MCP Context Efficiency](S03.05-MCP-Context-Efficiency/README.md) | Compare tool exposure, large-result delivery and retained history; design material with a bounded minimum build |
| [S03.06: Client as Trust Boundary](S03.06-Client-as-Trust-Boundary/README.md) | Enforce task authority, approvals and disclosure policy; proposed attack matrix and effect-based evaluation |

Start with S03.01, then continue through S03.06. Each implementation project has its own source,
fixtures, tests, manifest, and lockfile. Detailed explanations, commands, and
Inspector screenshots stay in the project READMEs.

## Completion and evidence

Use the [S03 completion checklist](S03-COMPLETION-TASKS.md) to track documentation, builds and recall separately. S03.04–06 contain design exercises; their descriptions are not evidence that the proposed servers, harnesses or controls have been implemented. The next build priority is S04 evaluation evidence; S03.05's minimum build follows it. Preserve the existing S03.03 live-check limitations.

## Protocol baselines

Local manifests, lockfiles and installed protocol registries were inspected on 21 October 2026:

| Stage | SDK pin | Supported protocol evidence | What remains to record |
|---|---|---|---|
| S03.02 | `mcp==2.3.0` in `uv.lock` | Installed `mcp_types/version.py` includes `2026-07-28` and earlier handshake revisions, including `2025-11-25` | Actual interpreter/package version and protocol exercised by each client run; the shared root environment can differ from this lockfile |
| S03.03 | `mcp==1.26.0` | Installed `mcp/types.py` declares latest `2025-11-25` | Redacted wire evidence and a revision-matched conformance run |
| S03.04–06 | No new runtime pin established by the chapters | Wire examples use the S03.03 `2025-11-25` baseline; later changes are labelled | Pin the actual runtime when the learner builds each stage |

A package version, a supported revision and the protocol actually exercised are different facts. Independent stages may use different pins; do not silently migrate them to make the table uniform.

## MCP in two minutes

The **host** is the application that manages the model, user interaction and policy. Its **MCP client** maintains a connection to a **server**, which exposes capabilities over a protocol. The server executes registered operations; it does not need an LLM. MCP messages use JSON-RPC 2.0: requests have an `id`, responses echo it, and notifications have no response ID. The host still decides whether a proposed call is allowed.

| Primitive | Ticket example | How it is consumed |
|---|---|---|
| Tool | `get_ticket(ticket_id)` | An operation invoked through `tools/call`; model selection is mediated by the host |
| Resource | A versioned payment-log URI | Data the application retrieves through `resources/read` and selectively exposes |
| Prompt | A user-selected refund-investigation template | Messages retrieved through `prompts/get`; not a new system-level authority |

**Transport is not policy.** With stdio the client starts a local process and exchanges protocol messages over its pipes; diagnostics go to stderr. Streamable HTTP connects to a separately running service, which may stream messages using SSE. HTTP access still needs the appropriate authentication and authorization. Neither a local process nor an HTTP session is automatically a sandbox. [MCP transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)

**Lifecycle is version-specific.** In 2025-11-25, the client sends `initialize`, checks the agreed revision/capabilities, then sends `notifications/initialized` before ordinary calls. Features such as elicitation require declared support. [Lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle) The 2026-07-28 release replaces that handshake/session core with self-describing requests and adds list-cache hints; roots, sampling and logging are deprecated. These changes do not retroactively alter the pinned S03.03 example. [Release notes](https://blog.modelcontextprotocol.io/posts/2026-07-28/)

### Annotated success and failure

This is an **illustrative 2025-11-25 message sequence**, not a captured run. Authentication headers and payload details are omitted; never paste bearer tokens into a trace.

| Direction | Message | Meaning / effect |
|---|---|---|
| Client → server | `initialize`, request ID 1 | Offer revision and client capabilities |
| Server → client | Result for ID 1 | Agreed revision, server identity and capabilities |
| Client → server | `notifications/initialized` | Notification: no response expected |
| Client → server | `tools/list`, ID 2 | Discover definitions; not permission to invoke |
| Server → client | Result for ID 2 | Tool names, descriptions and schemas |
| Client → server | `tools/call`, ID 3, `get_ticket`, `{"ticket_id":"T-1003"}` | Validate request, authenticate/authorize as appropriate, then read the fixture |
| Server → client | Result for ID 3, content, `isError: false` | Read evidence; no refund or notification effect |

For the failed trace, reuse an authenticated initialized S03.03 client with a token lacking `tickets.refund`: `tools/call` → `issue_refund` → scope guard rejects → result with `isError: true`. HTTP can still be 200 because delivery succeeded. The refund ledger is untouched. This matches the documented scope-test contract, not a newly executed test. By contrast, a missing/invalid bearer token is rejected at the HTTP authentication boundary before tool execution.

| Failure layer | Example | What to inspect |
|---|---|---|
| Transport | Connection refused or stream breaks | Network/process logs; a lost write response leaves an unknown outcome |
| HTTP authentication | 401 before dispatch | Intended issuer/audience, expiry and credential acquisition; redact tokens |
| JSON-RPC envelope | Invalid JSON or malformed request | Parse/invalid-request error, not a business rejection |
| MCP method/protocol | Unknown method/tool or unsupported revision | Protocol error and the revision-specific contract |
| Tool execution | Missing scope, invalid business input or backend failure | Tool result `isError`; backend state determines actual effects |

See [S03.04 error handling](S03.04-MCP-Tool-Design/README.md#3-design-results-errors-and-ambiguity-handling) for the pinned distinction between malformed requests and tool-input validation.

## Choosing MCP and choosing server boundaries

| Interface | Main job | Relationship to this stage |
|---|---|---|
| Model function calling | Let a model propose structured arguments to application functions | Can call local functions directly or use host adapters for MCP tools |
| MCP | Discover and invoke reusable capabilities across clients/servers | Useful when several hosts need a shared integration contract |
| OpenAPI / framework plugins | Describe HTTP APIs or package framework-specific functions | Can underpin an MCP adapter; descriptions still need tool-design work |
| A2A | Delegate work between agents that manage their own tasks | Complements tool access; it is not needed merely to call a ticket API. [A2A overview](https://a2a-protocol.org/latest/topics/what-is-a2a/) |

MCP may add little for one client with a stable local backend. A fixed batch pipeline may be clearer as ordinary code, and a latency-critical path should justify discovery, serialization and network overhead with measurements. These are trade-offs, not bans: interoperability can still outweigh the cost.

Choose server boundaries around credential ownership, data sensitivity, operational ownership and failure impact. HR, tickets and payments should not share broad credentials just to reduce server count. A common gateway can route to separate services while preserving identities and policy; one shared server is reasonable only when its isolation and permission model are explicit. Namespacing avoids ambiguity but does not enforce that isolation.

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
