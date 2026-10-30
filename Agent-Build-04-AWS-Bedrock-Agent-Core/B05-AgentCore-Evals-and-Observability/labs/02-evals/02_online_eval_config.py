"""Proves: an online evaluation config samples 10% of the agent's live sessions and scores them continuously.

Creates the config on the agent's log group with six built-ins and a dedicated results log group.
--cleanup deletes it. ACTIVE means configured; scores appear only after sessions close (sessionTimeoutMinutes).
"""
import sys
from bedrock_agentcore.evaluation import EvaluationClient
from _common import EVALUATORS, EVAL_ROLE_ARN, REGION, control, log_group, write_env

NAME = "ticket-agent-online"
client = EvaluationClient(region_name=REGION)

if "--cleanup" in sys.argv:
    for c in control().list_online_evaluation_configs().get("onlineEvaluationConfigs", []):   # verify list key
        if c.get("onlineEvaluationConfigName") == NAME:
            client.delete_online_evaluation_config_and_wait(onlineEvaluationConfigId=c["onlineEvaluationConfigId"])
            print("deleted", c["onlineEvaluationConfigId"])
    sys.exit(0)

if not EVAL_ROLE_ARN:
    sys.exit("set AGENTCORE_EVAL_ROLE_ARN (logs read on source group, write on results group) in .env")
pct = float(sys.argv[sys.argv.index("--sample") + 1]) if "--sample" in sys.argv else 10.0
cfg = client.create_online_evaluation_config_and_wait(
    onlineEvaluationConfigName=NAME,
    description="B05 lab 02: six built-ins on sampled live sessions",
    rule={"samplingConfig": {"samplingPercentage": pct}, "sessionConfig": {"sessionTimeoutMinutes": 15}},
    dataSourceConfig={"cloudWatchLogs": {"logGroupNames": [log_group()]}},
    evaluators=[{"evaluatorId": e} for e in EVALUATORS],
    outputConfig={"cloudWatchConfig": {"resultDestination": "DEDICATED_LOG_GROUP"}},
    evaluationExecutionRoleArn=EVAL_ROLE_ARN,
    enableOnCreate=True,
)
print("status:", cfg.get("status"), "executionStatus:", cfg.get("executionStatus"))
print("results ->", cfg.get("outputConfig"))
write_env("ONLINE_EVAL_CONFIG_ID", cfg["onlineEvaluationConfigId"])
print("now generate traffic (B03 lab 01 04-invoke-everything.py) and watch CloudWatch -> GenAI Observability -> agent -> Evaluations")
