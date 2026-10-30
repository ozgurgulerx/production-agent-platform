# Which door for which app (reading map C7–C10)

| Door | Carries the user | Harness | Use for |
|---|---|---|---|
| Direct-to-Engine (Agents SDK Copilot Studio client) | yes, via delegated `CopilotStudio.Copilots.Invoke` and OBO | Standard only (GitHub harness not yet supported) | services, bots on other channels, bridges between tenants |
| Direct Line (token endpoint) | optional, through manual auth / token exchange | Standard | custom web canvases, kiosks |
| Agents Client SDK (Android, iOS, Windows) | no (unauthenticated only) | Standard | consumer mobile surfaces without sign-in |
| Connected agent (lab 04) | yes | both | agent-to-agent, not app-to-agent |

Rule: if a human is signed in to your app, use Direct-to-Engine and OBO so the transcript, the tools and the security scan all see that human.
