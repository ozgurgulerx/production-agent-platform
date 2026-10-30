# 03 — Gateway: the governed surface

**Start with the failure.** Give the Strands agent all four tools straight from lab 02 and ask "refund £400 on 1043". The tool itself says ESCALATE, which is fine, but nothing outside your code enforced it, and the next developer can delete that `if`. This lab puts the same tools behind a Gateway, adds search, and moves the £250 rule into a request interceptor that runs no matter which backend serves the tool.

## Goal
One Gateway, two targets (a Lambda with an inline tool schema, an OpenAPI document in S3), semantic search, a Cognito JWT inbound, the Gateway role outbound, and a REQUEST interceptor.

## You will end with
- `AGENTCORE_GATEWAY_ROLE_ARN`, `TICKET_TOOLS_LAMBDA_ARN`, `TICKET_GATEWAY_ID`, `TICKET_GATEWAY_URL`, two target ids in `.env`
- a transcript showing `all tools` (eight names, `tickets-lambda___get_ticket` style), a search subset, a refund, and the interceptor refusal

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
cd 03-gateway
python gateway_role.py          # trust + inline policy
python deploy_lambda.py         # ticket-tools on python3.13 arm64
python create_gateway.py        # MCP, SEMANTIC search, CUSTOM_JWT
python add_targets.py           # Lambda target (GATEWAY_IAM_ROLE) + OpenAPI target (API_KEY if lab 04 row 01 ran)
python search_and_call.py       # list → search → agent refund → £400 attempt
python attach_interceptor.py    # REQUEST interceptor; rerun search_and_call.py
```
Node CLI twin: `agentcore add gateway`, `agentcore add tool --gateway ticket-gateway --lambda ...`, `agentcore deploy`.

## Facts that matter
- Search is `searchType: SEMANTIC` at creation; the tool is `x_amz_bedrock_agentcore_search` with `{"query": ...}`; 25 searches/min, 18 regions; not for HTTP targets.
- Tool names are `<targetName>___<toolName>`; Cedar in B09 uses the same string as the action id.
- Outbound credential is per target: `GATEWAY_IAM_ROLE`, `API_KEY`, `OAUTH`, `CALLER_IAM_CREDENTIALS`, `JWT_PASSTHROUGH`.
- One REQUEST and one RESPONSE interceptor per gateway; `passRequestHeaders` is off by default; `payloadFilter.exclude` keeps secrets out of the hook.
- `update_gateway` needs `name`, `roleArn`, `authorizerType` again; it is a full replace, not a patch.
- The OpenAPI target needs a reachable `servers[].url`; the lab document points at a placeholder until you have an API (lab 04 rows 01–02 use it).

## Proof (checklist)
- [ ] `get_gateway` shows `status READY`, `searchType SEMANTIC`, a `workloadIdentityDetails` ARN
- [ ] both targets `READY` (the OpenAPI target may be `FAILED` until the base URL is real; record the `statusReasons`)
- [ ] `search result` lists `issue_refund` and `get_policy` above `list_tickets` for the refund query
- [ ] the £40 refund returns `REFUNDED` and CloudWatch shows the Lambda log line with `"tool": "issue_refund"`
- [ ] after `attach_interceptor.py`, the £400 refund fails with the interceptor message and the Lambda log has **no** new line

## Next
`../04-auth-matrix/` — one script per outbound credential type.
