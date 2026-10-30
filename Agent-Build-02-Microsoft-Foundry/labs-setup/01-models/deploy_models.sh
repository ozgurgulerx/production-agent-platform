#!/usr/bin/env bash
# Creates the four model deployments the labs need, idempotently. Entra only (az login).
# Reads .env at the track root. Override SKU/capacity with SKU_NAME / SKU_CAPACITY.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
env_file="$(cd "$here/../.." && pwd)/.env"
[ -f "$env_file" ] || { echo "Missing $env_file (copy .env.example)"; exit 1; }
set -a; # shellcheck disable=SC1090
source "$env_file"; set +a
: "${FOUNDRY_ACCOUNT_NAME:?set in .env}" "${AZ_RESOURCE_GROUP:?set in .env}"
SKU_NAME="${SKU_NAME:-GlobalStandard}"; SKU_CAPACITY="${SKU_CAPACITY:-50}"

# deployment-name|model-name|format
wanted=(
  "${FOUNDRY_MODEL:-gpt-5-mini}|${FOUNDRY_MODEL:-gpt-5-mini}|OpenAI"
  "${FOUNDRY_REASONING_MODEL:-gpt-5-mini}|${FOUNDRY_REASONING_MODEL:-gpt-5-mini}|OpenAI"
  "${FOUNDRY_EMBEDDING_MODEL:-text-embedding-3-small}|${FOUNDRY_EMBEDDING_MODEL:-text-embedding-3-small}|OpenAI"
  "${FOUNDRY_VOICE_MODEL:-gpt-realtime}|${FOUNDRY_VOICE_MODEL:-gpt-realtime}|OpenAI"
)
existing="$(az cognitiveservices account deployment list -n "$FOUNDRY_ACCOUNT_NAME" -g "$AZ_RESOURCE_GROUP" --query "[].name" -o tsv)"
seen=""
for row in "${wanted[@]}"; do
  IFS='|' read -r dep model fmt <<<"$row"
  case " $seen " in *" $dep "*) continue;; esac; seen="$seen $dep"
  if grep -qx "$dep" <<<"$existing"; then echo "exists: $dep"; continue; fi
  version="$(az cognitiveservices account list-models -n "$FOUNDRY_ACCOUNT_NAME" -g "$AZ_RESOURCE_GROUP" \
      --query "[?name=='$model' && format=='$fmt'] | [0].version" -o tsv)"
  [ -n "$version" ] || { echo "model $model ($fmt) not available on this account/region; skipping"; continue; }
  cap="$SKU_CAPACITY"; [ "$model" = "gpt-realtime" ] && cap=1
  echo "creating: $dep <- $model $version ($SKU_NAME, capacity $cap)"
  az cognitiveservices account deployment create -n "$FOUNDRY_ACCOUNT_NAME" -g "$AZ_RESOURCE_GROUP" \
    --deployment-name "$dep" --model-name "$model" --model-version "$version" --model-format "$fmt" \
    --sku-name "$SKU_NAME" --sku-capacity "$cap" -o none
done
az cognitiveservices account deployment list -n "$FOUNDRY_ACCOUNT_NAME" -g "$AZ_RESOURCE_GROUP" \
  --query "[].{deployment:name,model:properties.model.name,version:properties.model.version,sku:sku.name,capacity:sku.capacity}" -o table
