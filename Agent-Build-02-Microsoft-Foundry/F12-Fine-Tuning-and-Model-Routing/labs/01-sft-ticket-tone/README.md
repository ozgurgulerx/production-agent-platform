# 01 — Fine-tune the ticket agent's tone, then prove it with the same eval

SFT on `gpt-4.1-mini` with ~60 reviewed rows generated from the F08 policy documents. The point is the last step: the tuned model is only promoted if F05 lab 02 scores it higher than the base on the same six rows.

## Prerequisites
- Shared setup; F08 lab 01's policy files exist (they are read from that folder; no need to have run the lab).
- A region and resource where `gpt-4.1-mini` is fine-tunable (overview table, 2026-10-19). Roles: Azure AI Developer / Foundry Project Manager on the project.
- Optional: `azd ext install azure.ai.finetune` for the YAML path.

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
python make_dataset.py        # writes data/*.jsonl and prints every row: read them, fix or delete bad ones
python submit_sft.py          # ~20–60 min on Developer training type
# deploy the printed fine_tuned_model with ../../../labs-setup/01-models (SKU_NAME=DeveloperTier bash deploy_models.sh after setting FOUNDRY_MODEL to the new name, or az ... deployment create)
# create ticket-agent-tuned on that deployment (F03 lab 01 02-prompt-agent-sdk.py with FOUNDRY_MODEL=<tuned>)
# F05 lab 02: EVAL_AGENT_NAME=ticket-agent-prompt python 01_batch_eval_agent_target.py ; EVAL_AGENT_NAME=ticket-agent-tuned python 01_batch_eval_agent_target.py
```

## What to notice
- The refund cap is never in the training data as a rule to learn; it is in the tool. The data teaches how to *say* the refusal.
- Developer training type and `DeveloperTier` deployment make the whole experiment cost training tokens only. The 24-hour deployment is the eval window.
- The two eval runs share the dataset and evaluators; the comparison is apples to apples. Promote on numbers, with the CI threshold from `eval.yaml`.

## Proof (checklist)
- [ ] `make_dataset.py` output reviewed; `data/train.jsonl` ≥ 45 rows, `validation.jsonl` ≥ 8
- [ ] `submit_sft.py` prints `succeeded` and a `fine_tuned_model` name
- [ ] two F05 `report_url`s, base and tuned, with the per-evaluator scores side by side in this README
- [ ] Developer deployment gone after 24 h (or deleted), no hosting fee incurred

## Known gaps
DPO and RFT variants not scripted (shapes in `../../sketches/three_jsonl_shapes.py`). Synthetic-data generator in the portal not used (Learn page 404). Nothing here has run yet.
