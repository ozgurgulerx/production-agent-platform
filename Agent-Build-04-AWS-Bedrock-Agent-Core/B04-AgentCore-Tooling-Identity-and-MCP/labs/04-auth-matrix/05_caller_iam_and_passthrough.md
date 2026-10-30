# Rows CALLER_IAM_CREDENTIALS and JWT_PASSTHROUGH

Both exist only on **HTTP targets** (`agentcoreRuntime` and `passthrough`), not on Lambda/OpenAPI MCP targets. Lab 06 creates them.

| Row | What the Gateway forwards | Downstream must | Use when |
|---|---|---|---|
| `CALLER_IAM_CREDENTIALS` | signs the downstream call with the **caller's** IAM credentials (the Gateway acts as a proxy, not a principal) | be an AWS resource that authorises on IAM: another Runtime, an IAM-authorised MCP Runtime | the calling role is the policy subject; audit shows the human's assumed role, not the Gateway |
| `JWT_PASSTHROUGH` | the inbound `Authorization: Bearer` header, unchanged | validate the same issuer/audience as the Gateway's authorizer | your own services behind the same IdP; never a third party (its audience is wrong there) |

Neither reaches the token vault. Neither works with a `NONE` or `AUTHENTICATE_ONLY` gateway for the IAM row (there is no caller identity to forward).

Choosing between the seven rows in one line each:
- Your Lambda, your account → `GATEWAY_IAM_ROLE`.
- A legacy key → `API_KEY` (vault-managed or Secrets Manager).
- A SaaS as the agent → `OAUTH` client credentials, or `PRIVATE_KEY_JWT` if the SaaS supports it.
- A SaaS as the user, different IdP → `OAUTH` authorization code (3LO) + Consent Portal.
- A SaaS as the user, same IdP (Entra in, Graph out) → `OAUTH` token exchange (OBO).
- Another agent or Runtime in AWS → `CALLER_IAM_CREDENTIALS`.
- Your own API behind the same JWT issuer → `JWT_PASSTHROUGH`.
