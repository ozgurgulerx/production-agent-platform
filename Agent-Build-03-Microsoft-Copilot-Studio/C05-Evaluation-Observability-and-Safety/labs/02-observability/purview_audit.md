# Purview: the compliance view of the same conversation

Reading map F6, F7, H4.

- **Audit** (Purview → Audit → search): `CopilotInteraction` records carry prompts and responses; maker and admin events include `BotCreate`, `BotPublish`, `BotShare`, `BotAuthUpdate`. Search by the agent's app id or the user.
- **DSPM for AI**: transcripts by agent, risky-usage signals; Insider Risk "Risky AI usage" flags injection attempts (the C05 lab 03 XPIA test should appear here).
- **eDiscovery**: Copilot Studio messages are stored as `IPM.SkypeTeams.Message.Copilot.Studio.*` items; retention through the "Microsoft Copilot Experiences" policy location.
- **Non-Microsoft channels** (website, WhatsApp) need Purview pay-as-you-go for interaction capture.
- With **Agent 365** the agent also appears in the registry with observability auto-emitted (E8); Defender uses that stream (F14).

Proof: find the lab 02 refund conversation as a `CopilotInteraction` record and note the time lag versus App Insights.
