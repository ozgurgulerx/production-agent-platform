# labs-setup — the one environment shared by the C-chapter labs

Each chapter carries its own `labs/` so a subject stays in one place; what they share lives here once: the Python environment, the pinned requirements, the tenant and tooling checklist, the verify script, the model notes and the notebook helper. The `.env` sits one level up, at the track root, and every script loads it by path. This track is the Copilot Studio mirror of `../../Agent-Build-02-Microsoft-Foundry/` and `../../Agent-Build-04-AWS-Bedrock-Agent-Core/`; chapter numbers line up (C03 ↔ F03 ↔ B03 creating agents, C04 tooling and identity, C05 evals, C09 governance).

```
Agent-Build-03-Microsoft-Copilot-Studio/
├── .env.example                      copy to .env (same folder); Entra device-code only, no client secrets
├── labs-setup/
│   ├── 00-setup/                     tenant, licence, admin, app registration, pac CLI, scripts/bootstrap_venv.sh, scripts/verify.sh
│   ├── 01-models/                    the primary-model dropdown, the retirement wave, external-model consent, credits per feature; read_primary_model.py
│   ├── .venv/                        Python 3.13; microsoft-agents-copilotstudio-client 1.9.0, hosting-aiohttp 1.9.0, msal 1.39.0, mcp 2.3.0
│   ├── requirements.txt              fully pinned
│   ├── assets/
│   └── tools/nb_from_py.py           regenerate a notebook from a `# %%`-sectioned script
├── reference/                        dated reading map (25 Oct 2026), letters A–M cited by every chapter
├── C01-Power-Platform-Landing-Zone-for-Agents/     skeleton (tenant → Managed Environments → your solution)
├── C02-Code-First-Toolchain-and-ALM/               pac, VS Code extension, Power Platform API, Dataverse, credits
├── C03-Creating-Agents-in-Copilot-Studio/labs/     01 ticket agent two ways · 02 GitHub Copilot harness · 03 autonomous trigger · 04 Agents SDK connected
├── C04-Tools-Identity-MCP-and-Connected-Agents/labs/ 01 identity · 02 MCP tool · 03 REST and flow tools · 04 connected agents · 05 Direct-to-Engine apps
├── C05-Evaluation-Observability-and-Safety/labs/   01 evaluation · 02 observability · 03 safety
├── C06-Models-Prompts-and-Customisation/labs/      01 models and prompts (no fine-tuning exists; BYO Foundry model for prompt tools)
├── C07-Code-First-Dev-Loop/labs/                   01 dev loop (YAML in Git, pac, VS Code, Agents SDK on your laptop)
├── C08-Knowledge-and-Memory/labs/                  01 knowledge (SharePoint two ways, Foundry IQ tool, the three policy questions)
└── C09-Governance-and-Agent-365/labs/              01 inventory and quarantine · 02 DLP and environment rules · 03 Agent 365 and Purview
```

## Set up once
```bash
cd Agent-Build-03-Microsoft-Copilot-Studio
bash labs-setup/00-setup/scripts/bootstrap_venv.sh        # creates labs-setup/.venv on python3.13
source labs-setup/.venv/bin/activate
cp .env.example .env                                       # TENANT_ID, CLIENT_ID, ENVIRONMENT_ID, ENVIRONMENT_URL at minimum
brew install dotnet && dotnet tool install --global Microsoft.PowerApps.CLI.Tool   # pac CLI (not installed on this machine on 25 Oct 2026)
pac auth create --deviceCode                               # sign in as the maker/admin; no secrets
bash labs-setup/00-setup/scripts/verify.sh                 # must print OK
python labs-setup/01-models/read_primary_model.py          # after C03 lab 01 created the agent
```
Details, the app registration and the proof checklist: [`00-setup/README.md`](00-setup/README.md).

## Order across chapters
| Session | Chapter | Labs | Outcome |
|---|---|---|---|
| 1 | setup + C03 | 00, C03 01 | ticket agent exists on the Standard harness; cloned to YAML; `invoke_direct_to_engine.py` gets two answers incl. a refusal |
| 2 | C03 | 02, 03, 04 | same agent on the GitHub Copilot harness; a trigger run visible in Activity; the Agents SDK agent answers locally and as a connected agent |
| 3 | C04 | 01, 02 | the agent's Entra Agent ID and connector scopes printed; the MCP server added three ways (None, API key, OAuth) with an allow-list |
| 4 | C04 | 03, 04, 05 | REST tool and approval flow; Foundry agent connected; app calls the agent through Direct-to-Engine |
| 5 | C05 | 01, 02 | test set run from the REST API with per-case scores; `ExecuteTool` spans in App Insights |
| 6 | C05 + C09 | 03, 01 | prompt injection in a knowledge file blocked and audited; agent quarantined and released from the API |
| 7 | C09 | 02, 03 | DLP blocks publish and is reverted; agent found in the Agent 365 registry; Purview audit rows |
| 8 | C08 | 01 | three policy questions answered with citations; Peru refused |
| 9 | C06 + C07 | 01, 01 | model switched and evaluated; the YAML round trip through Git |

C04, C05 and C09 labs assume `AGENT_SCHEMA_NAME` and `AGENT_ID` from C03 lab 01 and `TICKET_MCP_URL` from C04 lab 02, written into `.env` by the scripts.

## Rules the code follows (do not regress)
Entra device-code sign-in through the public-client app in `CLIENT_ID`; no client secrets in any file (service paths use federated credentials or certificates and say so). Standard harness for anything scripted; the GitHub Copilot harness is documented with portal steps. `pac copilot` verbs as documented on 10 Jul 2026 (`init`, `clone`, `pull`, `push`, `pack`, `publish`); never an old `pac chatbot` spelling. Direct-to-Engine via `microsoft_agents.copilotstudio.client` with `AgentType.PUBLISHED`. Evaluation and quarantine through the Power Platform API `copilotstudio` namespace with the api-version the Learn page shows. Billing unit is Copilot Credits, never "messages". Every admin change in C09 has a revert step. Proof checklists ticked only with real output.

## Cost guard
Copilot Credits: generative answer 2, agent action 5, tenant graph grounding 10, flow actions 13 per 100 (reading map K6). A lab day with a few hundred turns stays within a prepaid pack; per-agent caps in PPAC stop a runaway trigger (C09 lab 02).
