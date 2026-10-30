# Channels and end-user auth for the ticket agent (L1, L2, E5)

| Channel | Switch on | What you see | Credits |
|---|---|---|---|
| Demo website | Channels → Demo website → copy link | a hosted test page outside the maker pane | per answer (K6) |
| Teams + Microsoft 365 Copilot | Channels → Teams and Microsoft 365 Copilot → Add; "Make available to others" | the agent in the Teams app store for you; tenant catalogue needs admin approval (L4) | per answer; free for M365 Copilot-licensed users in B2E |
| Custom website | Channels → Custom website → embed snippet | iframe on your page | |
| Mobile app (Direct Line) | Channels → Mobile app → Token endpoint | the endpoint `invoke_directline.py` uses (C10) | |
| Direct-to-Engine | no portal switch; delegated `CopilotStudio.Copilots.Invoke` on the Power Platform API (C8) | `invoke_direct_to_engine.py` | |
| WhatsApp, SharePoint, Facebook, Azure Bot channels, telephony | per channel | blocked per channel by DLP virtual connectors (F1) | |

End-user authentication (Settings → Security → Authentication):
- **Authenticate with Microsoft** (default): SSO in Teams, SharePoint, Power Apps, M365 Copilot; tools run as the user.
- **No authentication**: anyone with the link; tools set to end-user credentials are unavailable; the security scan flags it (E6).
- **Authenticate manually**: Entra ID v2 (federated credentials, certificate or secret), Entra ID, generic OAuth 2; needed for manual SSO on a custom website.

Publish semantics: one publish, every channel; new content reaches new sessions (~30 min inactivity or "start over"). Versions live in solutions (C3).
