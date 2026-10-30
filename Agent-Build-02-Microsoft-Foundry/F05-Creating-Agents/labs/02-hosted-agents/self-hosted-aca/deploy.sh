#!/usr/bin/env bash
# Deploys the self-hosted agent to Azure Container Apps with a system-assigned identity that
# has Foundry User on the project, then prints the public /responses URL.
# Usage: set -a; source ../../../../.env; set +a; bash deploy.sh   (.env lives at the track root)
set -euo pipefail
: "${AZ_RESOURCE_GROUP:?}" "${FOUNDRY_PROJECT_ENDPOINT:?}" "${FOUNDRY_MODEL:?}" "${AZ_SUBSCRIPTION_ID:?}" "${FOUNDRY_ACCOUNT_NAME:?}" "${FOUNDRY_PROJECT_NAME:?}"
APP=${APP:-ticket-agent-self-hosted}
ENVNAME=${ENVNAME:-foundry-demo-aca-env}
LOCATION=${LOCATION:-$(az group show -n "$AZ_RESOURCE_GROUP" --query location -o tsv)}

az extension add --name containerapp --upgrade --only-show-errors
az containerapp env show -g "$AZ_RESOURCE_GROUP" -n "$ENVNAME" >/dev/null 2>&1 || \
  az containerapp env create -g "$AZ_RESOURCE_GROUP" -n "$ENVNAME" -l "$LOCATION" --only-show-errors

# Source-to-cloud build (no local Docker needed), public ingress on 8088, system identity.
az containerapp up -g "$AZ_RESOURCE_GROUP" -n "$APP" --environment "$ENVNAME" --source . \
  --ingress external --target-port 8088 \
  --env-vars FOUNDRY_PROJECT_ENDPOINT="$FOUNDRY_PROJECT_ENDPOINT" AZURE_AI_MODEL_DEPLOYMENT_NAME="$FOUNDRY_MODEL" \
  --only-show-errors
az containerapp identity assign -g "$AZ_RESOURCE_GROUP" -n "$APP" --system-assigned --only-show-errors >/dev/null
PRINCIPAL=$(az containerapp show -g "$AZ_RESOURCE_GROUP" -n "$APP" --query identity.principalId -o tsv)
SCOPE="/subscriptions/$AZ_SUBSCRIPTION_ID/resourceGroups/$AZ_RESOURCE_GROUP/providers/Microsoft.CognitiveServices/accounts/$FOUNDRY_ACCOUNT_NAME/projects/$FOUNDRY_PROJECT_NAME"
az role assignment create --assignee-object-id "$PRINCIPAL" --assignee-principal-type ServicePrincipal \
  --role "Azure AI User" --scope "$SCOPE" --only-show-errors >/dev/null || true
FQDN=$(az containerapp show -g "$AZ_RESOURCE_GROUP" -n "$APP" --query properties.configuration.ingress.fqdn -o tsv)
echo "SELF_HOSTED_URL=https://$FQDN"
echo "Invoke: python invoke.py https://$FQDN"
