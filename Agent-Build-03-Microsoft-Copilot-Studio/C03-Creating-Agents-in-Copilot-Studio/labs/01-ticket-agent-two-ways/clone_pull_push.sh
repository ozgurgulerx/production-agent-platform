#!/usr/bin/env bash
# Way 2: the portal agent becomes YAML in Git, is edited, pushed back and published (C1). Flags marked verify
# against `pac copilot --help` on your machine; the command set is init/clone/pull/push/pack/publish/list/status.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"; set -a; . "$here/../../../.env"; set +a
pac auth list
pac copilot list --environment "$ENVIRONMENT_ID"
pac copilot clone --environment "$ENVIRONMENT_ID" --agent "$AGENT_SCHEMA_NAME" --outputDirectory "$here/agent"   # verify flag names
echo "cloned to $here/agent; edit agent/instructions (or the YAML) now, then:"
echo "  git add -A && git commit -m 'ticket agent: tighten refund wording'"
read -r -p "press enter to pull (three-way merge), push and publish..."
pac copilot pull --environment "$ENVIRONMENT_ID" --directory "$here/agent"      # verify
pac copilot push --environment "$ENVIRONMENT_ID" --directory "$here/agent"      # conflict stops push (C1)
pac copilot publish --environment "$ENVIRONMENT_ID" --agent "$AGENT_SCHEMA_NAME"   # verify
pac copilot status --environment "$ENVIRONMENT_ID" --agent "$AGENT_SCHEMA_NAME"    # verify
