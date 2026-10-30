#!/usr/bin/env bash
# Proves: an agent is a folder of YAML. `init` scaffolds offline; `clone` pulls the real C03 ticket agent.
# Needs: pac installed; for the clone step a pac auth profile on the dev environment and AGENT_SCHEMA_NAME in .env.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
root="$(cd "$here/../../.." && pwd)"                      # track root, where .env lives
[ -f "$root/.env" ] && { set -a; . "$root/.env"; set +a; }

command -v pac >/dev/null || { echo "pac not found: dotnet tool install --global Microsoft.PowerApps.CLI.Tool"; exit 1; }
echo "pac $(pac --version 2>/dev/null | head -1)"

# 1. offline scaffold: no environment, no auth
rm -rf "$here/scaffold" && mkdir -p "$here/scaffold"
pac copilot init --outputDirectory "$here/scaffold/ticket-agent-scaffold" --authoring-mode cli-copilot    # verify: flag names (C1)
echo "-- scaffold tree:"; find "$here/scaffold" -type f | sed "s|$here/||" | sort

# 2. clone the real agent (needs pac auth + env)
if [ -n "${AGENT_SCHEMA_NAME:-}" ]; then
  pac env select --environment "${ENVIRONMENT_ID:?ENVIRONMENT_ID missing in .env}"
  rm -rf "$here/ticket-agent"
  pac copilot clone --schemaName "$AGENT_SCHEMA_NAME" --outputDirectory "$here/ticket-agent"          # verify: option names (C1)
  echo "-- clone tree (record this in README.md, Learn does not enumerate it):"
  find "$here/ticket-agent" -type f | sed "s|$here/||" | sort
  git -C "$here/ticket-agent" init -q 2>/dev/null || true
  git -C "$here/ticket-agent" add -A && git -C "$here/ticket-agent" commit -q -m "clone of $AGENT_SCHEMA_NAME" || true
  echo "-- status:"; pac copilot status --path "$here/ticket-agent"                                      # verify
else
  echo "AGENT_SCHEMA_NAME empty: skipping clone (publish the C03 lab 01 agent first)"
fi
