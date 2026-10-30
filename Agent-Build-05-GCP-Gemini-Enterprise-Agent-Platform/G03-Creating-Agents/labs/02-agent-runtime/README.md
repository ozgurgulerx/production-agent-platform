# 02 — `ticket-agent` on Agent Runtime: CLI deploy, SDK deploy, `:query`, revisions, registration

The same `ticket_agent/` folder from lab 01, put on Agent Runtime (ex-Vertex AI Agent Engine; the API resource is still `ReasoningEngine`, A1, A5). Two deploy paths produce the same resource: `adk deploy agent_engine` (way 5, C2) and `agentplatform.Client().runtimes.create` (way 6, I7). Then the resource is called through `:query`, given a second revision, rolled back by traffic split, and registered in Gemini Enterprise (way 9, C8). The resource path goes into `.env` as `AGENT_RUNTIME_RESOURCE`; every later lab reads it.

| #   | Way                   | Command                                         | Status (25 Oct 2026)                                 | Map        |
| --- | --------------------- | ----------------------------------------------- | ---------------------------------------------------- | ---------- |
| 5   | CLI                   | `adk deploy agent_engine ... ticket_agent`      | GA                                                   | B6, C2, C3 |
| 6   | SDK                   | `deploy_sdk.py` → `client.runtimes.create(...)` | GA; `vertexai.agent_engines` legacy since 2026-09-18 | A2, A5, I7 |
| 9   | Gemini Enterprise     | console or REST v1alpha                         | GA                                                   | C8         |
| –   | revisions and traffic | `revisions.py`                                  | preview (v1beta1)                                    | C4         |

## Prerequisites

Lab 01 done (the `ticket_agent/` folder answers under `adk web`). `.env` has `AGENT_RUNTIME_STAGING_BUCKET` (same region, A9) and the roles from `labs-setup/00-setup` (`roles/aiplatform.user`, `agentContextEditor`, `agentDefaultAccess`, `storage.admin`, I6). `google-cloud-agentplatform` 2.6.0 is in the shared venv; the CLI refuses to deploy without `client.runtimes` (C2).

## Files

```
02-agent-runtime/
├── ticket_agent/                 symlink or copy of ../01-ways-to-run/ticket_agent (TODO(learner): copy it; a symlink is not packaged)
├── .agent_engine_config.json     identity_type AGENT_IDENTITY, display_name, env_vars (B6, C5)
├── deploy_sdk.py                 way 6: get-or-create by display_name, runtimes.create, write AGENT_RUNTIME_RESOURCE
├── query.py                      :query and :streamQuery against AGENT_RUNTIME_RESOURCE (C3)
├── revisions.py                  list revisions, manual traffic split to an earlier revision, back to always-latest (C4)
├── requirements.txt
└── test_02_agent_runtime.py
```

## Run

```bash
source ../../../labs-setup/.venv/bin/activate
cd 02-agent-runtime && cp -r ../01-ways-to-run/ticket_agent .      # once

# Way 5: CLI. Config comes from .agent_engine_config.json (default --agent_engine_config_file, B6).
adk deploy agent_engine --project "$GOOGLE_CLOUD_PROJECT" --region "$GOOGLE_CLOUD_LOCATION" \
  --display_name ticket-agent --otel_to_cloud ticket_agent
# Output ends with projects/P/locations/L/reasoningEngines/ID (C3). Write it into .env:
#   AGENT_RUNTIME_RESOURCE=projects/P/locations/L/reasoningEngines/ID
# Re-deploys MUST pass --agent_engine_id ID, or each run creates a new agent (B6).

# Way 6: SDK. Reuses the resource if one with display_name ticket-agent exists; else creates; writes .env for you.
python deploy_sdk.py

# Call it (C3)
python query.py "My card was charged twice for order 8841. Ticket 1042."
gcloud ai reasoning-engines describe "${AGENT_RUNTIME_RESOURCE##*/}" --project "$GOOGLE_CLOUD_PROJECT" --region "$GOOGLE_CLOUD_LOCATION"   # I10; spec.effectiveIdentity shows the SPIFFE principal (C5)

# Revisions and traffic (preview, C4): change the instruction, redeploy with --agent_engine_id, then
python revisions.py list
python revisions.py pin <earlier-revision-id>      # manual split, 100 % to the earlier active revision = rollback
python revisions.py latest                        # back to trafficSplitAlwaysLatest

# Way 9: Gemini Enterprise, console: app → Agents → Add agent → "Custom agent via Agent Runtime" → paste AGENT_RUNTIME_RESOURCE (C8).
# App location (global/us/eu) must match the region prefix; europe-west2 → eu (C8).
```

## Expected output

- `adk deploy agent_engine` prints the generated requirements (`google-cloud-aiplatform[adk,agent_engines]>=2.2,<3`, `google-adk[a2a]==2.13.0`, C2), then a `reasoningEngines/<ID>` line.
- `deploy_sdk.py` prints `[get-or-create] reusing ticket-agent ...` on the second run, never a second create.
- `query.py` prints the agent's answer; `:streamQuery` prints chunks.
- `describe` shows `spec.effectiveIdentity` with `principal://...` (C5), not a service account email.
- `revisions.py list` shows two revisions after the redeploy; after `pin` the old instruction answers; after `latest` the new one does.

## What each step proves

- The CLI is `runtimes.create` then `runtimes.update` (C2); `.agent_engine_config.json` is where `identity_type` lives (C5).
- `identity_type=AGENT_IDENTITY` needs `api_version="v1beta1"` on the client (C5); unset means a service account.
- Rollback has no verb; it is a manual traffic split to an active revision (C4). Archived revisions cannot come back.
- Quotas: 10 create/update/delete per minute, 90 `Query`/`StreamQuery` per minute, 950 revisions per agent (A10).
- Gemini Enterprise points at the resource; it does not run the agent (C8).

## Proof (checklist)

- [ ] `.env` contains `AGENT_RUNTIME_RESOURCE=projects/.../reasoningEngines/...` written by this lab
- [ ] `deploy_sdk.py` run twice: second run says reusing, `gcloud ai reasoning-engines list` shows one `ticket-agent`
- [ ] `query.py` returns a refusal with a policy citation for the goodwill refund turn
- [ ] `describe` shows `spec.effectiveIdentity` as a `principal://` (Agent Identity, not a service account)
- [ ] `revisions.py` shows the pin and the return to latest, with a visibly different answer
- [ ] `ticket-agent` appears in the Gemini Enterprise app's Agents list (or the REST call returns 200)
- [ ] `pytest test_02_agent_runtime.py` runs the tests you wrote

## Cleanup

Keep `ticket-agent`: G04 and G05 need it. For a throwaway copy: `python deploy_sdk.py --delete <display_name>` calls `delete(force=True)` (C1). Deleting and recreating yields a new Agent Identity principal (D10).

## Next

`../03-multi-agent-workflow/`: the same deploy command on a `SequentialAgent`.
