# 10 — Foundry IQ Grounding Proof

## Goal
Connect the IQ knowledge base to the agent and prove retrieval behavior in traces (including citations in the response).

## You will end with
- Agent configured with a knowledge retrieval tool (IQ/MCP-backed)
- A question that requires retrieval and yields citations/grounding output

## Prerequisites
- Completed `../01-seven-ways` (the prompt agent exists)
- Optional: `../../../F08-Evals-Tracing-and-Release/labs/01-observability` to see the grounding spans

## Proof (checklist)
- [ ] Response includes citations/grounding output
- [ ] Trace shows retrieval tool calls/spans
- [ ] Search/retrieval spans are visible and correlated to the run

## Next
Continue to F04: `../../../F06-Agent-Tooling-MCP-and-Integration/labs/02-mcp-tool`.
