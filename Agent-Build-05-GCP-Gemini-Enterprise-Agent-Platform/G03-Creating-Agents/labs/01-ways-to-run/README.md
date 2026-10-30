# 01 — Run the same agent four ways before any cloud resource exists

One agent, `ticket-agent`, defined once in `ticket_agent/agent.py` as `root_agent`, run from the `Runner` in code, from `adk run`, from `adk web`, from `adk api_server`, and then on Cloud Run with `adk deploy cloud_run`. The point is not the agent. The point is to see that the definition never moves and that none of these four ways produces a `ReasoningEngine` resource, which is what lab 02 adds.

| #   | Way                  | Definition lives        | Loop runs          | Resource          | Status          | Map |
| --- | -------------------- | ----------------------- | ------------------ | ----------------- | --------------- | --- |
| 1   | `Runner` in code     | `ticket_agent/agent.py` | your process       | none              | GA (ADK 2.13.0) | B5  |
| 2   | `adk run`, `adk web` | same                    | your process       | none              | GA              | B6  |
| 3   | `adk api_server`     | same                    | your process, REST | none              | GA              | B6  |
| 4   | Cloud Run            | same, in your container | Cloud Run          | Cloud Run service | GA              | B7  |

Decision rule to carry: _no resource needed → Runner, `adk run` or `adk web`; a URL for other services → `adk api_server` locally, Cloud Run in the cloud; revisions, identity, registration, Sessions, Memory Bank → Agent Runtime (lab 02)._

## Prerequisites

[`../../../labs-setup/`](../../../labs-setup/) done: shared venv, `.env` at the track root with `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, `GOOGLE_GENAI_USE_VERTEXAI=TRUE`, `GEMINI_MODEL`; ADC in place. Way 4 needs the Cloud Run API enabled (`enable_apis.sh` does it) and `roles/run.admin`.

## Files

```
01-ways-to-run/
├── ticket_agent/
│   ├── __init__.py          `from . import agent`
│   └── agent.py             root_agent: LlmAgent, two function tools, refusal rule, policy citations (TODO(learner))
├── run_local.py             way 1: Runner + InMemorySessionService, two turns, prints events
├── requirements.txt         pins copied from labs-setup/requirements.txt
└── test_01_ways_to_run.py   pytest skeletons, TODO(learner)
```

`agent.py` ships with two local stand-in tools (`get_ticket`, `check_refund_policy`) so the lab runs before the ticketing MCP server exists. G04 lab 02 swaps them for `McpToolset` pointed at `TICKET_MCP_URL`.

## Run

```bash
source ../../../labs-setup/.venv/bin/activate
cd 01-ways-to-run
python run_local.py                                       # way 1
adk run ticket_agent --save_session                       # way 2, terminal; saves the session for --replay later (B6)
adk web --port 8000                                       # way 2, dev UI; pick "ticket_agent" in the app list
adk api_server --with_ui                                  # way 3; REST on :8000
curl -s localhost:8000/list-apps                          # TODO(learner): confirm the route list on the running server; names unverified
adk deploy cloud_run --project "$GOOGLE_CLOUD_PROJECT" --region "$GOOGLE_CLOUD_LOCATION" \
  --service_name ticket-agent --app_name ticket-agent --with_ui ticket_agent    # way 4 (B6, B7)
```

Alternative for way 4, from the same page (B7): a `main.py` calling `get_fast_api_app(...)`, a `python:3.13-slim` Dockerfile with `uvicorn main:app`, and `gcloud run deploy --source .`. Not scaffolded here; `adk deploy cloud_run` is enough for the proof.

## Expected output

- `run_local.py`: turn 1 prints the agent asking for or using a ticket number; turn 2 (a refund request outside policy) prints a refusal that names the policy document. Events show a `function_call` for `get_ticket`.
- `adk web`: the same two turns in the UI, with the Events tab showing the tool call.
- `adk api_server`: the server lists `ticket_agent` as an app and answers a session request.
- `adk deploy cloud_run`: gcloud prints a `https://ticket-agent-....run.app` URL; the dev UI at that URL answers the same two turns.

## What each step proves

- **way 1** the `Runner` is the loop; `auto_create_session=True` removes the create_session call (B5).
- **way 2** `adk web` is a UI over the same Runner; `--save_session` writes a replayable session (B6).
- **way 3** the REST contract exists locally; it is what Agent Runtime runs on 8080 (C2).
- **way 4** Cloud Run is the self-host path: a URL, no `ReasoningEngine` resource, no entry for Gemini Enterprise (C8).

## Proof (checklist)

- [ ] `run_local.py` prints two turns; turn 2 refuses the out-of-policy refund and cites a policy document
- [ ] `adk run ticket_agent --save_session` saves a session file you can name
- [ ] `adk web` shows `ticket_agent` and the tool call in the Events tab
- [ ] `adk api_server` answers a request from `curl` or the bundled UI
- [ ] `adk deploy cloud_run` prints a run.app URL and the UI there answers turn 1
- [ ] `pytest test_01_ways_to_run.py` runs the tests you wrote (empty collection is "scaffold only", not a pass)

## Cleanup

```bash
gcloud run services delete ticket-agent --region "$GOOGLE_CLOUD_LOCATION" --quiet
```

## Next

`../02-agent-runtime/`: ways 5, 6 and 9, and `AGENT_RUNTIME_RESOURCE`.
