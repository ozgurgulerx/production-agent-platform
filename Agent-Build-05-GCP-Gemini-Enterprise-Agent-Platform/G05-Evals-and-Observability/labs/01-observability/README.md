# 01 — Observability and guardrails: traces, logs, an alert, a floor setting that blocks a jailbreak

## Goal
Redeploy `ticket-agent` with OpenTelemetry to Cloud Trace on and content capture consciously off, read its logs with the resource filter, create the p99 latency alert, enable Data Access audit logs, then bind a Model Armor floor setting to the project and watch a jailbreak prompt go from answered (INSPECT_ONLY) to blocked (INSPECT_AND_BLOCK). Facts: map E4, E5, E6, F1, F2, F3, F8.

## Prerequisites
- G03 lab 02 done: `AGENT_RUNTIME_RESOURCE` in `.env` (form `projects/P/locations/L/reasoningEngines/ID`).
- G04 lab 03 done: `TICKET_MCP_URL` in `.env`.
- Shared venv active; `gcloud auth application-default print-access-token` works; `telemetry`, `cloudtrace`, `logging`, `monitoring` and Model Armor APIs enabled by `labs-setup/00-setup/scripts/enable_apis.sh`.

## Steps

### 1. Redeploy with tracing on, content off
`--otel_to_cloud` turns on OpenTelemetry export to Cloud Trace (E4). The deploy writes the requirements for you (C2); `.agent_engine_config.json` in this folder keeps `identity_type` as `AGENT_IDENTITY` (C5). Content capture stays off because neither `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` nor `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS` is set (E4).
```bash
set -a; source ../../../.env; set +a
ID=${AGENT_RUNTIME_RESOURCE##*/}
adk deploy agent_engine --project="$GOOGLE_CLOUD_PROJECT" --region="$GOOGLE_CLOUD_LOCATION" \
  --agent_engine_id="$ID" --display_name=ticket-agent --otel_to_cloud agent
```
Expected: the command ends by printing the same `reasoningEngines/<ID>` (C3).

### 2. Make three calls and open the trace
```bash
python jailbreak_probe.py --benign      # three ordinary ticket questions, prints the response text
```
Console: Agent Runtime → Deployments → `ticket-agent` → Traces tab (E4). Expected: one trace per call with spans for the agent, the model call and the `lookup_ticket` MCP tool; no prompt text inside span attributes.

### 3. Read the logs with the resource filter (E6)
```bash
gcloud logging read "resource.type=\"aiplatform.googleapis.com/ReasoningEngine\" AND resource.labels.reasoning_engine_id=\"$ID\" AND severity>=INFO" \
  --project="$GOOGLE_CLOUD_PROJECT" --limit=20 --format='value(logName,textPayload)'
```
Expected: lines from `reasoning_engine_stdout` that include the `before_tool_callback` message `tool=lookup_ticket args={...}` written by `agent/agent.py`, and `reasoning_engine_build` lines from step 1.

### 4. Create the p99 alert (E5)
The monitoring page's example threshold is p99 of `reasoning_engine/request_latencies` above 5000 ms. `alert_policy.json` is that policy; its JSON shape is standard Cloud Monitoring and is unverified against the map.
```bash
gcloud alpha monitoring policies create --policy-from-file=alert_policy.json --project="$GOOGLE_CLOUD_PROJECT"
```
Expected: a policy name `projects/P/alertPolicies/N`. Open Monitoring → Dashboards → "Agent Runtime Overview" and confirm `request_count` moved after step 2.

### 5. Turn on Data Access audit logs for `aiplatform.googleapis.com` (F8)
Console: IAM & Admin → Audit Logs → filter `Vertex AI API` → tick Data Read and Data Write. Then re-run step 2 and read:
```bash
gcloud logging read 'logName:"cloudaudit.googleapis.com%2Fdata_access" AND protoPayload.serviceName="aiplatform.googleapis.com"' \
  --project="$GOOGLE_CLOUD_PROJECT" --limit=5 --format='value(protoPayload.methodName,protoPayload.authenticationInfo.principalEmail)'
```
Expected: `Query` or `StreamQuery` method entries with your ADC principal. Needs `roles/logging.privateLogViewer` (F8).

### 6. Model Armor floor setting: INSPECT_ONLY, then INSPECT_AND_BLOCK (F2)
```bash
python jailbreak_probe.py --jailbreak                        # baseline: no floor setting yet
bash ../../sketches/model_armor_floor.sh INSPECT_ONLY
python jailbreak_probe.py --jailbreak                        # still answered; findings land in Cloud Logging
bash ../../sketches/model_armor_floor.sh INSPECT_AND_BLOCK
python jailbreak_probe.py --jailbreak                        # expected: the request is rejected before the model
python jailbreak_probe.py --benign                           # expected: still answered
```
Expected after `INSPECT_AND_BLOCK`: the jailbreak call returns an error or a blocked response rather than an answer, the benign calls still work. The exact error payload is unverified (the floor-settings reference page could not be fetched, map Gaps); record what you see in the checklist.

### 7. Gemini safety settings are separate (F3)
`agent/agent.py` sets `HARM_CATEGORY_DANGEROUS_CONTENT` to `BLOCK_MEDIUM_AND_ABOVE` explicitly, because the default on gemini-3.5-flash and later is `OFF` (F3). Remove the setting, redeploy, and nothing visible changes for the ticket prompts; the point is that you now know which layer did what.

## Proof checklist (tick with real output, not intent)
- [ ] step 1 prints `reasoningEngines/<ID>` for the existing agent (an update, not a second agent)
- [ ] step 2: a trace in the Traces tab with agent, model and `lookup_ticket` spans, and no prompt text in attributes
- [ ] step 3: a `reasoning_engine_stdout` line with `tool=lookup_ticket`
- [ ] step 4: alert policy name printed; `request_count` visible on "Agent Runtime Overview"
- [ ] step 5: a Data Access entry with `methodName` ending in `Query`
- [ ] step 6: jailbreak answered with no floor and under `INSPECT_ONLY`; rejected under `INSPECT_AND_BLOCK`; benign still answered
- [ ] step 6: `gcloud model-armor floorsettings describe` shows the platform integration and `INSPECT_AND_BLOCK`
- [ ] `pytest test_01_observability.py` runs the tests you wrote (not an empty collection)

## Cleanup
Leave the floor setting on for lab 02 (its jailbreak case depends on it). Delete the alert policy when the track is done: `gcloud alpha monitoring policies delete <name>`. The redeployed agent is the same resource G03 created; delete it at the end of the track as G03 lab 02 describes.

## Next
`../02-evals/`.
