# 05 — Your app calls the agent on behalf of the user (Direct-to-Engine)

**Start with the failure.** Call the agent from a service with the service's own token: the agent answers as nobody, every end-user-credential tool fails, and the transcript has no user. Direct-to-Engine is meant to carry the user: the app exchanges the user's token on-behalf-of for `CopilotStudio.Copilots.Invoke`.

## Goal
A minimal FastAPI web app with a `/chat` endpoint that takes the user's bearer token, performs OBO, and streams the Copilot Studio agent's Activities back with the Agents SDK Copilot Studio client.

## You will end with
- `web_app/app.py` running locally; a `curl` with a user token returns the agent's answer and the user is visible in the transcript
- a note on when to use Direct Line instead, and what the Agents Client SDK is for

## Prerequisites
A **confidential** app registration for the web app with a certificate or a federated identity credential (no client secret in the repo), exposing a scope `access_as_user`; the Power Platform API delegated permission `CopilotStudio.Copilots.Invoke` added to it and consented; `WEBAPP_CLIENT_ID`, `WEBAPP_CERT_PATH` (PEM with private key) in the environment. The user's token must be issued for the web app's scope.

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
cd 05-direct-to-engine-apps
WEBAPP_CLIENT_ID=<id> WEBAPP_CERT_PATH=./webapp.pem uvicorn web_app.app:app --port 8002
curl -s -H "Authorization: Bearer <user token for api://<WEBAPP_CLIENT_ID>/access_as_user>" \
     -H 'Content-Type: application/json' -d '{"text":"What is ticket 1042 about?"}' localhost:8002/chat
```

## Facts that matter (reading map)
- C8: Direct-to-Engine needs delegated `CopilotStudio.Copilots.Invoke`, environment id + schema name; OBO for services; Standard-harness agents only.
- C9: `CopilotClient(ConnectionSettings(environment_id, agent_identifier, cloud=PowerPlatformCloud.PROD, copilot_agent_type=AgentType.PUBLISHED), token)`; `start_conversation()` and `ask_question()` yield Activities.
- C10: Direct Line token endpoint for custom canvases; Agents Client SDK for mobile, unauthenticated only.

## Proof (checklist)
- [ ] a request with the user's token returns the agent's answer; the ConversationTranscript row (C05 lab 02) shows that user
- [ ] a request with the app's own token (client credentials) is rejected or answers without a user; note which
- [ ] the certificate or FIC path is used; `grep -r client_secret web_app` is empty

## Next
`../../C05-Evaluation-Observability-and-Safety/labs/`.
