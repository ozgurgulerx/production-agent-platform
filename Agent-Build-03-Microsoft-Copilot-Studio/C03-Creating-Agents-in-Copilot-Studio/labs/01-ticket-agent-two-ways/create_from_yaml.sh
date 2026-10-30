#!/usr/bin/env bash
# Way 2 from zero: scaffold locally, pack a solution offline (no auth, pipeline-safe, C1), import, publish.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"; set -a; . "$here/../../../.env"; set +a
pac copilot init --directory "$here/agent-from-yaml" --environment "$ENVIRONMENT_ID" --authoring-mode cli-copilot   # verify flags
cp "$here/instructions.md" "$here/agent-from-yaml/"   # verify: where the scaffold expects instructions
pac copilot pack --directory "$here/agent-from-yaml" --outputFile "$here/ticket-agent.zip"                           # verify
pac solution import --path "$here/ticket-agent.zip" --environment "$ENVIRONMENT_ID" --publish-changes
pac copilot list --environment "$ENVIRONMENT_ID"
echo "then: pac copilot publish --environment $ENVIRONMENT_ID --agent <schema name printed above>"
