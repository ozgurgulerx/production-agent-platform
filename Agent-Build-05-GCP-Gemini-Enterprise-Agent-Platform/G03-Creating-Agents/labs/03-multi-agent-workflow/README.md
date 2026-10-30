# 03 — Multi-agent as one resource: `ticket-agent-workflow`

Three agents (triage → lookup → reply) composed with ADK's `SequentialAgent`, exported as a single `root_agent`, and deployed with exactly the lab 02 command. To a caller it is one `ReasoningEngine` named `ticket-agent-workflow`, with one Agent Identity, one revision history, one trace tree, one Gemini Enterprise entry. That is the multi-agent pattern this track recommends inside one trust boundary (B2, C2). Across boundaries it is A2A, in G04 lab 06 (C7).

State moves between steps with `output_key` on one agent and `{placeholder}` in the next agent's instruction (B2). The `LoopAgent` and `ParallelAgent` variants and a custom `BaseAgent` router are in [`../../sketches/workflow_agents.py`](../../sketches/workflow_agents.py); the Loop and Parallel detail pages were not fetched on 25 Oct 2026, so only the Sequential shape is scaffolded here. ADK 2.0 adds graph workflows that supersede the template agents (B2, A8); their API is on no fetched page and is not used.

## Prerequisites

Lab 02 done (`AGENT_RUNTIME_RESOURCE` exists, so the deploy roles and bucket are known to work).

## Files

```
03-multi-agent-workflow/
├── ticket_agent_workflow/
│   ├── __init__.py
│   └── agent.py                  triage, lookup, reply; root_agent = SequentialAgent(...)
├── .agent_engine_config.json     display_name ticket-agent-workflow, identity_type AGENT_IDENTITY
├── run_local.py                  Runner over the SequentialAgent; prints each sub-agent's output_key
├── requirements.txt
└── test_03_multi_agent_workflow.py
```

## Run

```bash
source ../../../labs-setup/.venv/bin/activate
cd 03-multi-agent-workflow
python run_local.py                                               # in-process: three steps, one reply
adk web --port 8000                                               # Events tab shows triage, lookup, reply as nested agents
adk deploy agent_engine --project "$GOOGLE_CLOUD_PROJECT" --region "$GOOGLE_CLOUD_LOCATION" \
  --display_name ticket-agent-workflow --otel_to_cloud ticket_agent_workflow        # same command as lab 02 (C2)
# Then with the printed reasoningEngines/ID:
AGENT_RUNTIME_RESOURCE=projects/$GOOGLE_CLOUD_PROJECT/locations/$GOOGLE_CLOUD_LOCATION/reasoningEngines/<ID> \
  python ../02-agent-runtime/query.py "My card was charged twice for order 8841. Ticket 1042."
```

Do not overwrite `AGENT_RUNTIME_RESOURCE` in `.env`; that stays `ticket-agent`. Note the workflow's id in the proof below.

## Expected output

- `run_local.py` prints `category=card`, a `facts` block, then the customer reply; the reply refuses the goodwill refund and cites the policy document.
- `adk web` Events tab shows three agent spans under one invocation.
- `adk deploy agent_engine` prints a second `reasoningEngines/<ID>`; `gcloud ai reasoning-engines list` shows `ticket-agent` and `ticket-agent-workflow`.

## What to notice

- Multi-agent needed no new deployment primitive: the folder has a `root_agent`, so `adk deploy agent_engine` treats it like any other (C2).
- Each sub-agent writes one `output_key`; the next instruction reads it as `{category}` or `{facts}` (B2). Nothing else is shared.
- One resource means one `spec.effectiveIdentity` (C5), one revision history (C4) and one registration (C8). Three resources would mean three of each plus A2A between them (C7, experimental).
- Multi-agent over A2A is the only explicitly preview-labelled Agent Runtime feature on 25 Oct 2026 (A5).

## Proof (checklist)

- [ ] `run_local.py` prints the three step outputs and a final reply that cites the policy document
- [ ] `adk web` shows triage, lookup and reply as nested agent events in one invocation
- [ ] `adk deploy agent_engine` prints a `reasoningEngines/<ID>` for `ticket-agent-workflow`
- [ ] `query.py` against that id returns the same style of reply as `run_local.py`
- [ ] `gcloud ai reasoning-engines describe` for the workflow shows one `spec.effectiveIdentity`
- [ ] `pytest test_03_multi_agent_workflow.py` runs the tests you wrote

## Cleanup

Keep `ticket-agent-workflow`: G05 evaluates it next to `ticket-agent`. A throwaway copy goes with `delete(force=True)` (C1).

## Next

`../04-memory-bank/` (optional) or [`../../../G04-Agent-Tooling-Identity-MCP-A2A/labs/`](../../../G04-Agent-Tooling-Identity-MCP-A2A/labs/) for the MCP ticket tools and A2A.
