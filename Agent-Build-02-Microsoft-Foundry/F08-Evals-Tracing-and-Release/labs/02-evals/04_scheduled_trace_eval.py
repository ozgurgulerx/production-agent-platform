"""F05 step 4 — Scheduled evaluation over traces (preview): every day at 09:00 score the last
24 h of this agent's traces from Application Insights. Run: python 04_scheduled_trace_eval.py [--delete]
"""
import sys

from azure.ai.projects.models import DailyRecurrenceSchedule, EvaluationScheduleTask, RecurrenceTrigger, Schedule

from _common import AGENT_NAME, EVAL_MODEL, project_client

project = project_client(allow_preview=True)
client = project.get_openai_client()
SCHEDULE_ID = f"{AGENT_NAME}-daily-trace-eval"
if "--delete" in sys.argv:
    project.beta.schedules.delete(schedule_id=SCHEDULE_ID); print("deleted", SCHEDULE_ID); raise SystemExit

ev = client.evals.create(
    name=f"{AGENT_NAME}-traces",
    data_source_config={"type": "azure_ai_source", "scenario": "traces"},
    testing_criteria=[{"type": "azure_ai_evaluator", "name": "tool_call_accuracy", "evaluator_name": "builtin.tool_call_accuracy",
                       "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}", "tool_definitions": "{{item.tool_definitions}}"},
                       "initialization_parameters": {"deployment_name": EVAL_MODEL}}],
)
schedule = project.beta.schedules.create_or_update(
    schedule_id=SCHEDULE_ID,
    schedule=Schedule(
        display_name=f"Daily trace eval {AGENT_NAME}",
        enabled=True,
        trigger=RecurrenceTrigger(interval=1, schedule=DailyRecurrenceSchedule(hours=[9]), time_zone="Europe/London"),
        task=EvaluationScheduleTask(
            eval_id=ev.id,
            eval_run={"name": "daily", "data_source": {"type": "azure_ai_trace_data_source_preview",
                       "agent_filter": {"agent_name": AGENT_NAME}, "lookback_hours": 24}},
        ),
    ),
)
print("schedule", schedule.schedule_id, schedule.provisioning_status)
