# Purview for Copilot Studio agents (F6, F7, F8)

- **Audit**: maker and admin events `BotCreate`, `BotPublish`, `BotShare`, `BotAuthUpdate`; user turns as `CopilotInteraction`. `purview_audit.py` pulls both for the last day. Transcript text is not in the audit record.
- **DSPM for AI**: the only place transcripts are readable for compliance; shows prompts, responses and tool calls per agent; Agent 365-registered agents appear here with sensitivity label handling (an agent instance needs VIEW and EXTRACT rights on labelled content, F8).
- **Retention**: policy location "Microsoft Copilot Experiences"; a 0-day retention policy drops the text and keeps the event. Dataverse `ConversationTranscript` has its own 30-day default (G4) and is a separate store.
- **Insider Risk Management**: "Risky AI usage" detects prompt injection attempts against the agent.
- **eDiscovery**: items of type `IPM.SkypeTeams.Message.Copilot.Studio.*`; non-Microsoft channels (web chat, WhatsApp) need Purview pay-as-you-go to be captured.
- **Communication Compliance** and **Compliance Manager AI assessments** apply to Agent 365-registered agents.

Do: Purview portal → Audit → search operations `BotPublish`, `CopilotInteraction` for the last day; DSPM for AI → Agents → ticket agent → open one interaction and find the `issue_refund` tool call; Data lifecycle → create a retention policy on "Microsoft Copilot Experiences" for the lab (revert: delete it).
