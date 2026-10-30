#!/usr/bin/env bash
# Deploy the ticket MCP server to Azure Container Apps with external HTTPS ingress and write TICKET_MCP_URL to .env.
# Needs `az login`. Set TICKET_MCP_API_KEY to deploy in API-key mode.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"; track_root="$(cd "$here/../../../.." && pwd)"
RG="${RG:-rg-copilot-studio-labs}"; LOC="${LOC:-uksouth}"; APP="${APP:-ticket-mcp}"; ENVN="${ENVN:-cae-copilot-studio-labs}"
az group create -n "$RG" -l "$LOC" -o none
args=(--name "$APP" --resource-group "$RG" --location "$LOC" --environment "$ENVN" --source "$here" --ingress external --target-port 8000)
[ -n "${TICKET_MCP_API_KEY:-}" ] && args+=(--env-vars "TICKET_MCP_API_KEY=$TICKET_MCP_API_KEY")
az containerapp up "${args[@]}" -o none
fqdn=$(az containerapp show -n "$APP" -g "$RG" --query properties.configuration.ingress.fqdn -o tsv)
url="https://$fqdn/mcp"
grep -q '^TICKET_MCP_URL=' "$track_root/.env" && sed -i '' "s|^TICKET_MCP_URL=.*|TICKET_MCP_URL=$url|" "$track_root/.env" || echo "TICKET_MCP_URL=$url" >> "$track_root/.env"
echo "TICKET_MCP_URL=$url  (written to $track_root/.env)"
echo "cleanup: az group delete -n $RG --yes --no-wait"
