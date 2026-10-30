# labs-setup — the one environment shared by the F05, F06 and F08 labs

The three chapters each carry their own `labs/` folder so a subject stays in one place. What they share lives here, once: the Python environment, the pinned requirements, the setup and verify scripts, the diagram assets and the notebook helper. The `.env` sits one level up, at the track root, so every script in every chapter finds it by walking up.

```
Agent-Build-02-Microsoft-Foundry/
├── .env.example                      copy to .env (same folder); Entra only, no API keys
├── labs-setup/
│   ├── 00-setup/                     tooling, scripts/bootstrap_venv.sh, scripts/verify.sh, proof checklist
│   ├── 01-models/                    pick the model, pick the deployment type, deploy the four deployments (CLI + Bicep), Entra-only smoke test
│   ├── .venv/                        Python 3.13; azure-ai-projects 2.7.0, agent-framework-foundry 1.15.0, hosting 1.0.0b261022
│   ├── requirements.txt              fully pinned
│   ├── assets/                       diagrams
│   └── tools/nb_from_py.py           regenerate a notebook from a `# %%`-sectioned script
├── reference/                        dated reading map (25 Oct 2026)
├── F05-Creating-Agents/labs/   01 seven ways · 02 hosted agents · 03 multi-agent workflow · 04 memory · 05 AI Search
├── F06-Agent-Tooling-MCP-and-Integration/labs/               01 identity & CA · 02 MCP tool · 03 toolbox · 04 auth matrix + APIM · 05 private catalog · 06 A2A
├── F08-Evals-Tracing-and-Release/labs/                       01 observability · 02 evals (own .venv on azure-ai-projects 2.9.0)
├── F12-Fine-Tuning-and-Model-Routing/labs/                         01 SFT for tone on gpt-4.1-mini, Developer tier, eval tuned vs base
├── F13-Foundry-Local/labs/                         01 the ticket agent on a local model (no Azure), Olive INT4
└── F07-RAG-on-AI-Search/labs/                         01 knowledge base (Blob source → knowledge base → MCP tool, citations)
```

## Set up once
```bash
cd "Agent-Build-02-Microsoft-Foundry"
bash labs-setup/00-setup/scripts/bootstrap_venv.sh      # creates labs-setup/.venv on python3.13
source labs-setup/.venv/bin/activate
cp .env.example .env                                     # FOUNDRY_PROJECT_ENDPOINT, FOUNDRY_MODEL at minimum
az login && azd auth login
azd ext install microsoft.foundry                        # azd >= 1.34.2; azd ext show azure.ai.agents >= 1.0.0-beta.18
bash labs-setup/00-setup/scripts/verify.sh               # must print OK
bash labs-setup/01-models/deploy_models.sh              # the four model deployments the labs assume
```
Details and the proof checklist: [`00-setup/README.md`](00-setup/README.md). The evals lab needs `azure-ai-projects>=2.9`, which conflicts with `agent-framework-foundry`; it has its own venv, created from its README.

## Order across chapters
| Session | Chapter | Labs | Outcome |
|---|---|---|---|
| 1 | setup + F05 | 00, 01-models, F05 01 | seven agents exist; `06-invoke-everything.py` passes for the prompt agent |
| 2 | F05 | 02, 03 | hosted agent from source and container active; workflow agent active; invoke-everything passes for all |
| 3 | F06 | 01, 02, 03 | identity visible in Conditional Access; MCP approval loop; toolbox v1/v2 |
| 4 | F06 | 04, 05, 06 | auth matrix output; API Center entry; A2A delegation |
| 5 | F08 | 01, 02 | traces in App Insights; batch eval `report_url`; continuous rule on |
| optional | F05 | 04, 05 | memory and AI Search grounding |
| 6 | F07 | 01 | knowledge base provisioned from code; agent cites policy documents |
| 7 | F12 | 01 | tuned vs base `report_url`s side by side |
| 8 | F13 | 01 | same agent answering from a local model; `foundry model list --cached` |

F06 and F08 labs assume the agents F05 lab 01 and 02 create (`ticket-agent-prompt`, `ticket-agent-hosted-code`, `ticket-agent-workflow`).

## Rules the code follows (do not regress)
Entra only (`DefaultAzureCredential`). `azure-ai-projects` 2.x, never `azure.ai.agents`. `FoundryChatClient` / `FoundryAgent`, never `AzureOpenAIResponsesClient` / `AzureAIAgentClient`. Hosting via `agent_framework_foundry_hosting.ResponsesHostServer`, never `azure.ai.agentserver.agentframework`. All hosted-agent config in `azure.yaml`, no `agent.yaml`, protocol `responses 2.0.0`. Invoke with `project.get_openai_client(agent_name=...)`, no `extra_body`. `MCPTool` from `azure.ai.projects.models`; always handle `mcp_approval_request` and `oauth_consent_request`. Get-or-create; clean up versions (cap 1,000).
