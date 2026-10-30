# 01 — Inbound identity: a Runtime only a JWT can call

**Start with the failure.** B03 lab 01's runtime answers anyone with `bedrock-agentcore:InvokeAgentRuntime`. Put that ARN in a browser-side app and the app must hold AWS credentials. This lab recreates the agent with a `customJWTAuthorizer`, so the caller presents a Cognito token and no AWS credential leaves the account.

## Goal
See the three principals of §1 with your own eyes: the **caller** (a Cognito user or client), the **execution role** (unchanged from B03), and the Runtime's **workload identity** (listed in `get_agent_runtime`). Then watch the authorizer reject and accept.

## You will end with
- a Cognito pool, app client (with secret), resource-server scope `tickets/invoke`, test user `ayse` (all in `.env`)
- `ticket-agent-jwt`, the B03 code zip under a JWT authorizer, `TICKET_AGENT_JWT_ARN` in `.env`
- two transcripts: `401` with `WWW-Authenticate: Bearer resource_metadata=...`, then `200` with the agent's answer

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
cd 01-identity-inbound
python cognito_setup.py            # pool, client, scope, user → .env
python tokens.py                   # prints the first 40 chars of a user token and an m2m token
python runtime_with_jwt.py         # needs TICKET_AGENT_CODE_S3_URI and AGENTCORE_RUNTIME_ROLE_ARN from B03 lab 01
python invoke_with_bearer.py       # 401 then 200 (user token)
python invoke_with_bearer.py --m2m # same with a client-credentials token: no user in the token
```

## Facts that matter
- Runtime auth is **SigV4 or JWT, never both** (`authorizerConfiguration` is absent = IAM). To change it you update the Runtime, which creates a new immutable version.
- The authorizer checks `discoveryUrl` (issuer), `allowedClients`, optionally `allowedAudience`, `allowedScopes`, `customClaims`. Cognito access tokens have `client_id`, not `aud`, which is why the lab uses `allowedClients`.
- `allowedWorkloadConfiguration` (Jul 2026) restricts a JWT Runtime to tokens minted for a named Gateway or workload identity; lab 06 uses it.
- JWT Runtimes are invoked over HTTPS at `/runtimes/<url-encoded ARN>/invocations?qualifier=DEFAULT`; the session header must be ≥33 characters.
- `X-Amzn-Bedrock-AgentCore-Runtime-User-Id` with an IAM caller is the other way to pass a user; the docs steer production to JWT.

## Proof (checklist)
- [ ] `cognito_setup.py` printed the discovery URL and `.env` has seven `COGNITO_*` lines
- [ ] `get_agent_runtime` for `ticket-agent-jwt` shows `authorizerConfiguration.customJWTAuthorizer` and a workload identity ARN
- [ ] `[1] bad token → 401` with a `WWW-Authenticate` header containing `resource_metadata`
- [ ] `[2] user token → 200` and the answer mentions ticket 1042
- [ ] the same call with `--m2m` succeeds; decode both tokens (jwt.io) and note that only the user token has `username`

## Next
`../02-mcp-on-runtime/` — the ticket MCP server on Runtime, behind the same authorizer.
