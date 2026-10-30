"""Untested sketch. Continuous evaluation = eval over live responses + a rule with a cap. Project MI needs Foundry User."""
from azure.ai.projects.models import ContinuousEvaluationRuleAction, EvaluationRule, EvaluationRuleEventType, EvaluationRuleFilter
ev = client.evals.create(name="live", data_source_config={"type": "azure_ai_source", "scenario": "responses"}, testing_criteria=[...])  # noqa: F821
project.evaluation_rules.create_or_update(id="ticket-continuous", evaluation_rule=EvaluationRule(  # noqa: F821
    action=ContinuousEvaluationRuleAction(eval_id=ev.id, max_hourly_runs=100),
    filter=EvaluationRuleFilter(agent_name="ticket-agent-prompt"),
    event_type=EvaluationRuleEventType.RESPONSE_COMPLETED, enabled=True))
