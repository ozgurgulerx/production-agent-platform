"""F05 step 1 — Batch-evaluate a Foundry agent against a dataset, in the cloud.

The eval API is the OpenAI-compatible `evals` surface on the project's OpenAI client:
  evals.create  = WHAT to measure (testing criteria = Foundry evaluators, `builtin.*`)
  evals.runs.create = ON WHAT (a dataset) and AGAINST WHOM (an `azure_ai_agent` target: name+version)
Foundry runs the agent for every row, then the evaluators. Works for prompt agents and
responses-protocol hosted agents (02, 12) alike. Run: python 01_batch_eval_agent_target.py
"""
import time

from _common import AGENT_NAME, DATASET, EVAL_MODEL, agent_version, project_client

project = project_client()
version = agent_version(project)
client = project.get_openai_client()

# 1. dataset as a versioned project asset
dataset = project.datasets.upload_file(name="ticket-queries", version=str(int(time.time())), file_path=str(DATASET))
print("dataset", dataset.name, dataset.version, dataset.id)

# 2. eval definition: data schema + criteria. {{item.*}} = dataset columns, {{sample.*}} = the agent's output.
#    sample.output_text is the text; sample.output_items is the full item list incl. tool calls.
criteria = [
    {"type": "azure_ai_evaluator", "name": "task_adherence", "evaluator_name": "builtin.task_adherence",
     "data_mapping": {"query": "{{item.query}}", "response": "{{sample.output_items}}"},
     "initialization_parameters": {"deployment_name": EVAL_MODEL}},
    {"type": "azure_ai_evaluator", "name": "intent_resolution", "evaluator_name": "builtin.intent_resolution",
     "data_mapping": {"query": "{{item.query}}", "response": "{{sample.output_text}}"},
     "initialization_parameters": {"deployment_name": EVAL_MODEL}},
    {"type": "azure_ai_evaluator", "name": "groundedness_vs_truth", "evaluator_name": "builtin.similarity",
     "data_mapping": {"query": "{{item.query}}", "response": "{{sample.output_text}}", "ground_truth": "{{item.ground_truth}}"},
     "initialization_parameters": {"deployment_name": EVAL_MODEL}},
    {"type": "azure_ai_evaluator", "name": "violence", "evaluator_name": "builtin.violence",
     "data_mapping": {"query": "{{item.query}}", "response": "{{sample.output_text}}"}},
]
ev = client.evals.create(
    name=f"{AGENT_NAME}-batch",
    data_source_config={"type": "custom", "item_schema": {"type": "object", "properties": {"query": {"type": "string"}, "ground_truth": {"type": "string"}}, "required": ["query"]}, "include_sample_schema": True},
    testing_criteria=criteria,
)
print("eval", ev.id)

# 3. run it against the agent target
run = client.evals.runs.create(
    eval_id=ev.id,
    name=f"{AGENT_NAME}:{version}",
    data_source={
        "type": "azure_ai_target_completions",
        "source": {"type": "file_id", "id": dataset.id},
        "input_messages": {"type": "template", "template": [{"type": "message", "role": "user", "content": {"type": "input_text", "text": "{{item.query}}"}}]},
        "target": {"type": "azure_ai_agent", "name": AGENT_NAME, "version": version},
    },
)
print("run", run.id, run.status)
while run.status in ("queued", "in_progress"):
    time.sleep(10)
    run = client.evals.runs.retrieve(run_id=run.id, eval_id=ev.id)
    print("  ", run.status)
print("report:", run.report_url)
print("result counts:", run.result_counts)
for c in run.per_testing_criteria_results or []:
    print(f"  {c.testing_criteria}: passed={c.passed} failed={c.failed}")
