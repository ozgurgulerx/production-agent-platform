# 06 — A2A: `ticket-agent` delegates to `ticket-agent-workflow`

## Goal
Serve `ticket-agent-workflow` (G03 lab 03) over A2A with `to_a2a`, read its card at `/.well-known/agent-card.json`, consume it from `ticket-agent` as a `RemoteA2aAgent` in `sub_agents`, and see one delegated turn (map C7). Then note what changes for Gemini Enterprise, which registers by pasted card and speaks A2A v0.3 streaming (map C9). A2A in ADK is **experimental** (map C7, undated page); say so in any design that uses it.

## Steps
```bash
source ../../../labs-setup/.venv/bin/activate
set -a; source ../../../.env; set +a
pip show google-adk | grep -i version          # 2.13.0 with the a2a extra (labs-setup requirements)

# 1. Expose the workflow agent locally. to_a2a serves the card and the JSON-RPC endpoint on 8001 (map C7).
python serve_workflow_a2a.py &                 # uvicorn app from to_a2a(root_agent, port=8001)
curl -s http://localhost:8001/.well-known/agent-card.json | python -m json.tool | head -30

# 2. Consume. ticket_agent/agent.py has RemoteA2aAgent(name="ticket_workflow", agent_card="http://localhost:8001/.well-known/agent-card.json") in sub_agents.
adk web --port 8000      # from this lab folder; pick ticket_agent; "Triage ticket 1003 and tell me if a refund is in policy"
# Events: a transfer to ticket_workflow, then the remote agent's answer

# 3. Remote on Agent Runtime instead of localhost. The Agent Runtime container already runs api_server --a2a (map C2);
#    multi-agent via A2A on Agent Runtime is the one explicitly preview-labelled feature on its page (map A5).
#    Point agent_card at the deployed workflow agent's card URL and redeploy ticket-agent with the lab 01 config
#    (identity_type AGENT_IDENTITY); the principal needs roles/agentregistry.viewer and roles/aiplatform.user (map C5, lab 01 step 4).
adk deploy agent_engine ticket_agent --project "$GOOGLE_CLOUD_PROJECT" --region "$GOOGLE_CLOUD_LOCATION" \
  --display_name ticket-agent --agent_engine_id "${AGENT_RUNTIME_RESOURCE##*/}" --agent_engine_config_file .agent_engine_config.json

# 4. Gemini Enterprise path (optional, needs discoveryengine.agentspaceAdmin, map C9): app → Agents → Add agent →
#    "Custom agent via A2A" → paste the card. Runtime-hosted A2A agents need an authorization with cloud-platform scope.
#    Gemini Enterprise speaks v0.3 streaming; for a 1.0 agent use a2a.compat.v0_3 (map C9).
```

## What to write
- `serve_workflow_a2a.py`: import the G03 workflow agent (or the stand-in in `workflow_agent.py`) and call `to_a2a(root_agent, port=8001)`; run with uvicorn.
- `ticket_agent/agent.py`: the `RemoteA2aAgent` entry and the instruction that tells `ticket-agent` when to transfer.
- `test_06_a2a.py`: the served card has the skills from `../../sketches/a2a_card.json`; a fake remote returns a result the root agent relays.

## Expected output
Step 1 prints a card with `name`, `url`, `skills` and `capabilities.streaming`. Step 2 shows a transfer event to `ticket_workflow` followed by text that cites the policy. If the card loads but calls fail with a version error, the server and client disagree on a2a-sdk 0.3 vs 1.x; 1.x is recommended on both ends, `use_legacy=True` is the 0.3 switch on `RemoteA2aAgent` (map C7).

## Proof checklist
- [ ] `curl .../.well-known/agent-card.json` returns the card with at least `triage_ticket`
- [ ] `adk web` Events show a transfer to `ticket_workflow` and its reply in one turn
- [ ] the remote card URL, not localhost, is used in the Agent Runtime redeploy and the delegated turn still works
- [ ] the agent principal holds `roles/agentregistry.viewer` and `roles/aiplatform.user` (lab 01)
- [ ] design note written: "A2A in ADK experimental (adk.dev, undated); Gemini Enterprise registration speaks 0.3 streaming (C9, 22 Oct 2026)"

## Cleanup
Stop the local server. Leave both Agent Runtime deploys for G05; delete them with `delete(force=True)` at the end of the track.

## Next
[`../../../G05-Evals-and-Observability/labs/`](../../../G05-Evals-and-Observability/labs/) — traces of these tool calls and the refund-policy eval.
