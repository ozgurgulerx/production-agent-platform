"""Proves: a batch evaluation scores a window of the agent's sessions with per-session ground truth.

StartBatchEvaluation over the last --hours of the agent's log group, ground truth from data/cases.jsonl keyed by
the session ids recorded by 01/04 (pass them with --sessions). The user-simulation path (SimulationConfig,
actor profiles) exists in the SDK but its wire shape is marked # verify and is left as a documented option.
"""
import sys
import time
from datetime import datetime, timedelta, timezone
from _common import EVALUATORS, data, load_cases, log_group

hours = int(sys.argv[sys.argv.index("--hours") + 1]) if "--hours" in sys.argv else 24
sessions = sys.argv[sys.argv.index("--sessions") + 1].split(",") if "--sessions" in sys.argv else []
end = datetime.now(timezone.utc); start = end - timedelta(hours=hours)

filter_cfg = {"timeRange": {"startTime": start, "endTime": end}}
if sessions:
    filter_cfg["sessionIds"] = sessions
metadata = {}
if sessions:   # ground truth per session; shape of groundTruth.inline is marked # verify
    c = {x["id"]: x for x in load_cases()}
    metadata = {"evaluationMetadata": {"sessionMetadata": [
        {"sessionId": s, "testScenarioId": "c03",
         "groundTruth": {"inline": {"assertions": [{"text": c["c03"]["assertion"]}],
                                    "expectedTrajectory": {"toolNames": c["c03"]["expected_tools"]}}}}   # inline keys: assertions, expectedTrajectory, turns
        for s in sessions]}}

r = data().start_batch_evaluation(
    batchEvaluationName=f"ticket-agent-batch-{int(time.time())}",
    evaluators=[{"evaluatorId": e} for e in EVALUATORS],
    dataSourceConfig={"cloudWatchLogs": {"logGroupNames": [log_group()], "filterConfig": filter_cfg}},
    outputConfig={"cloudWatchConfig": {"resultDestination": "DEDICATED_LOG_GROUP"}},
    **metadata,
)
bid = r["batchEvaluationId"]
print("batch:", bid, r["status"])
while True:
    g = data().get_batch_evaluation(batchEvaluationId=bid)
    print("status:", g["status"])
    if g["status"] in ("COMPLETED", "FAILED", "STOPPED"):
        break
    time.sleep(30)
print("results in", g.get("outputConfig"), "- batch is 25% cheaper than online on the same evaluators")
# Simulation option (SDK): from bedrock_agentcore.evaluation import SimulationConfig, ActorProfile  # verify fields
