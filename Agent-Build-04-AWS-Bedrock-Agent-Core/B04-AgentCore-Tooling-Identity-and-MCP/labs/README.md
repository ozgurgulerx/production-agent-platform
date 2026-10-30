# B04 labs — identity, MCP, Gateway, auth, Registry and A2A for the ticket agent

Runnable proofs for the B04 chapter. Setup is shared: [`../../labs-setup/`](../../labs-setup/) (venv, `.env` at the track root, `verify.sh` printing OK). These labs assume B03 lab 01 has run and written `TICKET_AGENT_RUNTIME_ARN` and `AGENTCORE_RUNTIME_ROLE_ARN` to `.env`. Each lab README ends with a **proof checklist**; a lab is done when the boxes are ticked with real output. Nothing here has run yet.

```
labs/
├── 01-identity-inbound/           Cognito pool → customJWTAuthorizer on a Runtime → 401 then 200 with a bearer token
├── 02-mcp-on-runtime/             the ticket MCP server hosted on Runtime (8000 /mcp, stateless), consumed from Strands
├── 03-gateway/                    Gateway with Lambda + OpenAPI targets, semantic search, request interceptor
├── 04-auth-matrix/                one script per outbound credential type; which principal the API saw
├── 05-agent-registry/             registry, records (MCP, A2A, skills), approval, discovery
└── 06-a2a-and-runtime-targets/    Runtime agent as a Gateway HTTP target; A2A passthrough target; weighted rule
```

| Lab | Chapter section | Writes to `.env` | Needs beyond the shared setup |
|---|---|---|---|
| 01 | §1 identity, §2 inbound | `COGNITO_*` | nothing (creates its own Cognito pool) |
| 02 | §4 MCP on Runtime | `TICKET_MCP_RUNTIME_ARN` | lab 01 (JWT), `CODE_BUCKET` |
| 03 | §5 Gateway, §6 Strands | `AGENTCORE_GATEWAY_ROLE_ARN`, `TICKET_GATEWAY_ID`, `TICKET_GATEWAY_URL` | lab 01; Lambda create permission |
| 04 | §3 outbound matrix | `TICKETS_API_KEY_PROVIDER_ARN`, `TICKETS_OAUTH_PROVIDER_ARN` | an OAuth client for rows 02–03; an Entra app for row 04 |
| 05 | §8 Registry | `TICKET_REGISTRY_ID` | lab 03; B03 lab 03 A2A runtime for the A2A record |
| 06 | §7 A2A, agent-as-target | — | labs 03; B03 labs 01 and 03 |

Order: 01 → 02 → 03 → 04 → 05 → 06. Session 3 is 01–03, session 4 is 04–06. Every script accepts `--cleanup` to delete what it created.

```bash
source ../../labs-setup/.venv/bin/activate
cd 01-identity-inbound && python cognito_setup.py
```

Prerequisites: `aws sso login`, `AWS_REGION` set to `us-east-1` or `us-west-2`, Bedrock access to `BEDROCK_MODEL_ID`, and the execution role from `labs-setup/00-setup`. Region matters: Gateway semantic search is in 18 regions, the Consent Portal needs a JWT Gateway.

Next chapter: [`../../B05-AgentCore-Evals-and-Observability/labs/`](../../B05-AgentCore-Evals-and-Observability/labs/).
