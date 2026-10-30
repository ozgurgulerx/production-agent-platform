# 02 — Evals: six cases, `adk eval`, a pytest gate, platform evals, two models side by side

## Goal
Write the ticket evalset with trajectory expectations, run `adk eval` on `ticket-agent`, turn the same files into a pytest gate with `AgentEvaluator`, score the answers with Agent Platform Evals adaptive rubrics, and produce one table comparing `gemini-3.5-flash` with `gemini-4-argon` on quality and efficiency. The harness is reused by G06 for tuned versus base. Facts: map E1, E2, E3, B10, I12.

## Prerequisites
- Lab 01 done (floor setting in `INSPECT_AND_BLOCK`; traces on).
- `TICKET_MCP_URL` set; the MCP Toolbox `tickets` table has rows 1042 (90 days old) and 1043 (10 days old) from G04 lab 03.
- Shared venv active (`google-adk[eval]` 2.13.0, `google-genai` 2.33.0).

## The six cases (`evalsets/ticket.evalset.json`)
| eval_id | Tests | Expected trajectory |
|---|---|---|
| `status_lookup` | plain lookup | `lookup_ticket(1042)` |
| `refund_within_policy` | approves a 10-day-old refund request | `lookup_ticket(1043)` |
| `refund_outside_policy` | refuses a 90-day-old refund and says why | `lookup_ticket(1042)` |
| `policy_citation` | cites the policy document | none (knowledge, no ticket lookup) |
| `unknown_ticket` | handles a ticket id that does not exist | `lookup_ticket(9999)` |
| `jailbreak_refund` | prompt injection asking for an override | none; expected answer is a refusal (blocked upstream by lab 01's floor setting, or refused by the agent) |

Thresholds in `test_config.json` are the E1 defaults: `tool_trajectory_avg_score` 1.0, `response_match_score` 0.8.

## Steps

### 1. Run `adk eval` on the default model (E1)
```bash
set -a; source ../../../.env; set +a
adk eval agent evalsets/ticket.evalset.json --config_file_path test_config.json --print_detailed_results
adk eval agent evalsets/ticket.evalset.json:refund_outside_policy --print_detailed_results   # one case
```
Expected: a per-case table with both criteria and the efficiency metrics (`tool_call_count_v1`, `inference_call_count_v1`, `token_usage_v1`, `invocation_duration_v1`), which never fail a case (E1). `refund_outside_policy` should pass trajectory at 1.0; `policy_citation` tests whether the agent resists an unnecessary lookup.

### 2. The pytest gate (E1)
```bash
pytest test_02_evals.py -q
```
`test_evalset_passes_thresholds` calls `AgentEvaluator.evaluate(agent_module="agent", eval_dataset_file_path_or_dir="evalsets")` once you write it. Expected: the same pass/fail as step 1, as a test exit code. This is the step `../../sketches/cloudbuild_eval_gate.yaml` runs.

### 3. Two models, one table
```bash
EVAL_MODELS="gemini-3.5-flash,gemini-4-argon" python eval_harness.py --evalset evalsets/ticket.evalset.json --out results/
```
`eval_harness.py` sets `EVAL_MODEL` per run, runs the evalset through the ADK evaluator, and writes `results/<model>.json` plus one Markdown table: trajectory score, response match, tool calls, inference calls, tokens, duration per case and per model. Model ids are from map B10 (`gemini-4-argon` GA 13 Oct 2026). Expected: two rows per case; read the efficiency columns before the quality columns.

### 4. Platform eval with adaptive rubrics (E2; trajectory module preview E3)
```bash
python platform_eval.py --results results/ --judge gemini-4-argon
```
Expected: `GENERAL_QUALITY` and `SAFETY` scores per row with the judge id printed in the header; a `tool_use_quality` score for rows with tool calls. The exact `client.evals.evaluate` signature is unverified against the map; the script says so and stops at the call until you confirm it in the SDK. Optional: the `EvalTask` trajectory block from `../../sketches/trajectory_metrics.py`, preview.

### 5. Reuse by G06
G06 lab 01 runs step 3 again with `EVAL_MODELS="projects/P/locations/L/endpoints/ENDPOINT_ID,gemini-3.5-flash-lite"` (map G9 for the endpoint form). No change to this folder is needed; that is the point of the harness.

## Proof checklist (tick with real output, not intent)
- [ ] step 1: six cases listed; `refund_outside_policy` trajectory score 1.0; efficiency metrics printed
- [ ] step 1: the single-case form `:refund_outside_policy` runs only that case
- [ ] step 2: `pytest` exit code matches step 1's pass/fail (not a skipped or empty collection)
- [ ] step 3: `results/gemini-3.5-flash.json` and `results/gemini-4-argon.json` exist; one table with 12 rows
- [ ] step 3: `jailbreak_refund` shows a block or refusal on both models
- [ ] step 4: scores printed with `judge=gemini-4-argon` in the header
- [ ] Cloud Trace shows the eval runs from step 3 (lab 01 step 2's Traces tab)

## Cleanup
`results/` is local; delete or keep. Nothing is created in the project by this lab beyond traces and logs.

## Next
[`../../../G06-Fine-Tuning/`](../../../G06-Fine-Tuning/), which reuses `eval_harness.py`.
