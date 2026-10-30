# 04 — Outbound auth matrix: which principal the API sees

**Start with the failure.** Paste the ticket API key into the Lambda's environment variables, call it from the agent, and ask: who else can read that key? Everyone with `lambda:GetFunctionConfiguration`. Now the same key lives in the token vault as a credential provider and the Gateway injects it per call. Same request on the wire, different blast radius.

## Goal
One script per outbound credential type, so you can say for each row **who the downstream system sees** and **whether the user travels**. The matrix:

| Row | Script | Downstream sees | User? |
|---|---|---|---|
| `GATEWAY_IAM_ROLE` | lab 03 | the Gateway role | no |
| `API_KEY` | `01_api_key_provider.py` | the stored key | no |
| `OAUTH` client credentials (2LO) | `02_oauth_client_credentials.py` | the agent's OAuth client | no |
| `OAUTH` authorization code (3LO) | `03_oauth_authorization_code.py` | the user, after one consent | yes |
| `OAUTH` token exchange (OBO) | `04_obo_token_exchange.py` | the user, no consent (Entra in, Graph out) | yes |
| `CALLER_IAM_CREDENTIALS` | lab 06 | the caller's IAM identity | IAM |
| `JWT_PASSTHROUGH` | lab 06 | the caller's inbound JWT | yes |

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
cd 04-auth-matrix
python run_matrix.py                       # shows which rows can run with what is in .env, runs those
TICKETS_API_KEY=demo-key python 01_api_key_provider.py
python 02_oauth_client_credentials.py      # Cognito as the IdP; prints the provider's callbackUrl
OAUTH_3LO_PROVIDER=tickets-oauth-m2m TICKETS_API_BASE=https://... python 03_oauth_authorization_code.py
python 04_obo_token_exchange.py && python 04_obo_token_exchange.py --call     # needs an Entra app
```

## Facts that matter
- A credential provider is an Identity resource; a target references it by ARN; code references it by name through `@requires_access_token` / `@requires_api_key`.
- `clientSecretSource` MANAGED (vault) or EXTERNAL (Secrets Manager ARN, Jul 2026); `clientAuthenticationMethod` can be `PRIVATE_KEY_JWT` with a KMS key, so no secret exists.
- 3LO: `GetResourceOauth2Token` returns `authorizationUrl` and `sessionUri` on a vault miss; the decorator polls; the token is stored per (workload, user). GA on MCP targets Apr 2026. The Consent Portal (Sep 2026) hosts the consent page for a JWT-fronted Gateway.
- OBO (Apr 2026): `oauth2Flow: ON_BEHALF_OF_TOKEN_EXCHANGE`; the inbound JWT must be from the same IdP; `MicrosoftOauth2` has the exchange built in; custom IdPs use `onBehalfOfTokenExchangeConfig` with `TOKEN_EXCHANGE` or `JWT_AUTHORIZATION_GRANT`.
- Running `@requires_access_token` outside a Runtime needs a workload identity and `GetWorkloadAccessToken*` permission; inside a Runtime the token is injected.

## Proof (checklist)
- [ ] `run_matrix.py` prints all seven rows with a status, none crashing
- [ ] row API_KEY: the Lambda/API log shows `x-api-key` present and the agent transcript never contains the key
- [ ] row 2LO: `get_oauth2_credential_provider` shows the provider; a tool call through the Gateway succeeds with a token whose `client_id` is the lab client
- [ ] row 3LO: the consent URL printed once; second run has no URL (vault hit)
- [ ] row OBO: either a Graph `200` with the user's displayName, or an honest "needs an Entra app" line in the proof

## Next
`../05-agent-registry/` — publish the gateway and the A2A agent as registry records.
