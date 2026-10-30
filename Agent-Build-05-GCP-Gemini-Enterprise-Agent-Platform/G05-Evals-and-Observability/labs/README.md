# G05 labs — observe, guard and measure the ticket agent

Runnable proofs for the G05 chapter. Setup is shared: [`../../labs-setup/`](../../labs-setup/) (activate `../../labs-setup/.venv`, `.env` at the track root). Both labs point at the agents G03 labs 01–03 created (`ticket-agent`, `ticket-agent-workflow`, `AGENT_RUNTIME_RESOURCE`) and at the ticketing MCP server from G04 lab 03 (`TICKET_MCP_URL`). Facts are cited by map letter from [`../../reference/reading-map-gcp-agents-2026-10-25.md`](../../reference/reading-map-gcp-agents-2026-10-25.md).

```
labs/
├── 01-observability/           redeploy with --otel_to_cloud, read traces, logs, create the p99 alert, Model Armor floor setting blocks a jailbreak
│   ├── agent/agent.py          ticket-agent with before_tool_callback logging and explicit Gemini safety settings
│   ├── .agent_engine_config.json
│   ├── alert_policy.json       p99 request_latencies > 5000 ms (shape unverified)
│   ├── jailbreak_probe.py      sends one jailbreak prompt before and after the floor setting
│   ├── test_01_observability.py
│   └── requirements.txt
└── 02-evals/                   six-case evalset, adk eval, AgentEvaluator under pytest, platform eval, two-model comparison
    ├── agent/agent.py          ticket-agent, model taken from EVAL_MODEL (default GEMINI_MODEL)
    ├── evalsets/ticket.evalset.json
    ├── test_config.json        criteria thresholds (E1 defaults)
    ├── eval_harness.py         run one evalset against N model ids, print one table; G06 reuses it for tuned vs base
    ├── platform_eval.py        client.evals.evaluate with adaptive rubrics on the harness output (shape, preview)
    ├── test_02_evals.py        pytest skeleton: AgentEvaluator.evaluate, the CI gate
    └── requirements.txt
```

| Lab | Chapter section | Creates | Time |
|---|---|---|---|
| 01 | §1 observability, §2 guardrails | a redeployed `ticket-agent` revision with tracing on, a log filter you have run, one alert policy, one Model Armor floor setting (INSPECT_ONLY then INSPECT_AND_BLOCK) | 60 min |
| 02 | §3 ADK evaluation, §4 platform evals, §5 CI gate | `ticket.evalset.json` (6 cases), `adk eval` report, pytest gate, platform eval report, `gemini-3.5-flash` vs `gemini-4-argon` table | 90 min |

Run order: 01 before 02, so the eval runs in lab 02 leave traces you can open, and so the floor setting is in place when the jailbreak case runs. Lab 02's harness is reused unchanged by [`../../G06-Fine-Tuning/labs/`](../../G06-Fine-Tuning/labs/) with `EVAL_MODELS` set to the tuned endpoint and the base.

```bash
cd Agent-Build-05-GCP-Gemini-Enterprise-Agent-Platform && source labs-setup/.venv/bin/activate
cd G05-Evals-and-Observability/labs/01-observability && cat README.md
```

Status on 25 Oct 2026: scaffold only, functionality unverified.

Next chapter: [`../../G06-Fine-Tuning/`](../../G06-Fine-Tuning/).
