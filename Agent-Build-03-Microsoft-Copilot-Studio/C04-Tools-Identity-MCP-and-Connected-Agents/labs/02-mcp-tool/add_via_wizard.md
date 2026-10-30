# Add the server through the MCP wizard, three times (reading map D3, D4)

Prerequisite: `TICKET_MCP_URL` reachable over HTTPS, `smoke_mcp.py` passing. Copilot Studio → the ticket agent → Tools → Add a tool → **Model Context Protocol** → New MCP server.

## Pass 1: None
Server URL `TICKET_MCP_URL`, name `tickets-none`, auth **None**. Finish. Expected: four tools listed; "Allow all" off by default in this lab (`allow_list.md`). What is stored: nothing beyond the URL.

## Pass 2: API key (header)
Redeploy with `TICKET_MCP_API_KEY=<value> bash mcp_server/deploy_container_apps.sh`. Add the server again as `tickets-apikey`, auth **API key**, location **Header**, name `X-API-Key`. Expected: on first use **each user** is asked for the key; the key is stored in that user's connection, not by the maker. A wrong key yields the server's 401 in the activity trace.

## Pass 3: OAuth 2.0, manual
Needs an Entra app for the server: expose an API `api://<server-app-id>` with scope `Tickets.ReadWrite`; add the wizard's callback URL (shown in the dialog) as a redirect URI; a client secret for the connector is held by the connector infrastructure, not by your repo. Add the server as `tickets-oauth`, auth **OAuth 2.0 → Manual**: client id, secret, `https://login.microsoftonline.com/<tenant>/oauth2/v2.0/authorize`, `.../token`, refresh URL same as token, scope `api://<server-app-id>/Tickets.ReadWrite offline_access`. Expected: first question shows a sign-in card; after consent the token lives in the user's connection; the server (if you validate the JWT) sees the user's `oid`. Dynamic discovery is the shorter route when the server publishes `.well-known/oauth-protected-resource`.

## What to record
For each pass: which principal the server saw (`none`, `shared key holder`, the user's `oid`), whether the wizard stored anything maker-side, and the first-use prompt the user saw.

## The DLP check
In PPAC create a DLP policy that puts the new MCP connector in **Blocked**, assign it to the environment, return to the agent: the tools show as blocked and **Publish is disabled** (F1). Remove the policy to continue. C09 lab 02 does this properly.
