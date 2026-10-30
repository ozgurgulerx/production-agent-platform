"""F05 step 3 — Continuous evaluation: sample live responses of an agent and score them.

A rule binds an eval (what to measure) to an agent (filter) on an event (response completed),
with an hourly cap. The project's managed identity needs Foundry User. Results land in the
Monitor dashboard and Application Insights. Run: python 03_continuous_evaluation_rule.py [--delete]
"""
import sys

from azure.ai.projects.models import (
    ContinuousEvaluationRuleAction,
    EvaluationRule,
    EvaluationRuleEventType,
    EvaluationRuleFilter,
)

from _common import AGENT_NAME, EVAL_MODEL, project_client

project = project_client()
client = project.get_openai_client()
RULE_ID = f"{AGENT_NAME}-continuous"

if "--delete" in sys.argv:
    project.evaluation_rules.delete(id=RULE_ID); print("deleted rule", RULE_ID); raise SystemExit

ev = client.evals.create(
    name=f"{AGENT_NAME}-live",
    data_source_config={"type": "azure_ai_source", "scenario": "responses"},     # live traffic, not a dataset
    testing_criteria=[
        {"type": "azure_ai_evaluator", "name": "intent_resolution", "evaluator_name": "builtin.intent_resolution",
         "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"}, "initialization_parameters": {"deployment_name": EVAL_MODEL}},
        {"type": "azure_ai_evaluator", "name": "task_adherence", "evaluator_name": "builtin.task_adherence",
         "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"}, "initialization_parameters": {"deployment_name": EVAL_MODEL}},
    ],
)
rule = project.evaluation_rules.create_or_update(
    id=RULE_ID,
    evaluation_rule=EvaluationRule(
        display_name=f"Continuous eval for {AGENT_NAME}",
        action=ContinuousEvaluationRuleAction(eval_id=ev.id, max_hourly_runs=100),
        filter=EvaluationRuleFilter(agent_name=AGENT_NAME),
        event_type=EvaluationRuleEventType.RESPONSE_COMPLETED,
        enabled=True,
    ),
)
print("rule", rule.id, "enabled", rule.enabled, "-> eval", ev.id)
print("Now generate traffic (F03 labs/01-seven-ways/06-invoke-everything.py) and open the Monitor tab; delete with --delete.")
