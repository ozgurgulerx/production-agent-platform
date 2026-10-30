#!/usr/bin/env bash
# Prints OK when .env, pac, the venv and a device-code token are ready for session 1. Read-only.
set -uo pipefail
root="$(cd "$(dirname "$0")/../../.." && pwd)"; venv="$root/labs-setup/.venv"
fail=0; ok(){ echo "  ok   $1"; }; bad(){ echo "  FAIL $1"; fail=1; }
[ -f "$root/.env" ] && ok ".env present" || bad ".env missing (cp .env.example .env)"
set -a; [ -f "$root/.env" ] && . "$root/.env"; set +a
for v in TENANT_ID CLIENT_ID ENVIRONMENT_ID ENVIRONMENT_URL; do [ -n "${!v:-}" ] && ok "$v set" || bad "$v empty"; done
command -v pac >/dev/null && ok "pac $(pac --version 2>/dev/null | head -1)" || bad "pac missing (dotnet tool install --global Microsoft.PowerApps.CLI.Tool)"
command -v pac >/dev/null && { pac auth list 2>/dev/null | grep -q "\*" && ok "pac auth profile active" || bad "no active pac auth (pac auth create --deviceCode)"; }
"$venv/bin/python" -c "import microsoft_agents.copilotstudio.client, microsoft_agents.hosting.aiohttp, msal, mcp; print('  ok   venv imports')" 2>/dev/null || bad "venv imports (run scripts/bootstrap_venv.sh)"
"$venv/bin/python" "$root/labs-setup/00-setup/scripts/whoami.py" && ok "device-code token + Dataverse WhoAmI" || bad "token or WhoAmI failed (consent? ENVIRONMENT_URL?)"
grep -rqE "client_secret\s*=\s*['\"][^'\"]+['\"]" "$root" --include='*.py' --exclude-dir=.venv 2>/dev/null && bad "a client secret literal is in the track" || ok "no secret literals"
[ $fail -eq 0 ] && echo OK || { echo "NOT READY"; exit 1; }
