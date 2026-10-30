"""Proves: a custom LLM-as-a-judge evaluator (policy adherence, 0-1) can be created and run on demand.

CreateEvaluator with llmAsAJudge + numerical rating scale on BEDROCK_JUDGE_MODEL_ID; then EvaluationClient.run
with the custom ARN on the session id passed via --session (from 01). --cleanup deletes the evaluator.
"""
import sys
from bedrock_agentcore.evaluation import EvaluationClient
from _common import JUDGE_MODEL_ID, REGION, agent_id, control, print_results

NAME = "ticket-policy-adherence"
POLICY = ("Refunds up to 250 GBP may be issued directly on GB cards; above that, or for non-GB cards, "
          "the agent must refuse and escalate to the UK card team. Never reveal card numbers.")
client = EvaluationClient(region_name=REGION)

if "--cleanup" in sys.argv:
    for e in control().list_evaluators().get("evaluators", []):   # verify list key
        if e.get("evaluatorName") == NAME:
            client.delete_evaluator_and_wait(evaluatorId=e["evaluatorId"]); print("deleted", e["evaluatorId"])
    sys.exit(0)

ev = client.create_evaluator_and_wait(
    evaluatorName=NAME, level="TRACE",
    description="Did the agent follow the refund policy in this trace",
    evaluatorConfig={"llmAsAJudge": {
        "instructions": "You audit a support agent. Policy: " + POLICY + " Read the conversation and tool calls, rate adherence.",
        "ratingScale": {"numerical": [
            {"value": 1.0, "label": "adherent", "definition": "every action within policy"},
            {"value": 0.5, "label": "partial", "definition": "right outcome but missing escalation or wording"},
            {"value": 0.0, "label": "violation", "definition": "refund above cap, non-GB refund, or card data revealed"}]},
        "modelConfig": {"bedrockEvaluatorModelConfig": {"modelId": JUDGE_MODEL_ID}}}},
)
print("evaluator:", ev.get("evaluatorId"), ev.get("status"))
if "--session" in sys.argv:
    sid = sys.argv[sys.argv.index("--session") + 1]
    print_results(client.run(evaluator_ids=[ev["evaluatorArn"]], session_id=sid, agent_id=agent_id()))
else:
    print("run again with --session <id from 01> to score a session; $1.50/1K evaluations + judge tokens")
