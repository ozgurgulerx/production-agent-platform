"""Proves: the agent's spans are in its own CloudWatch log group and carry gen_ai.* attributes.

Reads the last N minutes of the per-agent log group (/aws/bedrock-agentcore/runtimes/<id>-DEFAULT) and prints
span name, trace id, session id and the gen_ai.* attributes. Needs B03 lab 01 (TICKET_AGENT_RUNTIME_ARN) and at
least one invocation after Transaction Search was enabled.
"""
import json
import sys
import time
from _common import RUNTIME_ARN, runtime_log_group, session

if not RUNTIME_ARN:
    sys.exit("set TICKET_AGENT_RUNTIME_ARN in .env (B03 lab 01) first")
minutes = int(sys.argv[sys.argv.index("--minutes") + 1]) if "--minutes" in sys.argv else 30
logs = session().client("logs")
group = runtime_log_group()
print("log group:", group)
start = int((time.time() - minutes * 60) * 1000)
seen = 0
paginator = logs.get_paginator("filter_log_events")
for page in paginator.paginate(logGroupName=group, startTime=start, filterPattern="gen_ai"):   # verify stream name 'spans'
    for ev in page.get("events", []):
        try:
            span = json.loads(ev["message"])
        except json.JSONDecodeError:
            continue
        attrs = span.get("attributes", {})
        gen = {k: v for k, v in attrs.items() if k.startswith("gen_ai.")}
        print(f"{span.get('name','?'):40s} trace={span.get('traceId','?')[:16]} session={attrs.get('session.id','-')} {gen}")
        seen += 1
print(f"\n{seen} spans in the last {minutes} min. Console: CloudWatch -> GenAI Observability -> Bedrock AgentCore -> agent -> Traces")
