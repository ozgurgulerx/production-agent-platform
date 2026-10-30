# 03 — MCP Toolbox for Databases on Cloud Run: the governed ticketing surface

## Goal
Deploy the `tools.yaml` from lab 02 to Cloud Run as the ticketing MCP server over a Cloud SQL Postgres `tickets` table, with Google-user auth on `my_open_tickets` and IAM (`roles/run.invoker`) at the door (map D7, D8). The run ends with `TICKET_MCP_URL` in `.env`; labs 04 to 06 and the G05 labs use it.

## Files
- `schema.sql`: the `tickets` table (`id, customer, status, amount, opened_at`) and five seed rows
- `tools.yaml`: source, `authService google`, two tools, one toolset (same file lab 02 ran locally)
- `deploy.sh`: the Cloud Run commands from map D8, pinned to Toolbox 1.15.0
- `ticket_agent/agent.py`: `ticket-agent` pointed at `TICKET_MCP_URL` with `StreamableHTTPConnectionParams` and an ID token (map D3, D5)

## Steps
```bash
source ../../../labs-setup/.venv/bin/activate
set -a; source ../../../.env; set +a
P=$GOOGLE_CLOUD_PROJECT; L=$GOOGLE_CLOUD_LOCATION

# 1. Database. The map has no Cloud SQL page; the commands below are the standard gcloud sql verbs, unverified here.
gcloud sql instances create tickets-pg --database-version=POSTGRES_16 --tier=db-f1-micro --region="$L" --project "$P"
gcloud sql databases create tickets --instance=tickets-pg --project "$P"
gcloud sql users set-password postgres --instance=tickets-pg --password="$TICKETS_DB_PASSWORD" --project "$P"
gcloud sql connect tickets-pg --user=postgres --database=tickets < schema.sql

# 2. OAuth client id for authService google (map D7): APIs & Services → Credentials → OAuth client (Web). Put it in .env as GOOGLE_OAUTH_CLIENT_ID.

# 3. Deploy. Prints TICKET_MCP_URL.
bash deploy.sh
# write the printed value into ../../../.env  (TICKET_MCP_URL=https://ticket-mcp-....run.app)

# 4. Door policy: only the agent principal from lab 01 (and you, for the proof) may invoke (map D8).
PRINCIPAL=$(gcloud ai reasoning-engines describe "${AGENT_RUNTIME_RESOURCE##*/}" --project "$P" --region "$L" --format='value(spec.effectiveIdentity)')
gcloud run services add-iam-policy-binding ticket-mcp --region "$L" --project "$P" --member="$PRINCIPAL" --role=roles/run.invoker
gcloud run services add-iam-policy-binding ticket-mcp --region "$L" --project "$P" --member="user:$(gcloud config get-value account)" --role=roles/run.invoker

# 5. Prove the door. Anonymous fails, an ID token for the service URL succeeds.
curl -s -o /dev/null -w '%{http_code}\n' "$TICKET_MCP_URL/mcp"                                    # 401 or 403
curl -s -H "Authorization: Bearer $(gcloud auth print-identity-token --audiences="$TICKET_MCP_URL")" \
  -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' "$TICKET_MCP_URL/mcp"

# 6. Prove the claim binding. my_open_tickets needs a Google user token in header google-user_token (map D7).
python call_as_user.py my_open_tickets                                                             # TODO(learner) script

# 7. Run the agent against the Cloud Run server.
adk web --port 8000      # from this lab folder; pick ticket_agent; "What is the status of ticket 1003?"
```

## Expected output
Step 5: first curl prints `403` (Cloud Run IAM), second prints a `tools/list` result naming `lookup_ticket` and `my_open_tickets`. Step 6 returns only the rows whose `customer` equals the signed-in user's `sub` mapping, and a call without the header is rejected by Toolbox, not by Cloud Run. Step 7 shows a `lookup_ticket` call in the Events tab with `{"ticket_id": 1003}` and `amount: 250.00`.

## What Toolbox did not do here
It did not decide which principal may reach it (Cloud Run IAM did), it did not catalogue itself (lab 05), it did not screen the request (Model Armor is G05), and it did not stop you writing a broad `statement`. Section 5 of the chapter has the full list.

## Proof checklist
- [ ] `psql`/`gcloud sql connect` shows five rows in `tickets`
- [ ] `gcloud run services describe ticket-mcp` shows service account `toolbox-identity@...` and the `tools` secret mounted
- [ ] anonymous `curl` returns 401/403; ID-token `curl` returns the tool list
- [ ] `my_open_tickets` without `google-user_token` is refused by Toolbox; with it returns only that user's tickets
- [ ] `TICKET_MCP_URL` is in `.env` and `adk web` round-trips `lookup_ticket` against it
- [ ] the agent principal from lab 01 holds `roles/run.invoker` on `ticket-mcp` and nobody else except you

## Cleanup
Keep `ticket-mcp` and the Cloud SQL instance until G05 is done; they are the shared tool for the rest of the track. Then `gcloud run services delete ticket-mcp`, `gcloud sql instances delete tickets-pg`, `gcloud secrets delete tools`.

## Next
`../04-auth-matrix-apigee/` — one agent per credential type against this URL, and Apigee in front.
