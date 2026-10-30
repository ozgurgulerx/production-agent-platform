# F13 capability builds — Local and edge runtime

## Build contract

Status: **planned; functionality unverified**. Build one capability at a time using the existing module and labs. Record environment/dependency versions, permitted assistance, positive and negative results, and trace/test evidence. The learner writes code and tests; these contracts do not supply hidden implementations. Verify dated API and availability claims before execution.

### Bounded local model exercise

- [ ] Build: Run a supported local model with a recorded runtime/version/hardware profile. Compare offline/privacy, memory and latency constraints with the cloud task.
- [ ] Verify: Test offline execution, unavailable model and insufficient-resource failure. Do not equate local execution with an enterprise security boundary.

### Deployment decision

- [ ] Build: Explain when local/on-prem/edge is appropriate and what capabilities cannot match the cloud path. Preserve C28 awareness priority while allowing one bounded build.
- [ ] Verify: Produce measured resource/latency evidence and a decision note; link the original local lab without replacing it.

## Exact checklist targets

Each ID below is a distinct occurrence in the [full coverage matrix](../reference/production-build-coverage.md). Source wording is retained, including historical names and unfinished placeholders; it is not a fresh API guarantee. Compound items may require several small builds. Mark complete only after recording evidence.


- [ ] **TOP-LOCAL** — C28 local and edge: Foundry Local and small models; on-prem/offline decision and awareness baseline.

## Completion evidence

- [ ] Store the artifact path, reproducible command, observed outcome, limitations and next gap in the existing study log.
- [ ] Preserve current labs; link to shared concepts rather than importing another stage’s implementation.
- [ ] Do not label a sample, empty test collection or planned experiment as verified functionality.
