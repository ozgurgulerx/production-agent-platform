# F05 labs — observe and measure the ticket agents

Runnable proofs for the F05 chapter. Setup is shared: [`../../labs-setup/`](../../labs-setup/). These labs point at the agents from F03 labs 01–03; set `EVAL_AGENT_NAME` in the track-root `.env` to choose which.

```
labs/
├── 01-observability/   auto-instrumentation + manual spans into Application Insights (uses the shared venv)
└── 02-evals/           batch eval vs agent target, rubric generation, continuous rule, scheduled trace eval, red team, optimizer, CI gate
                        own .venv: azure-ai-projects 2.9.0 (agent-framework-foundry pins <2.8)
```

| Lab | Chapter section | Needs beyond the shared setup |
|---|---|---|
| 01 | §5 Insights and traces | Application Insights connected to the project |
| 02 | §1–§4 objects, evaluators, batch, continuous and scheduled; §6 optimizer; §7 red team; §8 CI | its own venv; project MI holds Foundry User for continuous rules |

Order: 01 first so lab 02's scheduled trace eval has traces to read.

```bash
cd 02-evals && python3.13 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python 01_batch_eval_agent_target.py
```
