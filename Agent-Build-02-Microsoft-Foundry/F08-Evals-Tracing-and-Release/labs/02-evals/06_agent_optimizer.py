"""F05 step 6 — Agent optimizer (preview) on the prompt agent: Foundry searches instruction/model
candidates, scores each with the evaluation set, and you promote the winner as a new version.
Costs real runs (it invokes the agent per row per candidate). Run: python 06_agent_optimizer.py
"""
from azure.ai.projects.models import (
    AgentOptimizationCandidateSearchConfiguration,
    AgentOptimizationEvaluationConfiguration,
    AgentOptimizationEvaluator,
    AgentOptimizationFoundryAgentTargetConfiguration,
    AgentOptimizationJob,
    AgentOptimizationModelConfiguration,
    AgentOptimizationTargetCompletionEvaluationSet,
    AgentOptimizationTargetCompletionInlineDataSource,
    AgentOptimizationTargetCompletionTestCase,
    PromptOptimizationConfiguration,
)

from _common import AGENT_NAME, DATASET, EVAL_MODEL, agent_version, project_client
import json

project = project_client(allow_preview=True)
rows = [json.loads(l) for l in DATASET.read_text().splitlines() if l.strip()]
test_cases = [AgentOptimizationTargetCompletionTestCase(query=r["query"], ground_truth=r.get("ground_truth")) for r in rows]
eval_set = AgentOptimizationTargetCompletionEvaluationSet(source=AgentOptimizationTargetCompletionInlineDataSource(test_cases=test_cases))

job = AgentOptimizationJob(
    display_name=f"optimize {AGENT_NAME}",
    target_configuration=AgentOptimizationFoundryAgentTargetConfiguration(name=AGENT_NAME, version=agent_version(project)),
    optimization_model_configuration=AgentOptimizationModelConfiguration(model=EVAL_MODEL),
    optimization_configuration=PromptOptimizationConfiguration(
        goal="Answer card-support questions accurately, never invent processes, keep replies under 60 words.",
        evaluation_configuration=AgentOptimizationEvaluationConfiguration(
            training_set=eval_set,
            evaluators=[AgentOptimizationEvaluator(name="builtin.task_adherence"), AgentOptimizationEvaluator(name="builtin.similarity")],
            evaluation_model=EVAL_MODEL,
        ),
        candidate_search_configuration=AgentOptimizationCandidateSearchConfiguration(max_candidates=4),
    ),
)
estimate = project.agents.estimate_optimization_job(job)   # cost before you spend it
print("estimate:", getattr(estimate, "cost", estimate))
poller = project.agents.begin_create_optimization_job(job)
result = poller.result()
print("job", result.id, result.status)
summary = result.result.candidate_summary if result.result else None
if summary:
    print(f"baseline {summary.baseline_score:.3f} -> best {summary.best_score:.3f} (candidate {summary.best_id})")
    if summary.best_score and summary.baseline_score and summary.best_score - summary.baseline_score > 0.03:   # <0.03 is noise per docs
        promoted = project.agents.promote_optimization_candidate(job_id=result.id, candidate_id=summary.best_id)
        print("promoted as new version:", promoted.promotion)
