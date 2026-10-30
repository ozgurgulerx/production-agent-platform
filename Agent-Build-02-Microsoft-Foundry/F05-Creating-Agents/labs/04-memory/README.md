# 04 — Memory (preview)

---
## 2026-10 refresh
All invocation now goes through `client.get_openai_client(agent_name=...)` + `responses.create(...)`; the `extra_body={"agent": ...}` spelling, `client.agents.invoke` and `--pre` installs are gone. Use the repo `.venv` (`azure-ai-projects` 2.7). See `../README.md` for the full list of retired APIs.
