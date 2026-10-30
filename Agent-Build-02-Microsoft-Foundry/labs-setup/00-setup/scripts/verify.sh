#!/usr/bin/env bash
# Verifies tooling, login, azd Foundry extensions, Python deps and the .env contract.
set -euo pipefail

setup_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"   # labs-setup/
track_root="$(cd "$setup_root/.." && pwd)"                            # Agent-Build-02-Microsoft-Foundry/
cd "$setup_root"
fail() { echo "FAIL: $*" >&2; exit 1; }

echo "Verifying local environment..."
command -v az  >/dev/null 2>&1 || fail "Azure CLI (az) not found"
command -v azd >/dev/null 2>&1 || fail "Azure Developer CLI (azd) not found"
echo "- az:  $(az version --query '\"azure-cli\"' -o tsv 2>/dev/null)"
echo "- azd: $(azd version 2>/dev/null | head -n 1)"

echo "Checking Azure login..."
az account show --query '{subscription:name,tenant:tenantId}' -o tsv >/dev/null 2>&1 || fail "Not logged in. Run: az login"
echo "- az account show: ok"
azd auth login --check-status >/dev/null 2>&1 || echo "- WARN: azd not logged in. Run: azd auth login"

echo "Checking azd Foundry extension (azure.ai.agents)..."
if azd ext show azure.ai.agents >/dev/null 2>&1; then
  echo "- azd ext azure.ai.agents: $(azd ext show azure.ai.agents 2>/dev/null | grep -i version | head -1)"
else
  echo "- WARN: run: azd ext install microsoft.foundry   (installs azure.ai.agents, connections, toolboxes, ...)"
fi

[ -f ".venv/bin/activate" ] || fail "labs-setup/.venv missing. Run: bash labs-setup/00-setup/scripts/bootstrap_venv.sh"
# shellcheck disable=SC1091
source .venv/bin/activate
echo "- python: $(python --version)"
python - <<'PY' || fail "Python deps missing or wrong generation. Re-run bootstrap_venv.sh"
import azure.ai.projects, agent_framework
from agent_framework.foundry import FoundryChatClient, FoundryAgent
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.ai.projects.models import PromptAgentDefinition, HostedAgentDefinition
v = tuple(int(x) for x in azure.ai.projects.__version__.split(".")[:2])
assert v >= (2, 2), f"azure-ai-projects {azure.ai.projects.__version__} is too old (need 2.x)"
print(f"- azure-ai-projects {azure.ai.projects.__version__}, agent-framework-foundry ok, hosting ok")
PY

[ -f "$track_root/.env" ] || fail ".env missing. Copy .env.example to .env at the track root ($track_root)"
set -a; # shellcheck disable=SC1091
source "$track_root/.env"; set +a
[ -n "${FOUNDRY_PROJECT_ENDPOINT:-}" ] || fail "FOUNDRY_PROJECT_ENDPOINT is empty in .env"
case "$FOUNDRY_PROJECT_ENDPOINT" in
  https://*.services.ai.azure.com/api/projects/*) echo "- FOUNDRY_PROJECT_ENDPOINT: shape ok";;
  *) fail "FOUNDRY_PROJECT_ENDPOINT must look like https://<resource>.services.ai.azure.com/api/projects/<project>";;
esac
[ -n "${FOUNDRY_MODEL:-}" ] || fail "FOUNDRY_MODEL is empty in .env"

echo "Checking the project endpoint answers (lists agents)..."
python - <<'PY' || fail "Could not list agents on the project. Check RBAC (Foundry User) and the endpoint."
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
p = AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"], credential=DefaultAzureCredential())
names = [a.name for a in p.agents.list()]
print(f"- project reachable, {len(names)} agent(s) present")
PY
echo "OK"
