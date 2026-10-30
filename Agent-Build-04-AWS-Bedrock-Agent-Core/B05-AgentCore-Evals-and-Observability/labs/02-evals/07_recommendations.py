"""Proves: Optimization recommends a rewritten system prompt from real traces (GA Jun 2026, no extra charge).

StartRecommendation(type=SYSTEM_PROMPT_RECOMMENDATION) with the current prompt and the agent's log group over
the last --hours, scored by the six built-ins; polls GetRecommendation and prints the recommended prompt and
explanation. Never promote blindly: re-run 06 against the new prompt first. # verify: logGroupArns vs names.
"""
import sys
import time
from datetime import datetime, timedelta, timezone
from _common import EVALUATORS, REGION, agent_id, data, session

PROMPT = "You are the UK support-ticket assistant. Use the tools. Never refund above policy."
hours = int(sys.argv[sys.argv.index("--hours") + 1]) if "--hours" in sys.argv else 24
acct = session().client("sts").get_caller_identity()["Account"]
lg_arn = f"arn:aws:logs:{REGION}:{acct}:log-group:/aws/bedrock-agentcore/runtimes/{agent_id()}-DEFAULT"
end = datetime.now(timezone.utc)
r = data().start_recommendation(
    name=f"ticket-prompt-rec-{int(time.time())}", type="SYSTEM_PROMPT_RECOMMENDATION",
    recommendationConfig={"systemPromptRecommendationConfig": {
        "systemPrompt": {"text": PROMPT},
        "agentTraces": {"cloudwatchLogs": {"logGroupArns": [lg_arn], "startTime": end - timedelta(hours=hours), "endTime": end}},
        "evaluationConfig": {"evaluators": [{"evaluatorArn": e} for e in EVALUATORS]}}},   # verify: ARN vs Builtin id
)
rid = r["recommendationId"]; print("recommendation:", rid, r["status"])
while True:
    g = data().get_recommendation(recommendationId=rid)
    if g["status"] in ("COMPLETED", "FAILED"):
        break
    print("status:", g["status"]); time.sleep(30)
res = g.get("recommendationResult", {}).get("systemPromptRecommendationResult", {})
print("\nRECOMMENDED PROMPT:\n", res.get("recommendedSystemPrompt"), "\n\nWHY:\n", res.get("explanation"), res.get("errorMessage", ""))
