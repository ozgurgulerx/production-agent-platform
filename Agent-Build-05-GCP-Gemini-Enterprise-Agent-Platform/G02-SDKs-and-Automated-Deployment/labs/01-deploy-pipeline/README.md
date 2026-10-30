# 01 — Deploy pipeline: build, eval gate, deploy, traffic 10/90, promote

Goal: one `git push` (or one `gcloud builds submit`) produces a new revision of `ticket-agent` on Agent Runtime, gives it 10 percent of traffic, and a second manual step promotes it to 100 or rolls it back. Same agent, no new resource per run. Facts cite the map (`../../../reference/reading-map-gcp-agents-2026-10-25.md`).

## Prerequisites

- `../../../labs-setup/` done; `.env` at the track root with `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, `AGENT_RUNTIME_STAGING_BUCKET`, `GEMINI_MODEL`, and `TICKET_MCP_URL` (empty is fine; the lookup tool then answers from the stub).
- Roles from map I6 on your account; Cloud Build's service account needs the same deploy roles plus `roles/iam.serviceAccountUser` (unverified beyond I6, check the Cloud Build page).
- Terraform ≥1.5 only for the variant (`brew install terraform`).
- Optional scaffold: `uvx google-agents-cli setup` then `infra cicd` (I12), or `uvx agent-starter-pack create` (I11, maintenance mode). This lab ships its own `cloudbuild.yaml` so neither is required.

## Steps

```bash
cd Agent-Build-05-GCP-Gemini-Enterprise-Agent-Platform
source labs-setup/.venv/bin/activate
set -a; source .env; set +a
cd G02-SDKs-and-Automated-Deployment/labs/01-deploy-pipeline

# 1. local check of the agent definition
adk run .                                 # ask: "refund 300 GBP on ticket 42"; expect a policy refusal

# 2. first deploy by hand if AGENT_RUNTIME_RESOURCE is empty (C2, B6)
adk deploy agent_engine . --project "$GOOGLE_CLOUD_PROJECT" --region "$GOOGLE_CLOUD_LOCATION" \
  --display_name ticket-agent --otel_to_cloud --agent_engine_config_file .agent_engine_config.json
#    copy the printed reasoningEngines/<ID> into .env as AGENT_RUNTIME_RESOURCE (full resource path)

# 3. the pipeline, manually triggered
gcloud builds submit --config cloudbuild.yaml \
  --substitutions _REGION="$GOOGLE_CLOUD_LOCATION",_AGENT_ID="${AGENT_RUNTIME_RESOURCE##*/}",_NEW_TRAFFIC=10 .

# 4. inspect revisions and traffic (C4; preview, v1beta1)
python ../../sketches/traffic_split.py split --new 10      # idempotent re-run of the pipeline's step
gcloud ai reasoning-engines describe "${AGENT_RUNTIME_RESOURCE##*/}" --region "$GOOGLE_CLOUD_LOCATION"

# 5. promote or roll back
python ../../sketches/traffic_split.py promote
python ../../sketches/traffic_split.py rollback

# 6. Terraform variant (plan only)
terraform -chdir=terraform init && terraform -chdir=terraform plan \
  -var project_id="$GOOGLE_CLOUD_PROJECT" -var region="$GOOGLE_CLOUD_LOCATION" \
  -var staging_bucket="${AGENT_RUNTIME_STAGING_BUCKET#gs://}"

# 7. tests (collect only until you write them)
pytest -q
```

## Expected output

- Step 2 prints a line ending in `reasoningEngines/<ID>` (C3).
- Step 3 ends with the eval-gate placeholder step printing `EVAL GATE: placeholder, wire adk eval here (E1, E7)` and the deploy step printing the same resource id, not a new one.
- Step 4 shows two active revisions; `spec.effectiveIdentity` is a `principal://` SPIFFE string (C5).
- Step 5 leaves one revision at 100 percent in either direction.
- Step 6 plan shows one `google_vertex_ai_reasoning_engine` to create or update and no destroy.

## Proof checklist (tick with real output, not intent)

- [ ] `adk run .` refuses the out-of-policy refund and the lookup tool is called once
- [ ] one `ticket-agent` in `gcloud ai reasoning-engines list --region $GOOGLE_CLOUD_LOCATION` after two pipeline runs
- [ ] build log shows build, eval gate, deploy, traffic, promote steps in that order
- [ ] `revisions.list` shows the new revision at 10 and the previous at 90
- [ ] `:query` against the resource returns a policy refusal (C3)
- [ ] rollback moves traffic without creating a revision
- [ ] `terraform plan` completes with no destroy
- [ ] `pytest -q` reports your tests, not an empty collection

## Cleanup

```bash
python ../../sketches/traffic_split.py prune --keep 2     # revisions; 950 cap (A10)
# delete the agent only if G03/G04 are not using it: runtimes.delete(force=True) in the SDK, or
gcloud ai reasoning-engines delete "${AGENT_RUNTIME_RESOURCE##*/}" --region "$GOOGLE_CLOUD_LOCATION"
```

## Known gaps

No first-party page wires `adk eval` into Cloud Build (E7); the gate is a placeholder step you replace with `adk eval . tests/ticket.evalset.json` (E1) or `agents-cli eval run` (I12). The `traffic_config` request shape is not in the fetched page body (C4); read it before writing `split()`. Whether the Terraform provider manages traffic is unverified. Nothing here has been run.

Status on 25 Oct 2026: scaffold only, functionality unverified.
