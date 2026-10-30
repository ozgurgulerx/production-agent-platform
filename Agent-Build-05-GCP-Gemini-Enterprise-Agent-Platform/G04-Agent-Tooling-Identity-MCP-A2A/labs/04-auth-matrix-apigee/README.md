# 04 — The credential matrix against the ticketing MCP server, with Apigee in front

## Goal
Run one `ticket-agent` per `AuthCredentialTypes` row against `TICKET_MCP_URL` and record what the server saw (map D5). Prove the OAuth passthrough flow by catching `adk_request_credential` and answering it (chapter §3). Optionally repeat the matrix against `APIGEE_MCP_URL`, where API hub serves the same tools over OAuth 2.1 (map D12, D13).

## Steps
```bash
source ../../../labs-setup/.venv/bin/activate
set -a; source ../../../.env; set +a

# 1. The matrix. Rows: none, API_KEY, HTTP, SERVICE_ACCOUNT (use_id_token, audience=TICKET_MCP_URL), OAUTH2, OPEN_ID_CONNECT.
python auth_matrix.py                       # prints one line per row: credential type | HTTP status | principal seen | note
python auth_matrix.py --row OAUTH2          # interactive: prints auth_uri, waits for the redirect URL, resumes

# 2. What the server saw. Toolbox logs on Cloud Run carry the caller identity for the IAM-gated rows;
#    for the OPEN_ID_CONNECT row the `sub`-bound my_open_tickets result is the proof.
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="ticket-mcp"' --limit 20 --format='value(textPayload)'

# 3. Apigee variant (skip when APIGEE_ORG is empty). API hub ingests the OpenAPI document and maps operations to tools (map D12).
#    Console steps: API hub → register ticketing-api (OpenAPI 3.0.x) → MCP server → ConfigureAndDeployServer (GA 24 Jul 2026, map D13)
#    → note the endpoint ORG_NAME.mcp.apigee.internal → write it to .env as APIGEE_MCP_URL.
#    Rate limiting and token exchange per API product: page not in the map, unverified; G09 designs around it.
python auth_matrix.py --target "$APIGEE_MCP_URL" --row OAUTH2
```

## What to write
- `auth_matrix.py`: for each row build the `(auth_scheme, auth_credential)` pair with `token_to_scheme_credential` or `service_account_scheme_credential` (map D5), construct `McpToolset(StreamableHTTPConnectionParams(url), auth_scheme=..., auth_credential=...)`, run one `lookup_ticket` call through a `Runner` with `InMemorySessionService`, and print the row. The `OAUTH2` and `OPEN_ID_CONNECT` rows need `GOOGLE_OAUTH_CLIENT_ID` and a client secret from lab 03 step 2; the loop that answers `adk_request_credential` is in `../../sketches/consent_and_resume.py`.
- `test_04_auth_matrix.py`: unit tests for the pair builders and for the consent loop with a fake event stream.

## Expected output
```
none              403  -                          Cloud Run IAM refused before Toolbox saw it
API_KEY           403  -                          Toolbox has no API-key authService; Apigee row only
HTTP              200  principal://.../ticket-... bearer was an ID token for TICKET_MCP_URL
SERVICE_ACCOUNT   200  principal://.../ticket-... use_id_token=True, audience=TICKET_MCP_URL
OAUTH2            200  user sub=1098...           consent shown once; adk_request_credential answered
OPEN_ID_CONNECT   200  user sub=1098...           my_open_tickets returned only that user's rows
```
Locally the principal column shows your ADC account; on Agent Runtime it shows the lab 01 principal. If the `SERVICE_ACCOUNT` row returns 401 the audience was the `/mcp` path, not the service URL.

## Proof checklist
- [ ] matrix printed with a status per row and a reason for every non-200
- [ ] `OAUTH2` row printed an `auth_uri`, you consented, and the retry returned a ticket (tick only with the URI in the output)
- [ ] `OPEN_ID_CONNECT` row returned only the signed-in user's tickets from `my_open_tickets`
- [ ] Cloud Run logs show the ID-token rows under the expected principal
- [ ] Apigee row (optional): `tools/list` through `APIGEE_MCP_URL` names `lookup_ticket`, and the OAuth 2.1 Protected Resource Metadata is discoverable
- [ ] `pytest test_04_auth_matrix.py` runs the builder tests

## Cleanup
Revoke the OAuth grant for the test user in the Google Account permissions page. Nothing is deployed by this lab.

## Next
`../05-registry-and-gateway/` — catalogue the agent and the server; put a default-deny gateway between them.
