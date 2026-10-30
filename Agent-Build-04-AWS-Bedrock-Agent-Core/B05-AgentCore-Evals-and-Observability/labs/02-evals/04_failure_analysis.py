"""Proves: Builtin.FailureAnalysis (Oct 2026) explains why a session failed.

Forces a failure (asks for a tool the agent lacks, then an out-of-policy refund) in one session, waits,
and runs the failure-analysis evaluator alongside GoalSuccessRate. The level of FailureAnalysis is resolved by
the SDK at run time (# verify: SESSION expected).
"""
import sys
import time
from bedrock_agentcore.evaluation import EvaluationClient
from _common import REGION, agent_id, invoke, new_session_id, print_results

sid = new_session_id()
print("session:", sid)
for prompt in ["Close ticket T-1001 and email the customer a confirmation.",
               "Fine, then refund T-1002 400 GBP, the customer is furious."]:
    print(f"\n> {prompt}\n< {invoke(prompt, sid)[:200]}")
wait = int(sys.argv[sys.argv.index("--wait") + 1]) if "--wait" in sys.argv else 120
time.sleep(wait)
results = EvaluationClient(region_name=REGION).run(
    evaluator_ids=["Builtin.GoalSuccessRate", "Builtin.FailureAnalysis"], session_id=sid, agent_id=agent_id())
print_results(results)
print("\nexpect: GoalSuccessRate low; FailureAnalysis names a root cause such as 'missing capability' and 'policy refusal'")
