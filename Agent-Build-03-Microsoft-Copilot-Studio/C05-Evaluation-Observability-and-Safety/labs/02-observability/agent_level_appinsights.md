# Agent-level App Insights (the older connection)

Reading map H3. Copilot Studio → the agent → **Settings** → **Advanced** → Application Insights connection string.

- Writes `customEvents`: topic and node execution, generative answers events, custom telemetry you add in topics; test pane traffic carries `designMode=True`.
- The "Copilot Studio Dashboard" workbook (preview) is built on these events.
- It does **not** write spans. If someone shows you a Copilot Studio "trace" from this connection, it is a sequence of events, not an OpenTelemetry trace.
- Both connections can point at the same App Insights resource; the environment export lands in `dependencies`, this one in `customEvents`, so the KQL never collides.

Quick check: `customEvents | where timestamp > ago(1h) | summarize count() by name`.
