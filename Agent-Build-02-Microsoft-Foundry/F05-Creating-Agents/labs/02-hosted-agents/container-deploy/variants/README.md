# Other frameworks, same contract

Both variants are taken from `microsoft-foundry/foundry-samples` (main, 2026-10-23) and renamed. They prove that the hosted-agent contract is the Responses protocol on port 8088, not Agent Framework:

- `langgraph/` — LangGraph `create_agent` graph exported from `main.py`; the host is `langchain_azure_ai.agents.hosting.run --protocol responses` (see `entryPoint` in `azure.yaml`). Note its `pyproject.toml` pins `openai<3`, so it needs its own environment; use the azd remote build rather than the repo `.venv`.
- `openai-agents-sdk/` — OpenAI Agents SDK `Agent` + `Runner` behind the raw `azure.ai.agentserver.responses.ResponsesAgentServerHost` with a `@app.response_handler`. No Agent Framework at all.

Deploy either exactly like `code-deploy`: `cd <variant> && azd ai agent init -m ./azure.yaml && azd provision && azd deploy && azd ai agent invoke "hi"`.
Both use `uv`-style `pyproject.toml` from upstream; `azd` remote build resolves it. Upstream README and licence: https://github.com/microsoft-foundry/foundry-samples (MIT).
