# 02 — Bedrock Guardrails inside a Cedar policy

One script. The gateway role gets `bedrock:InvokeGuardrailChecks`, two policies with `when guardrails {…}` clauses are created, and a refund whose reason carries a prompt-attack string is denied at the gateway. Compare with B05 lab 03 using `compare_with_model_guardrail.md`.

## Prerequisites
Lab 01 run to at least `05_enforce.py` (engine attached in ENFORCE). Region among the 7 with guardrails-in-policy (GA 17 Jun 2026). IAM: `iam:PutRolePolicy` on the gateway role.

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
python apply.py
python apply.py --cleanup
```

## Proof checklist
- [ ] both policies `ACTIVE` with no findings
- [ ] clean refund `ok`
- [ ] prompt-attack refund `DENIED` and the Lambda log shows no invocation for it
- [ ] PII refund `DENIED`
- [ ] comparison table filled in

## Unverified on 2026-10-25
The `when guardrails { … }` grammar, the `[output]` reference for response checks, the `suppressOutput` placement, and the exact IAM action name (`bedrock:InvokeGuardrailChecks` from the page; `ApplyGuardrail` added as a fallback).
