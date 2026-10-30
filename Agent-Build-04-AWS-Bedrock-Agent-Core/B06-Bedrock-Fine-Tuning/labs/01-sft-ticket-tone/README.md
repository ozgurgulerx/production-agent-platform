# 01 — Fine-tune the ticket agent's tone on Nova 2 Lite, then prove it with the same eval

SFT on `amazon.nova-2-lite-v1:0` with about 60 reviewed rows generated from the three policy documents. The point is the last step: the tuned model is only promoted if the B05 Strands Evals experiment scores it at least as well as the base on the same cases.

## Prerequisites
- Shared setup done; `CODE_BUCKET` set (training data and job output live under `s3://$CODE_BUCKET/finetune/`).
- Region where Nova 2 Lite customisation is offered (`us-east-1` on 25 Oct 2026, reading map K3). Permissions: `bedrock:CreateModelCustomizationJob`, `bedrock:CreateCustomModelDeployment`, `iam:CreateRole`, `iam:PassRole`.
- `BEDROCK_FT_BASE_MODEL_ID` in `.env` (default `amazon.nova-2-lite-v1:0`).

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
python make_dataset.py           # Converse generates ~60 rows, prints every one, writes data/train.jsonl + data/valid.jsonl, uploads to S3
python customization_role.py     # role trusted by bedrock.amazonaws.com; writes FT_ROLE_ARN
python submit_sft.py             # create_model_customization_job; polls to Completed; writes FT_JOB_ARN, FT_CUSTOM_MODEL_ARN
python deploy_custom_model.py    # create_custom_model_deployment; polls to Active; writes FT_DEPLOYMENT_ARN
python compare_base_vs_tuned.py  # Strands Evals on the B05 cases: base vs tuned, side by side, promote/hold verdict
python deploy_custom_model.py --cleanup    # deletes the deployment and the custom model (storage is USD 1.95/model/month)
```

## What each script proves
- **make_dataset** the row shape is a Converse conversation (`schemaVersion bedrock-conversation-2024`); the data teaches how to *say* the refusal, never the cap itself.
- **customization_role** the job runs under a Bedrock-trusted role scoped to one S3 prefix, not under your SSO identity.
- **submit_sft** one call creates the job; hyperparameters are a string map; `validationMetrics` arrive with `Completed`.
- **deploy_custom_model** a custom model is not callable until it has a deployment (or Provisioned Throughput); the deployment ARN is the `modelId`.
- **compare_base_vs_tuned** the same agent, same tools, same cases, two `BedrockModel`s. Numbers decide.

## What to notice
- There is no DPO job to reach for. If you want "prefer this reply over that", write it into the judge rubric of the custom evaluator (B05 lab 02 `03_custom_judge.py`) or into an RFT grader.
- `issue_refund` still refuses 400 GBP in both runs. If the tuned model *sounds* more willing, that is exactly the failure the eval must catch (`ToolSelectionAccuracy`, the refusal assertion).

## Proof (checklist)
- [ ] `make_dataset.py` output read; `data/train.jsonl` ≥ 45 rows, `data/valid.jsonl` ≥ 8; no row invents an amount or softens the £250 rule
- [ ] `submit_sft.py` prints `Completed`, an `outputModelArn`, and training/validation loss
- [ ] `deploy_custom_model.py` prints `Active` and the deployment ARN
- [ ] `compare_base_vs_tuned.py` table pasted here with the verdict line
- [ ] deployment and custom model deleted after the comparison (or the decision to keep them recorded)

## Known gaps
RFT and distillation are sketched, not scripted (`../../sketches/nova_jsonl_shapes.py`, `rft_mantle_note.md`). Nova 2 Lite hyperparameter key names are marked `# verify`. Nothing here has run yet.
