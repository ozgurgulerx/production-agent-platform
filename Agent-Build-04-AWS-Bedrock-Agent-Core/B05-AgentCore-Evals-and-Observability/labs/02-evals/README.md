# 02 — AgentCore Evaluations for the agent you just built

Same twelve cases, three homes: the deployed agent's traces (on demand, online, batch), the Optimization loop, and a local Strands Evals experiment that needs no Runtime. Set `TICKET_AGENT_RUNTIME_ARN` (B03 lab 01) and `AGENTCORE_EVAL_ROLE_ARN` (a role with `logs:*` read on the agent's log group and write on `/aws/bedrock-agentcore/evaluations/*`; `# verify` minimum policy) in `.env`.

Evaluations is GA (31 Mar 2026). Batch and Optimization recommendations are GA (Jun 2026); Failure Insights is preview; `Builtin.FailureAnalysis` is from Oct 2026.

| Step | Script | What it proves |
|---|---|---|
| 1 | `01_on_demand_session_eval.py` | three turns in one session → `EvaluationClient.run` → six `Builtin.*` scores with explanations |
| 2 | `02_online_eval_config.py` | 10 % of live sessions scored continuously; dedicated results log group; `--cleanup` |
| 3 | `03_custom_judge.py` | `CreateEvaluator` LLM-as-a-judge "policy adherence" 0–1, run on the session from step 1 |
| 4 | `04_failure_analysis.py` | `Builtin.FailureAnalysis` names the root cause of a forced failure |
| 5 | `05_batch_with_simulation.py` | batch over a window with per-session ground truth; simulation left as a verified-shape TODO |
| 6 | `06_strands_evals_ci.py` | local `Experiment` with `ToolSelectionAccuracy`, `GoalSuccessRate`, `OutputEvaluator(rubric)`; non-zero exit under threshold |
| 7 | `07_recommendations.py` | Optimization rewrites the system prompt from traces; you decide |
| CI | `eval.yaml`, `.github-workflow-snippet.yml` | one dataset, two gates with the same evaluator names |

```bash
source ../../../labs-setup/.venv/bin/activate
python 01_on_demand_session_eval.py --wait 120
python 02_online_eval_config.py && python 02_online_eval_config.py --cleanup
python 03_custom_judge.py --session <id printed by 01>
python 06_strands_evals_ci.py --threshold 0.8 ; echo exit=$?
```

## Reading results
- `value` is the score (numerical scales) and `label` the category; `explanation` says why; `context.spanContext` points at the session/trace/span judged.
- TOOL_CALL evaluators return one result per tool span; TRACE ones per invocation; SESSION ones once.
- Online results land in `/aws/bedrock-agentcore/evaluations/results/<config-id>` as OTel GenAI evaluation events and as metrics in `Bedrock-AgentCore/Evaluations`; alarm on `Builtin.ToolParameterAccuracy` first.
- Pricing: built-ins $0.0024 / $0.012 per 1K judge in/out tokens; custom judge $1.50 per 1K evaluations plus model; batch 25 % off.

## Proof (checklist)
- [ ] step 1 prints six evaluator rows; `Builtin.Refusal` or `ToolParameterAccuracy` explains the T-1002 refusal
- [ ] step 2 config reaches `ACTIVE` with `executionStatus` healthy; after traffic, the Evaluations tab shows scores; `--cleanup` deletes it
- [ ] step 3 returns a `value` for `ticket-policy-adherence` on the step-1 session
- [ ] step 4 prints a FailureAnalysis root cause
- [ ] step 6 exits 0 at threshold 0.8 and prints the per-case table
- [ ] step 7 prints a recommended prompt and explanation (promotion optional, re-run step 6 first)

## Maps to
S05.01 (foundations), S05.02 (tool-use evals = `ToolSelectionAccuracy` / `ToolParameterAccuracy`, `expected_trajectory`), S05.04 (task evals = `GoalSuccessRate` with assertions, custom judge), S05.05 (eval ops = online config, batch, recommendations, CI gate).
