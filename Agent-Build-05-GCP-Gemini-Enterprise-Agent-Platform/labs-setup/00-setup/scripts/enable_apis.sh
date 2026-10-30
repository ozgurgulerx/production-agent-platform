#!/usr/bin/env bash
# Enables the APIs the labs assume (map I6 plus Discovery Engine, Secret Manager, Cloud Run, Artifact Registry, Cloud Build, Model Armor).
# Idempotent. Reads GOOGLE_CLOUD_PROJECT from .env at the track root or from gcloud config.
set -euo pipefail
track_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
[ -f "$track_root/.env" ] && set -a && . "$track_root/.env" && set +a
project="${GOOGLE_CLOUD_PROJECT:-$(gcloud config get-value project 2>/dev/null)}"
[ -n "$project" ] || { echo "Set GOOGLE_CLOUD_PROJECT in .env" >&2; exit 1; }

apis=(
  aiplatform.googleapis.com
  storage.googleapis.com
  logging.googleapis.com
  monitoring.googleapis.com
  telemetry.googleapis.com
  cloudtrace.googleapis.com
  cloudresourcemanager.googleapis.com
  discoveryengine.googleapis.com
  secretmanager.googleapis.com
  run.googleapis.com
  artifactregistry.googleapis.com
  cloudbuild.googleapis.com
  modelarmor.googleapis.com
  iam.googleapis.com
)
echo "Enabling ${#apis[@]} APIs on $project ..."
gcloud services enable "${apis[@]}" --project "$project"
echo "Done. Verify: gcloud services list --enabled --project $project | grep -E 'aiplatform|discoveryengine|run'"
