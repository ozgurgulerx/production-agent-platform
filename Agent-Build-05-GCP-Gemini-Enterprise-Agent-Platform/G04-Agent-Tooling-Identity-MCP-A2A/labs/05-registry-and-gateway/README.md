# 05 — Agent Registry and Agent Gateway: catalogue, then default-deny

## Goal
Register `ticket-agent` and the `ticket-mcp` server in Agent Registry so other teams can find them (map F7), then put Agent Gateway between the agent and the server: default-deny, one IAM condition that opens `lookup_ticket` and `my_open_tickets` for the lab 01 principal and nothing else, rolled out in `DRY_RUN` first (map F7). Both went GA on 18 Jun 2026 (map A2).

The map has the govern overview, the gateway overview and the IAM policies page (F7) and the Terraform page (I8), but no gcloud or REST reference for creating registry entries or gateways. Steps marked **unverified** are console paths; check the live page before relying on a verb.

## Steps
```bash
source ../../../labs-setup/.venv/bin/activate
set -a; source ../../../.env; set +a
P=$GOOGLE_CLOUD_PROJECT; L=$GOOGLE_CLOUD_LOCATION
PRINCIPAL=$(gcloud ai reasoning-engines describe "${AGENT_RUNTIME_RESOURCE##*/}" --project "$P" --region "$L" --format='value(spec.effectiveIdentity)')

# 1. Registry (console, unverified verbs). Gemini Enterprise Agent Platform → Govern → Agent Registry:
#    - Add McpServer: name ticket-mcp, endpoint $TICKET_MCP_URL/mcp, transport streamable HTTP
#    - Add Agent: name ticket-agent, kind ADK, resource $AGENT_RUNTIME_RESOURCE; attach the A2A card from lab 06 later
#    Resources: Agent, McpServer, Endpoint, Service (GA); Skill, Publisher (preview). URNs are catalogue-only (map F7).

# 2. Gateway (console or Terraform google-beta agent_gateway_config, map I8; identity_type must be AGENT_IDENTITY).
#    Create gateway ticket-gateway in $L; add ticket-mcp as an MCP target; set iamEnforcementMode DRY_RUN and
#    Model Armor INSPECT_ONLY (map F7). Binding the agent to the gateway archives its earlier revisions (map C4): expected.
terraform -chdir=terraform init && terraform -chdir=terraform apply -var project="$P" -var region="$L" -var principal="$PRINCIPAL"

# 3. The one allow. roles/iap.egressor with a CEL condition on mcp.toolName (map F7). Attribute path form unverified.
gcloud projects add-iam-policy-binding "$P" --member="$PRINCIPAL" --role=roles/iap.egressor \
  --condition='title=ticket-agent-lookup-only,expression=request.mcp.toolName == "lookup_ticket" || request.mcp.toolName == "my_open_tickets"'

# 4. Point the agent at the gateway instead of the server and query it. The gateway URL comes from step 2.
python gateway_probe.py --tool lookup_ticket            # expected: allowed (dry run logs "would allow")
python gateway_probe.py --tool refund_ticket            # expected: dry run logs "would deny"; still passes through
# 5. Flip to enforce; repeat. refund_ticket now fails at the gateway, before Cloud Run and Toolbox.
```

## What to write
- `terraform/main.tf`: the google-beta `google_vertex_ai_reasoning_engine` block with `agent_gateway_config` for the existing agent (map I8); TODO markers where the gateway resource name goes once you have read the live page.
- `gateway_probe.py`: build the lab 03 agent with `TICKET_MCP_URL` replaced by the gateway URL, call the named tool, print the outcome and the matching gateway log line (OTel and L7 logs, map F7).

## Expected output
Registry lists `ticket-agent` and `ticket-mcp`. In `DRY_RUN` both probes succeed and the gateway log shows one "would deny" for `refund_ticket`. After enforcement `lookup_ticket` succeeds, `refund_ticket` is denied with the gateway as the source, and Cloud Run logs show no request for it.

## Proof checklist
- [ ] Agent Registry shows an `Agent` and an `McpServer` resource with the right endpoints
- [ ] gateway exists, bound to `ticket-agent`, prior revisions archived (map C4)
- [ ] IAM policy shows `roles/iap.egressor` for the principal with the CEL condition
- [ ] dry-run log line "would deny" for `refund_ticket`; after enforce, a real deny with no matching Cloud Run request
- [ ] `lookup_ticket` still works through the gateway after enforce

## Cleanup
Leave the registry entries. Set the gateway back to `DRY_RUN` if G05 needs unfiltered traces; delete the gateway before deleting the agent.

## Next
`../06-a2a/` — the agent delegates to the workflow agent over A2A.
