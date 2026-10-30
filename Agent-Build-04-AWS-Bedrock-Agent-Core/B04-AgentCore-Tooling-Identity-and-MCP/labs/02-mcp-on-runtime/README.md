# 02 — The ticket MCP server hosted on AgentCore Runtime

**Start with the failure.** Deploy `mcp_server/main.py` with `port=8080` (the agent port) and watch the Runtime end in `CREATE_FAILED`: the platform probes 8000 for an MCP Runtime and never gets a reply. Then forget the session header in a raw call and get a 400. Both failures are about the contract, not your code. Put the port back to 8000 and run the lab for the contrast.

## Goal
Host the four-tool ticket server on Runtime (`serverProtocol: MCP`), protect it with the lab 01 Cognito authorizer, and consume it from a Strands agent. No Gateway yet; lab 03 adds that.

## You will end with
- `ticket_mcp_server` Runtime, status `READY`, `TICKET_MCP_RUNTIME_ARN` and `TICKET_MCP_URL` in `.env`
- a transcript: `tools: ['get_ticket', 'list_tickets', 'get_policy', 'issue_refund']`, a refund answer, and an ESCALATE/REFUSED answer

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
cd 02-mcp-on-runtime
python -m pip install -r mcp_server/requirements.txt -t /dev/null 2>/dev/null; python mcp_server/main.py &   # local smoke on :8000, Ctrl-C after
python deploy_mcp_runtime.py          # zip → S3 → create_agent_runtime(serverProtocol=MCP) → READY
python consume_from_strands.py        # Strands MCPClient with a Cognito m2m token
```
Node CLI twin: `agentcore add runtime --protocol MCP --authorizer-type CUSTOM_JWT` then `agentcore deploy`.

## Facts that matter
- Ports: **8080** HTTP agents, **8000** MCP, **9000** A2A. The health probe for MCP Runtimes is the MCP endpoint itself.
- Stateless by default: the platform injects `Mcp-Session-Id`; one microVM per MCP session. See `stateful_note.md` for the trade.
- Invoke URL is the same `/runtimes/<arn>/invocations?qualifier=DEFAULT` as agents; Strands `MCPClient(url=..., headers=...)` handles the rest.
- An IAM-authorised MCP Runtime needs SigV4 on every request; use `mcp-proxy-for-aws` or `MCPClient(auth_provider=...)` with a SigV4 httpx auth. The lab uses JWT to keep the client plain.
- Gateway supports MCP versions 2026-07-28, 2025-11-25, 2025-06-18, 2025-03-26; `FastMCP` from the pinned `mcp` package negotiates.

## Proof (checklist)
- [ ] the deliberate 8080 deploy ended `CREATE_FAILED` with a readiness reason (keep the `failureReason` text)
- [ ] the 8000 deploy is `READY` and `get_agent_runtime` shows `protocolConfiguration.serverProtocol = MCP`
- [ ] `consume_from_strands.py` lists exactly four tools
- [ ] the refund question returns `REFUNDED` for 1042 and `REFUSED` or `ESCALATE` for the second question
- [ ] a raw `httpx` call without the session header returns 4xx (note the status and message)

## Next
`../03-gateway/` — the same tools behind a Gateway with search and an interceptor.
