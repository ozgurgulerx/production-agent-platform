#!/usr/bin/env bash
# Untested sketch. Model Armor floor setting bound to the platform (map F2, page 2026-10-22).
# Floor = project minimum every agent gets; templates attached per request cannot be weaker (F1).
# Stage with INSPECT_ONLY, read the findings in Cloud Logging, then flip to INSPECT_AND_BLOCK.
set -euo pipefail
: "${GOOGLE_CLOUD_PROJECT:?}"
ENFORCEMENT="${1:-INSPECT_ONLY}"   # INSPECT_ONLY | INSPECT_AND_BLOCK
PROJECT_NUMBER=$(gcloud projects describe "$GOOGLE_CLOUD_PROJECT" --format='value(projectNumber)')

# The platform's service agent must be allowed to call Model Armor (F2).
gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
  --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-aiplatform.iam.gserviceaccount.com" \
  --role="roles/modelarmor.user" --condition=None >/dev/null

# gcloud still spells the integration VERTEX_AI; the REST field is integratedServices: ["AI_PLATFORM"] (F2).
gcloud model-armor floorsettings update \
  --full-uri="projects/${GOOGLE_CLOUD_PROJECT}/locations/global/floorSetting" \
  --add-integrated-services=VERTEX_AI \
  --vertex-ai-enforcement-type="$ENFORCEMENT"

# TODO(learner): the filter-level flags (RAI categories, prompt injection confidence, SDP) are on the floor-settings
# reference page, which could not be fetched on 25 Oct 2026 (map Gaps). Add them here once read; mark unverified until then.
gcloud model-armor floorsettings describe --full-uri="projects/${GOOGLE_CLOUD_PROJECT}/locations/global/floorSetting"
