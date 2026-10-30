# C04 labs — identity, MCP, REST and flow tools, connected agents, Direct-to-Engine

Runnable proofs for the C04 chapter. Setup is shared: [`../../labs-setup/`](../../labs-setup/) (venv, `.env` at the track root, `pac auth` signed in, `verify.sh` printing OK). These labs assume C03 lab 01 has run and written `AGENT_SCHEMA_NAME` and `AGENT_ID`. Scripts sign in with a device code through the public-client app registration from `labs-setup/00-setup` (no secrets). Each lab README ends with a **proof checklist**; a lab is done when the boxes are ticked with real output. Nothing here has run yet.

```
labs/
├── 01-identity/                 the agent's Entra Agent ID in Graph, its connector scopes, the inventory entry, CA note, credential switch + security scan
├── 02-mcp-tool/                 the ticket MCP server on Container Apps → wizard (None / API key / OAuth) → custom connector route → allow-list
├── 03-rest-and-flow-tools/      OpenAPI v2 REST tool, agent flow with approval above 250, Dataverse MCP, prompt tool
├── 04-connected-agents/         Foundry agent (enable Activity endpoint first), A2A remote agent, Agents SDK agent, publish this agent as A2A for Foundry
└── 05-direct-to-engine-apps/    a web app calling the agent on behalf of the user with the Agents SDK Copilot Studio client
```

| Lab | Chapter section | Writes to `.env` | Needs beyond the shared setup |
|---|---|---|---|
| 01 | §1 identity, §2 credentials | `AGENT_ENTRA_OBJECT_ID` | Graph `Application.Read.All` consented on the app registration |
| 02 | §3 MCP | `TICKET_MCP_URL` | an Azure subscription for Container Apps (or any HTTPS host); for the OAuth pass, an Entra app for the server |
| 03 | §4 other tools | `TICKET_API_BASE` | the same host for the REST API |
| 04 | §5 connected agents | — | the Foundry track `.env` (F03 agent) and/or the AWS track A2A runtime; C03 lab 04 for the SDK agent |
| 05 | §6 from code | — | a confidential app with a certificate or federated credential for OBO |

Order: 01 → 02 → 03 → 04 → 05. Session 3 is 01–02, session 4 is 03–05.

```bash
source ../../labs-setup/.venv/bin/activate
cd 01-identity && python inspect_agent_identity.py
```

Next chapter: [`../../C05-Evaluation-Observability-and-Safety/labs/`](../../C05-Evaluation-Observability-and-Safety/labs/).
