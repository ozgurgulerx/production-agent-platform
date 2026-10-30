# F12 capability builds — Fine-tuning, LoRA and model improvement

## Build contract

Status: **planned; functionality unverified**. Build one capability at a time using the existing module and labs. Record environment/dependency versions, permitted assistance, positive and negative results, and trace/test evidence. The learner writes code and tests; these contracts do not supply hidden implementations. Verify dated API and availability claims before execution.

### Choose an improvement method

- [ ] Build: Start with prompt/RAG baseline and held-out evaluation. Compare SFT, distillation and adapters against the specific failure; state data rights, split, cost budget and success threshold.
- [ ] Verify: Demonstrate that evaluation data is excluded from training and show no-tune alternative; retain unsuccessful outcomes rather than declaring a win.

### Prepare and run a bounded training experiment

- [ ] Build: Create/version a minimal validated dataset, inspect format and safety, then submit a supported fine-tuning job only within an approved lab budget. Capture base model/version, configuration and training outputs.
- [ ] Verify: Test invalid examples and job failure/cancellation; preserve dataset provenance and estimated/actual cost. Treat the source ellipsis as unresolved scope, not completed training coverage.

### Serve LoRA and compare deployment

- [ ] Build: Verify compatible base weights, adapter format and serving/runtime support before deploying an adapter to managed compute. Document how adapter training produced the artifact and how it is versioned.
- [ ] Verify: Compare baseline/adapted model on the same holdout for quality, latency and cost; test incompatible adapter rejection and rollback to base/previous adapter. Model routing enforcement remains F09.

## Exact checklist targets

Each ID below is a distinct occurrence in the [full coverage matrix](../reference/production-build-coverage.md). Source wording is retained, including historical names and unfinished placeholders; it is not a fresh API guarantee. Compound items may require several small builds. Mark complete only after recording evidence.

- [ ] **CB020** — Serving fine-tuned LoRA adapters (preview) [link](https://learn.microsoft.com/en-us/azure/foundry/concepts/managed-compute-overview)
- [ ] **CB021** — Adapter deployment overview [link](https://learn.microsoft.com/en-us/azure/foundry/concepts/adapter-deployment-overview)
- [ ] **CB022** — ==Depoy fine-tuned LoRA adapters== [link](https://learn.microsoft.com/en-us/azure/foundry/how-to/deploy-lora-managed-compute) - how are they fine-tuned?
- [ ] **CB028** — fine-tuning [fine-tuning](https://learn.microsoft.com/en-us/azure/foundry/fine-tuning/overview)
- [ ] **CB029** — …
- [ ] **CB037** — When SFT beats prompting, Foundry fine-tuning options, cost, eval before/after, distillation workflow.

## Completion evidence

- [ ] Store the artifact path, reproducible command, observed outcome, limitations and next gap in the existing study log.
- [ ] Preserve current labs; link to shared concepts rather than importing another stage’s implementation.
- [ ] Do not label a sample, empty test collection or planned experiment as verified functionality.
