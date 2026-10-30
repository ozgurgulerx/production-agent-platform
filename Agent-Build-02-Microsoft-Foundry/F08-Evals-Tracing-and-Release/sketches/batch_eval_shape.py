"""Untested sketch. Eval = what; run = on what, against whom. Runnable: ../labs/02-evals/01_batch_eval_agent_target.py."""
client = project.get_openai_client()   # noqa: F821  (project: AIProjectClient on azure-ai-projects>=2.8)
ev = client.evals.create(name="ticket-batch",
    data_source_config={"type": "custom", "item_schema": {"type": "object", "properties": {"query": {"type": "string"}}}, "include_sample_schema": True},
    testing_criteria=[{"type": "azure_ai_evaluator", "name": "task_adherence", "evaluator_name": "builtin.task_adherence",
                       "data_mapping": {"query": "{{item.query}}", "response": "{{sample.output_items}}"},   # items, not text: tool calls matter
                       "initialization_parameters": {"deployment_name": "gpt-5-mini"}}])
run = client.evals.runs.create(eval_id=ev.id, data_source={"type": "azure_ai_target_completions",
    "source": {"type": "file_id", "id": "<dataset id>"},
    "input_messages": {"type": "template", "template": [{"type": "message", "role": "user", "content": {"type": "input_text", "text": "{{item.query}}"}}]},
    "target": {"type": "azure_ai_agent", "name": "ticket-agent-prompt", "version": "2"}})
