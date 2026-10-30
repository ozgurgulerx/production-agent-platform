"""Proves: one session of the deployed ticket agent gets six Builtin.* scores with explanations.

Drives three dataset cases through one runtimeSessionId, waits for spans to land, then calls
EvaluationClient.run which resolves each evaluator's level (SESSION/TRACE/TOOL_CALL) and batches Evaluate.
"""
import sys
import time
from bedrock_agentcore.evaluation import EvaluationClient
from _common import EVALUATORS, REGION, agent_id, invoke, load_cases, new_session_id, print_results

cases = [c for c in load_cases() if c["id"] in ("c01", "c02", "c03")]
sid = new_session_id()
print("session:", sid)
for c in cases:
    print(f"\n> {c['input']}\n< {invoke(c['input'], sid)[:200]}")

wait = int(sys.argv[sys.argv.index("--wait") + 1]) if "--wait" in sys.argv else 120
print(f"\nwaiting {wait}s for spans to reach CloudWatch ...")
time.sleep(wait)

client = EvaluationClient(region_name=REGION)
results = client.run(evaluator_ids=EVALUATORS, session_id=sid, agent_id=agent_id())
print(f"\n{len(results)} results")
print_results(results)
print("\nexpect: ToolParameterAccuracy / Refusal explain that T-1002 (400 GBP) was refused under the 250 cap")
