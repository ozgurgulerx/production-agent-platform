# 02 — See what the agent did: spans, transcripts, Monitor, Purview

Four views of the same conversation (chapter §6). The one that makes Copilot Studio comparable with Foundry and AgentCore is the **environment-level App Insights export** (preview, Sept 2026): OpenTelemetry GenAI spans named `InvokeAgent`, `ExecuteTool`, `OutputMessages` in the `dependencies` table (reading map H2). It needs a Managed Environment and a Power Platform admin.

## Prerequisites
`labs-setup/` done; an Application Insights resource (`APPINSIGHTS_CONNECTION_STRING` in `.env`); C03 lab 01 agent published and used at least once outside the test pane (the test pane is excluded from Monitor).

## Steps
1. `enable_env_telemetry.md`: turn on the environment-level export in the Power Platform admin centre.
2. `agent_level_appinsights.md`: also connect the agent-level connection string so you can see the difference (events, not spans).
3. Talk to the published agent in Teams or the demo website: a status question, a refund within policy, a refund above 250.
4. Run the three queries in `query_spans.kql` in App Insights → Logs; screenshot the `ExecuteTool` row for `issue_refund` with its arguments.
5. `python transcripts.py --hours 24` reads the same conversations from Dataverse and prints outcome and tool calls.
6. `monitor_page.md` and `purview_audit.md`: find the same conversation in Monitor and in the Purview audit log.

```bash
source ../../../labs-setup/.venv/bin/activate
python transcripts.py --hours 24
```

## Proof checklist
- [ ] App Insights `dependencies` shows `InvokeAgent` and `ExecuteTool` rows for the agent (environment-level export)
- [ ] Query 2 lists the refund attempts with amounts; the 400 GBP attempt shows no successful `issue_refund`
- [ ] `transcripts.py` prints at least one conversation with its `SessionInfo` outcome
- [ ] The same conversation is visible in Monitor → Conversational sessions and absent for a test-pane chat
- [ ] Purview audit search returns a `CopilotInteraction` record for it
