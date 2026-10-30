# What a good trace looks like (tick list for the screenshot)

Open CloudWatch → GenAI Observability → Bedrock AgentCore → `ticket-agent` → Sessions → pick one → Trace.

- [ ] one root span per invocation named `invoke_agent ticket-agent` with `gen_ai.agent.name`
- [ ] a `chat` span per model call with `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`
- [ ] a `Tool: get_ticket` and a `Tool: issue_refund` span with `gen_ai.tool.name` and the tool input/output (unless `AWS_GENAI_CONTENT_EXTRACTION_OPT_OUT` is set)
- [ ] `session.id` equals the `runtimeSessionId` you passed to `invoke_agent_runtime`
- [ ] the caller's `traceparent` (if you set one) stitches your client span above the agent's root
- [ ] the Evaluations tab (after lab 02) shows the six evaluator scores on this session

If the Traces list is empty: Transaction Search off (lab step 1), the container not started with `opentelemetry-instrument`, or you are looking at the wrong endpoint's log group.
