#!/usr/bin/env bash
# deploy_three_ways.sh: the same ticket-agent deployed by CLI, SDK and Terraform (map C2, I7, I8).
# Each way is a function; run one at a time: `bash deploy_three_ways.sh cli|sdk|tf`.
# Status 25 Oct 2026: scaffold only, functionality unverified. Nothing here has been run.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$HERE/../.."                                   # track root, holds .env
# shellcheck disable=SC1091
source "$ROOT/labs-setup/.venv/bin/activate"
set -a; source "$ROOT/.env"; set +a
AGENT_DIR="$HERE/../labs/01-deploy-pipeline"          # agent.py + .agent_engine_config.json

way_cli() {
  # B6, C2: config file carries identity_type, staging bucket and env; flags only name the target.
  # With AGENT_RUNTIME_RESOURCE set, update the existing resource instead of creating another.
  local id_flag=()
  if [[ -n "${AGENT_RUNTIME_RESOURCE:-}" ]]; then
    id_flag=(--agent_engine_id "${AGENT_RUNTIME_RESOURCE##*/}")
  fi
  adk deploy agent_engine "$AGENT_DIR" \
    --project "$GOOGLE_CLOUD_PROJECT" \
    --region "$GOOGLE_CLOUD_LOCATION" \
    --display_name ticket-agent \
    --otel_to_cloud \
    --agent_engine_config_file "$AGENT_DIR/.agent_engine_config.json" \
    "${id_flag[@]}"
  # TODO(learner): capture the printed reasoningEngines/<ID> and write AGENT_RUNTIME_RESOURCE into .env.
}

way_sdk() {
  # I7: one config dictionary. traffic_split.py holds get_or_create and the update call.
  python "$HERE/traffic_split.py" deploy --agent-dir "$AGENT_DIR"
}

way_tf() {
  # I8: Terraform needs the pickle and requirements objects to exist first (produced by the SDK path).
  # TODO(learner): upload agent.pkl and requirements.txt to $AGENT_RUNTIME_STAGING_BUCKET/ticket-agent/
  terraform -chdir="$AGENT_DIR/terraform" init
  terraform -chdir="$AGENT_DIR/terraform" plan \
    -var "project_id=$GOOGLE_CLOUD_PROJECT" \
    -var "region=$GOOGLE_CLOUD_LOCATION" \
    -var "staging_bucket=${AGENT_RUNTIME_STAGING_BUCKET#gs://}" \
    -var "ticket_mcp_url=${TICKET_MCP_URL:-}"
  # No apply in the lab; read the plan.
}

verify() {
  # I10, C5: resource exists and runs under a SPIFFE principal.
  gcloud ai reasoning-engines describe "${AGENT_RUNTIME_RESOURCE##*/}" \
    --project "$GOOGLE_CLOUD_PROJECT" --region "$GOOGLE_CLOUD_LOCATION" \
    --format 'value(spec.effectiveIdentity)'
}

case "${1:-}" in
  cli) way_cli ;;
  sdk) way_sdk ;;
  tf)  way_tf ;;
  verify) verify ;;
  *) echo "usage: $0 cli|sdk|tf|verify" >&2; exit 2 ;;
esac
