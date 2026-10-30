"""F05 step 2 — Let Foundry write the rubric for THIS agent, then use it as a criterion.

`evaluators.begin_create_generation_job` reads the agent's instructions/tools and produces a
weighted multi-dimension rubric (1–5 per dimension, normalised 0–1). You review it, version it,
and reference it like any builtin.* evaluator. Run: python 02_rubric_generation.py
"""
from azure.ai.projects.models import AgentEvaluatorGenerationJobSource, EvaluatorGenerationInputs

from _common import AGENT_NAME, EVAL_MODEL, agent_version, project_client

project = project_client()
version = agent_version(project)
poller = project.evaluators.begin_create_generation_job(
    job=EvaluatorGenerationInputs(
        sources=[AgentEvaluatorGenerationJobSource(agent_name=AGENT_NAME, agent_version=version,
                                                  description="UK bank card-team support-ticket assistant; must not invent processes")],
        model=EVAL_MODEL,
        evaluator_name=f"{AGENT_NAME}-rubric",
        evaluator_display_name=f"Rubric for {AGENT_NAME}",
    )
)
job = poller.result()
print("job", job.id, job.status)
if job.input_quality_warnings:
    print("warnings:", job.input_quality_warnings)
result = job.result
print("evaluator:", getattr(result, "name", None), "version", getattr(result, "version", None))
dims = getattr(getattr(result, "definition", None), "dimensions", None) or []
for d in dims:
    print(f"  [{d.weight}] {d.id}: {d.description}")
print("\nUse it in 01_batch_eval_agent_target.py criteria as:")
print(f'  {{"type":"azure_ai_evaluator","name":"rubric","evaluator_name":"{getattr(result, "name", AGENT_NAME + "-rubric")}", "data_mapping": {{"query":"{{{{item.query}}}}","response":"{{{{sample.output_items}}}}"}}}}')
