#!/usr/bin/env bash
# G04 lab 03: MCP Toolbox on Cloud Run with Google auth (map D8). Prints TICKET_MCP_URL at the end.
# Status: scaffold only, functionality unverified. Run from this folder with .env sourced.
set -euo pipefail
P=${GOOGLE_CLOUD_PROJECT:?}; L=${GOOGLE_CLOUD_LOCATION:?}
SA=${TOOLBOX_SERVICE_ACCOUNT:-toolbox-identity}
IMAGE=us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:1.15.0      # pin, not :latest (map D6)

gcloud iam service-accounts create "$SA" --project "$P" 2>/dev/null || true
gcloud secrets create tools --data-file=tools.yaml --project "$P" 2>/dev/null \
  || gcloud secrets versions add tools --data-file=tools.yaml --project "$P"
gcloud secrets add-iam-policy-binding tools --project "$P" \
  --member="serviceAccount:$SA@$P.iam.gserviceaccount.com" --role=roles/secretmanager.secretAccessor >/dev/null

# TODO(learner): grant $SA roles/cloudsql.client and pass the DB env vars (TICKETS_DB_HOST etc.) via --set-env-vars /
# --set-secrets; the Cloud SQL connection method (private IP vs connector) is outside the map: unverified, pick one and note it.
gcloud run deploy ticket-mcp --project "$P" --region "$L" --image "$IMAGE" \
  --service-account "$SA@$P.iam.gserviceaccount.com" \
  --set-secrets "/app/tools.yaml=tools:latest" \
  --args="--config=/app/tools.yaml,--address=0.0.0.0,--port=8080" \
  --no-allow-unauthenticated

URL=$(gcloud run services describe ticket-mcp --project "$P" --region "$L" --format='value(status.url)')
echo "TICKET_MCP_URL=$URL"
echo "Now: write TICKET_MCP_URL into ../../../.env and grant roles/run.invoker to the agent principal (README step 4)."
