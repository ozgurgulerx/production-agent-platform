# 12 — Multi-agent as one hosted agent

Three agents (triage → specialist → responder) built with Agent Framework `WorkflowBuilder`, wrapped with `.as_agent()`, and served by `ResponsesHostServer`. To a caller it is one agent named `ticket-agent-workflow` with one Responses endpoint, one identity, one version history, one trace tree. That is the multi-agent pattern Foundry recommends today.

What this replaces: the 2025 version deployed a **Foundry declarative workflow** (YAML, `InvokeAzureAgent`) plus two separately hosted agents. Foundry retires declarative workflows on **1 Dec 2026**; the YAML is kept under `appendix-foundry-workflow-retiring-2026-12-01/` for the migration story. **Connected Agents** from the classic API do not exist in the new service either; its replacements are this (in-process workflow) and **A2A** across trust boundaries (F04, lab 12).

## Run
```bash
source ../.venv/bin/activate
cd 03-multi-agent-workflow && python run_local.py                                  # in-process: prints the customer reply
azd ai agent init -m ./azure.yaml --deploy-mode code && azd provision && azd deploy
azd ai agent invoke "My card was charged twice for order 8841, £42.10 each."
cd ../01-seven-ways && AGENT_NAMES=ticket-agent-workflow python 06-invoke-everything.py
```

## What to notice
- `AgentExecutor(agent, context_mode="last_agent")` is what keeps each step's context small; without it every agent sees the whole transcript.
- `output_executors=[responder]` limits the Responses output to the final text; otherwise every intermediate message streams out.
- The workflow is deployed exactly like lab 02's code path: same `azure.yaml` shape, same `create_version_from_code` behind `azd deploy`. Multi-agent did not need a new deployment primitive.
- Checkpoints (`FileCheckpointStorage`, `CosmosCheckpointStorage`) make long workflows resumable; `run_local.py` shows where they plug in. Human-in-the-loop uses `RequestInfoExecutor`; the upstream `05-workflows` and `23-resilient-workflow` samples go further.
- Orchestrations other than sequential (`ConcurrentBuilder`, handoff, group chat, Magentic) are the same `WorkflowBuilder` graph with different edges.

## Proof (checklist)
- [ ] `run_local.py` prints a reply signed "Card Services" that states the refund and the 5-working-day timeline
- [ ] `azd deploy` produces `ticket-agent-workflow` v1 active; `azd ai agent invoke` returns the same style of reply
- [ ] portal trace for one call shows three nested agent spans under one response
- [ ] `06-invoke-everything.py` passes all four controls against `ticket-agent-workflow`

## Next
`../../../F08-Evals-Tracing-and-Release/labs/02-evals/` (F05) to evaluate the prompt agent, the hosted agent and this workflow with the same dataset.
