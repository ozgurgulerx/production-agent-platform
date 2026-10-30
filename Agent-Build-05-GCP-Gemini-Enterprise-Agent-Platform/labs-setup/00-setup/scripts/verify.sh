#!/usr/bin/env bash
# Prints OK when the shared environment is usable: venv, pins, ADC, project, APIs, bucket.
set -euo pipefail
track_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
fail() { echo "FAIL: $*" >&2; exit 1; }

[ -f "$track_root/.env" ] || fail ".env missing at track root (cp .env.example .env)"
set -a; . "$track_root/.env"; set +a
[ -n "${GOOGLE_CLOUD_PROJECT:-}" ] || fail "GOOGLE_CLOUD_PROJECT empty"
[ -n "${GOOGLE_CLOUD_LOCATION:-}" ] || fail "GOOGLE_CLOUD_LOCATION empty"

python -c "import google.adk, sys; v=google.adk.__version__; print('google-adk', v); sys.exit(0 if v.startswith('2.') else 1)" || fail "google-adk 2.x not in the active venv (source labs-setup/.venv/bin/activate)"
python -c "import google.genai; print('google-genai', google.genai.__version__)" || fail "google-genai missing"
python -c "import agentplatform; print('google-cloud-agentplatform ok')" || fail "google-cloud-agentplatform missing (adk deploy needs it, map C2)"

gcloud auth application-default print-access-token >/dev/null 2>&1 || fail "no ADC: gcloud auth application-default login"
gcloud projects describe "$GOOGLE_CLOUD_PROJECT" --format='value(projectId)' >/dev/null || fail "cannot read project $GOOGLE_CLOUD_PROJECT"

for api in aiplatform.googleapis.com discoveryengine.googleapis.com run.googleapis.com; do
  gcloud services list --enabled --project "$GOOGLE_CLOUD_PROJECT" --filter="config.name=$api" --format='value(config.name)' | grep -q "$api" || fail "$api not enabled (run 00-setup/scripts/enable_apis.sh)"
done

if [ -n "${AGENT_RUNTIME_STAGING_BUCKET:-}" ]; then
  gcloud storage buckets describe "$AGENT_RUNTIME_STAGING_BUCKET" --format='value(name)' >/dev/null || fail "staging bucket $AGENT_RUNTIME_STAGING_BUCKET not found"
fi
echo "OK"
