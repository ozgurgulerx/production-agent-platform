# Environment-level App Insights export (preview, Sept 2026)

Reading map H2. Managed Environments only; Power Platform admin.

1. Power Platform admin centre → **Manage** → **Environments** → the lab environment → **Settings** → **Product** → *Application Insights export* (the label may read "Agent telemetry"; verify in your tenant).
2. Paste the connection string of your App Insights resource (`APPINSIGHTS_CONNECTION_STRING`). Choose whether to include message content (`gen_ai.*` content attributes); for the lab include it, for production decide with the data owner.
3. Save. Spans arrive within minutes of the next conversation; the test pane is also exported, tagged as design mode.
4. In App Insights open **Agents (preview)**: Agent Runs, Tools, Models. Then Logs → `dependencies | where name in ("InvokeAgent","ExecuteTool","OutputMessages") | take 20`.

What you get: one `InvokeAgent` per turn, one `ExecuteTool` per tool call with `gen_ai.tool.name`, `gen_ai.tool.call.arguments`, `gen_ai.tool.call.result`, `gen_ai.request.model`, `gen_ai.conversation.id`; `OutputMessages` with the answer. Standard and GitHub Copilot harnesses; no topic-level events; GUID trace ids.
What you do not get: topic node events (those are agent-level, see `agent_level_appinsights.md`), and anything for agents in non-managed environments.
