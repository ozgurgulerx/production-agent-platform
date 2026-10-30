# B05 labs — see the traces, score them, guard the runtime

Runnable proofs for the B05 chapter. Setup is shared: do [`../../labs-setup/`](../../labs-setup/) first (venv, `.env` at the track root, `verify.sh` printing OK) and have B03 lab 01 done so `TICKET_AGENT_RUNTIME_ARN` exists. Each lab README ends with a **proof checklist**; a lab is done when the boxes are ticked with real output.

```
labs/
├── 01-observability/   Transaction Search once, a locally traced Strands agent, spans read back from the agent's log group
├── 02-evals/           on-demand session eval, online config, custom judge, failure analysis, batch, Strands Evals CI gate, recommendations
└── 03-guardrails/      a Bedrock guardrail on the model, ApplyGuardrail on tool output, the same rule as Cedar for B09
```

| Lab | Chapter section | Creates | Time |
|---|---|---|---|
| 01 | §7 | Transaction Search setting, nothing billable beyond CloudWatch | 30 min |
| 02 | §2–§6, §9 | online config (delete with `--cleanup`), one custom evaluator | 1 session |
| 03 | §8 | one guardrail + version | 30 min |

Run them in order. Region must be one where Evaluations is available (us-east-1, us-west-2, Frankfurt, Ireland, Tokyo, Sydney, Singapore, Mumbai, Ohio).

```bash
source ../../labs-setup/.venv/bin/activate
cd 01-observability && python enable_transaction_search.py
```

Nothing here has run against AWS yet (no account at build time, 25 Oct 2026). Next chapter: [`../../B09-AgentCore-Policy-and-Governance/labs/`](../../B09-AgentCore-Policy-and-Governance/labs/).
