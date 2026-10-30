# 01 — Tune the ticket agent's tone, then prove it with the same eval

SFT on `gemini-3.5-flash-lite` with 100 reviewed rows that teach how the agent _says_ a refund refusal and a status answer. The point is the last step: the tuned endpoint is only promoted if `adk eval` scores it higher than the base on the G05 lab 02 evalset.

Status on 25 Oct 2026: scaffold only, functionality unverified.

## Goal

A tuned endpoint path, a `ticket-agent-tuned` agent that uses it, and two eval reports side by side.

## Prerequisites

- Shared setup done ([`../../../labs-setup/`](../../../labs-setup/)); ADC; `.env` at the track root.
- Add to `.env`: `TUNING_LOCATION=eu` (Gemini 3.x tunes and serves on `us`/`eu` only, map G2) and `TUNING_BUCKET=gs://<bucket>`. Whether the bucket must itself be in the EU multi-region for an `eu` job is unverified; create it there to be safe.
- G05 lab 02 evalset path exported as `EVALSET` (the `*.evalset.json` that lab writes, map E1) and its criteria file as `EVAL_CONFIG`.
- Quota "Global concurrent tuning jobs" above zero in the project (map G2).

## Steps

```bash
cd Agent-Build-05-GCP-Gemini-Enterprise-Agent-Platform/G06-Fine-Tuning/labs/01-sft-ticket-tone
source ../../../labs-setup/.venv/bin/activate
python make_dataset.py                       # writes data/train.jsonl (85) and data/validation.jsonl (15); prints every row
python submit_sft.py                         # gcloud storage cp, client.tunings.tune on eu, polls, prints the endpoint
export TUNED_ENDPOINT="projects/.../locations/eu/endpoints/..."   # from the last line above; also put it in .env
export GOOGLE_GENAI_USE_ENTERPRISE=TRUE      # map G9; .env already sets GOOGLE_GENAI_USE_VERTEXAI=TRUE, which one ADK 2.13 reads is unverified
adk eval ../../../G03-Creating-Agents/labs/01-ways-to-run/ticket-agent "$EVALSET" --config_file_path "$EVAL_CONFIG" --print_detailed_results
adk eval . "$EVALSET" --config_file_path "$EVAL_CONFIG" --print_detailed_results     # this folder is ticket-agent-tuned
pytest -q                                    # collects the skeleton; reports "scaffold only" until you write the tests
```

`adk eval <AGENT_DIR> <EVALSET> --config_file_path --print_detailed_results` is the form on adk.dev (map E1). Rubric criteria need the platform evals (ADC plus project) (E1); `response_match_score` and `tool_trajectory_avg_score` do not.

## Expected output

- `make_dataset.py`: 100 numbered rows on stdout, two files in `data/`.
- `submit_sft.py`: a job name, a state line every minute, then `tuned endpoint: projects/P/locations/eu/endpoints/ID`.
- Two `adk eval` tables with the same case ids and different scores.

## What to notice

- The £250 rule is never in the training data as a rule to learn; it is in the instruction and in the ticketing MCP tool. The data teaches how to say the refusal.
- The agent code in `agent.py` is the G03 agent with one line changed (map G9).
- Training tokens equal dataset tokens times epochs (map G2); the pricing snippet "$0.003 / 1,000 count" for 3.5 Flash Lite SFT is unverified (map G8).

## Proof (checklist)

- [ ] `make_dataset.py` output reviewed row by row; `data/train.jsonl` has 85 lines, `data/validation.jsonl` 15, every `model` turn states the £250 rule the agreed way
- [ ] `submit_sft.py` prints a succeeded state and a `tuned endpoint:` line
- [ ] `TUNED_ENDPOINT` in `.env`; `adk run .` answers "Refund 300 GBP on ticket 1042" with a refusal in the new tone
- [ ] two `adk eval` result tables, base and tuned, pasted below with per-criterion scores
- [ ] decision written in one line: promoted or not, and on which number

## Cleanup

Delete the tuned endpoint and model from the console (Agent Studio, Tuning) or the SDK when the comparison is recorded; remove `data/*.jsonl` from the bucket with `gcloud storage rm`. Exact delete call for a tuned model in `google-genai` 2.33.0 unverified.

## Known gaps

Hyperparameter keyword spellings in `CreateTuningJobConfig` and the polling call are marked `TODO(learner)` to confirm against the installed SDK. Tool-call rows (shape 3 in the sketch) not generated here. Nothing here has run yet.

## Results

_(paste the two eval tables here)_
