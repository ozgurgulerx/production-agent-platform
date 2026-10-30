# The three end-user authentication modes (reading map E5)

| Mode | Who the agent knows | Where SSO works | Tools with end-user credentials | DLP handle |
|---|---|---|---|---|
| No authentication | nobody | n/a | cannot run | virtual connector "Chat without Microsoft Entra ID authentication" |
| Authenticate with Microsoft (default) | the Entra user | Teams, SharePoint, Power Apps, M365 Copilot | run as the user; no `User.AccessToken` variable exposed | channel connectors |
| Authenticate manually | the user from your IdP | any channel, incl. custom web | run as the user; `User.AccessToken` available for your own calls | admin can lock manual auth tenant-wide |

Manual providers: Microsoft Entra ID v2 with federated credentials (recommended), certificate, or client secret; Microsoft Entra ID; Generic OAuth 2 with a token-exchange URL so a website session becomes an agent sign-in.

## Try it
1. Settings → Security → Authentication → No authentication → Save. The refund tool, which uses end-user credentials, is now greyed; the test pane says the tool requires authentication.
2. Switch back to Authenticate with Microsoft. In Teams the user is signed in silently; on the demo website a sign-in card appears.
3. Optional: Authenticate manually with Entra ID v2 and a federated credential; note that no secret is stored.

Record: which tools stopped working under "No authentication", and the exact wording of the test-pane message.
