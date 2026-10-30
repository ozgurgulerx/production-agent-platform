# 01 — Observability: enable, emit, read

Three scripts, in order. The first is the account-level switch that every AgentCore evaluation silently depends on. The second shows what Strands emits, locally, so you recognise the span tree before you look for it in CloudWatch. The third reads the deployed agent's spans back from its log group.

| Step | Script | What it proves |
|---|---|---|
| 1 | `enable_transaction_search.py` | X-Ray destination → CloudWatch Logs; indexing rule at 1 % (free). Idempotent. |
| 2 | `local_traced_agent.py` | Strands `StrandsTelemetry` console exporter: `invoke_agent → cycle → chat → Tool:*` with `gen_ai.*` attributes; `--otlp` sends the same spans wherever `OTEL_EXPORTER_OTLP_*` points |
| 3 | `read_spans.py` | the deployed ticket agent's spans in `/aws/bedrock-agentcore/runtimes/<id>-DEFAULT` |

```bash
source ../../../labs-setup/.venv/bin/activate
python enable_transaction_search.py              # or: aws xray update-trace-segment-destination --destination CloudWatchLogs
python local_traced_agent.py                     # console spans
python read_spans.py --minutes 60                # after invoking the B03 agent once
```

## On Runtime
The container from B03 lab 02 starts with `opentelemetry-instrument python main.py` and `aws-opentelemetry-distro>=0.18.0` installed; Runtime injects the rest. Outside Runtime (Lambda, ECS) set, per the chapter §7: `AGENT_OBSERVABILITY_ENABLED=true`, `OTEL_PYTHON_DISTRO=aws_distro`, `OTEL_PYTHON_CONFIGURATOR=aws_configurator`, `OTEL_RESOURCE_ATTRIBUTES=service.name=ticket-agent-lambda,aws.log.group.names=/aws/bedrock-agentcore/runtimes/ticket-agent-lambda`, `OTEL_EXPORTER_OTLP_LOGS_HEADERS=x-aws-log-group=...,x-aws-metric-namespace=bedrock-agentcore`.

## Proof (checklist)
- [ ] step 1 prints `destination: CloudWatchLogs`
- [ ] step 2 prints a `Tool: issue_refund` span whose output contains `REFUSED` (T-1002 is £400)
- [ ] step 3 lists ≥ 1 span with `gen_ai.agent.name` for the deployed agent
- [ ] screenshot per `README-observability-proof.md` saved as `proof-trace.png`

Cost: CloudWatch ingestion only; 1 % indexing is free.
