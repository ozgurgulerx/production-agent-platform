#!/usr/bin/env bash
# The whole C07 loop as commands. Shape-only sketch: flags copied from the pac copilot reference (reading map C1,
# updated 2026-07-10) and still marked verify until the first run against the tenant. No secrets; auth is device code.
set -euo pipefail

AGENT_SCHEMA_NAME="${AGENT_SCHEMA_NAME:?set in .env}"      # e.g. cr1ab_ticketAgent
ENVIRONMENT_ID="${ENVIRONMENT_ID:?set in .env}"
WORK=./ticket-agent

# 0. one-time auth, interactive, no client secret
pac auth create --deviceCode                                  # verify: flag spelling on your pac version
pac env select --environment "$ENVIRONMENT_ID"

# 1. clone once (or init a new agent)
pac copilot clone --schemaName "$AGENT_SCHEMA_NAME" --outputDirectory "$WORK"        # verify: option names
# pac copilot init --environment "$ENVIRONMENT_ID" --outputDirectory "$WORK"         # new agent, bootstrapped in the environment
# pac copilot init --outputDirectory "$WORK" --authoring-mode cli-copilot            # offline scaffold (C1)

# 2. branch and edit
git -C "$WORK" checkout -b feat/refund-cap-wording
#   ... edit instructions / topics YAML ...

# 3. pull (three-way merge against last sync) before pushing; a conflict stops the push, there is no --force
pac copilot pull  --path "$WORK"                              # verify: --path vs positional
pac copilot push  --path "$WORK"
pac copilot publish --schemaName "$AGENT_SCHEMA_NAME"         # new sessions get the new content (L1)

# 4. CI path: pack needs no auth; import needs a service principal / federated credential
pac copilot pack --path "$WORK" --outputFile ./out/ticket-agent.zip     # "safe to run in a build pipeline" (C1)
pac solution import --path ./out/ticket-agent.zip --environment "$ENVIRONMENT_ID" --publish-changes   # verify flags

# 5. gate: C05 evaluation REST API (I3) runs after import; see ../labs/01-dev-loop/ci_pipeline.yml
