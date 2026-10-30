# Watch the delegation

1. Test pane or Teams: "What is the SLA for P1 tickets?" The Ticket Agent has no SLA knowledge; the activity trace shows **Connected agent: ticket-sdk-agent** and the reply text from `app.py`.
2. "Refund 400 GBP on T-2041": both agents refuse; note which one answered in the trace (the orchestrator may answer from instructions without delegating).
3. Monitor → Sessions: the delegation shows as a tool/agent call inside one session; credits count as agent actions (K6).
4. App Insights (C05 lab 02): the environment-level export shows an `ExecuteTool` span for the connected agent (H2).
