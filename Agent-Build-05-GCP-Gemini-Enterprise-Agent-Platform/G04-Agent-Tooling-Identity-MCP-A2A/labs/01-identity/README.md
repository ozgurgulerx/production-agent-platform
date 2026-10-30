# 01 — Agent Identity versus a service account

## Goal
Deploy `ticket-agent` twice from the same source: once with `identity_type=AGENT_IDENTITY` and once with an explicit service account. Read `spec.effectiveIdentity` on both and see a `principal://` SPIFFE principal on one and a service-account email on the other (map C5). Keep the Agent Identity deploy; delete the other.

## Steps
```bash
source ../../../labs-setup/.venv/bin/activate
set -a; source ../../../.env; set +a
P=$GOOGLE_CLOUD_PROJECT; L=$GOOGLE_CLOUD_LOCATION

# 1. Agent Identity deploy. .agent_engine_config.json carries {"identity_type": "AGENT_IDENTITY"} (map C5, B6).
adk deploy agent_engine ticket_agent --project "$P" --region "$L" --display_name ticket-agent-identity \
  --agent_engine_config_file .agent_engine_config.json --otel_to_cloud
# prints reasoningEngines/<ID>; copy the id
ID_AI=<ID>

# 2. Comparison deploy with a service account (the only place in the track that uses one; labs-setup README).
gcloud iam service-accounts create ticket-agent-sa --project "$P" 2>/dev/null || true
SA=ticket-agent-sa@$P.iam.gserviceaccount.com
gcloud projects add-iam-policy-binding "$P" --member="serviceAccount:$SA" --role=roles/aiplatform.user --condition=None
adk deploy agent_engine ticket_agent --project "$P" --region "$L" --display_name ticket-agent-sa \
  --service_account "$SA" --agent_engine_config_file sa.agent_engine_config.json
ID_SA=<ID>

# 3. Read the effective identity of both (map C5).
for ID in $ID_AI $ID_SA; do
  gcloud ai reasoning-engines describe "$ID" --project "$P" --region "$L" --format='value(name,spec.effectiveIdentity)'
done

# 4. Grant the Agent Identity principal what the later labs need (map C5): agent-to-agent calls in lab 06.
PRINCIPAL=$(gcloud ai reasoning-engines describe "$ID_AI" --project "$P" --region "$L" --format='value(spec.effectiveIdentity)')
for r in roles/agentregistry.viewer roles/aiplatform.user; do
  gcloud projects add-iam-policy-binding "$P" --member="$PRINCIPAL" --role="$r" --condition=None
done

# 5. Prove the token is bound: query the agent with the `whoami` tool (ticket_agent/agent.py) and inspect the result.
python query_whoami.py "$ID_AI"
```

`query_whoami.py` is yours to write (TODO in the file): call `:query` on the resource and print the `whoami` tool result, which should show the principal from the metadata server and whether the access token carries a `cnf` claim (map D10).

## Expected output
Step 3 prints a `principal://.../resources/...` string for `$ID_AI` and `ticket-agent-sa@...iam.gserviceaccount.com` for `$ID_SA`. Step 5 prints a dict with `principal` and `token_bound: true`. If `spec.effectiveIdentity` is empty on the first deploy, the config file was not picked up; `adk deploy agent_engine` reads `.agent_engine_config.json` by default (map B6).

## Proof checklist
- [ ] two resources listed by `gcloud ai reasoning-engines list` with display names `ticket-agent-identity` and `ticket-agent-sa`
- [ ] `spec.effectiveIdentity` is `principal://...` on one and a service-account email on the other
- [ ] IAM policy shows the `principal://` member with `roles/agentregistry.viewer` and `roles/aiplatform.user`
- [ ] `query_whoami.py` output shows `token_bound: true` for the Agent Identity deploy
- [ ] `.env` `AGENT_RUNTIME_RESOURCE` points at the Agent Identity deploy

## Cleanup
Delete the service-account deploy (`delete(force=True)` via the SDK or the console) and the `ticket-agent-sa` account. Deleting and recreating the Agent Identity deploy would mint a new principal and orphan the bindings from step 4 (map D10), so keep it.

## Next
`../02-mcp-tool/` — the agent reaches a ticketing MCP server through `McpToolset`.
