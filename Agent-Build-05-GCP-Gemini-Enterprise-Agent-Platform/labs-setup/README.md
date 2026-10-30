# labs-setup — the one environment shared by the G03, G04 and G05 labs

Each chapter carries its own `labs/` folder so a subject stays in one place. What they share lives here, once: the Python environment, the pinned requirements, the setup and verify scripts and the notebook helper. The `.env` sits one level up, at the track root, so every script in every chapter finds it by walking up. Facts are cited by letter from the reading map in [`../reference/reading-map-gcp-agents-2026-10-25.md`](../reference/reading-map-gcp-agents-2026-10-25.md).

```
Agent-Build-05-GCP-Gemini-Enterprise-Agent-Platform/
├── .env.example                      copy to .env (same folder); ADC only, no API keys
├── labs-setup/
│   ├── 00-setup/                     tooling, scripts/bootstrap_venv.sh, enable_apis.sh, verify.sh, proof checklist
│   ├── 01-models/                    pick region and model ids, smoke test, staging bucket
│   ├── .venv/                        Python 3.13; google-adk 2.13.0, google-cloud-agentplatform 2.6.0, google-genai 2.33.0
│   ├── requirements.txt              fully pinned
│   └── tools/nb_from_py.py           regenerate a notebook from a `# %%`-sectioned script
├── reference/                        dated reading map (25 Oct 2026) and the Foundry ↔ GCP comparison
├── G01-GCP-Agent-Landing-Zones/      skeleton: VPC-SC, PSC, CMEK, org policy, IAM, Terraform
├── G02-SDKs-and-Automated-Deployment/labs/   01 deploy pipeline: agents-cli, Terraform, revisions and traffic
├── G03-Creating-Agents/labs/         01 ways to run · 02 Agent Runtime · 03 multi-agent workflow · 04 Memory Bank · 05 grounding
├── G04-Agent-Tooling-Identity-MCP-A2A/labs/  01 identity · 02 MCP tool · 03 MCP Toolbox · 04 auth matrix + Apigee · 05 registry · 06 A2A
├── G05-Evals-and-Observability/labs/ 01 observability + Model Armor · 02 evals (adk eval, platform evals, CI gate)
├── G06-Fine-Tuning/labs/             01 SFT for tone on gemini-3.5-flash-lite, eval tuned vs base
├── G07-Local-and-Edge/labs/          01 the ticket agent on Gemma 4 via Ollama (no cloud)
├── G08-Knowledge-Agent-Search-RAG-Engine/labs/   01 knowledge base (GCS → data store / RAG corpus → tool, citations)
└── G09-Apigee-Integrated-Designs/    designs only
```

## Set up once
```bash
cd Agent-Build-05-GCP-Gemini-Enterprise-Agent-Platform
bash labs-setup/00-setup/scripts/bootstrap_venv.sh      # creates labs-setup/.venv
source labs-setup/.venv/bin/activate
cp .env.example .env                                     # GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION at minimum
gcloud auth login && gcloud auth application-default login
gcloud config set project "$GOOGLE_CLOUD_PROJECT"
bash labs-setup/00-setup/scripts/enable_apis.sh
bash labs-setup/00-setup/scripts/verify.sh               # must print OK
python labs-setup/01-models/smoke_test.py                # three model lines
```
Details and the proof checklist: [`00-setup/README.md`](00-setup/README.md). Terraform (G01, G02) and MCP Toolbox (G04 lab 03) are installed when those chapters ask.

## Order across chapters
| Session | Chapter | Labs | Outcome |
|---|---|---|---|
| 1 | setup + G03 | 00, 01-models, G03 01 | the ticket agent runs under `adk web`, `adk run`, `adk api_server`, and on Cloud Run |
| 2 | G03 | 02, 03 | `ticket-agent` on Agent Runtime with a `reasoningEngines/ID`; workflow agent deployed; both answer `:query` |
| 3 | G04 | 01, 02, 03 | `spec.effectiveIdentity` shows a SPIFFE principal; MCP tool call round-trips; Toolbox on Cloud Run with Google auth |
| 4 | G04 | 04, 05, 06 | auth matrix output; agent and MCP server in Agent Registry; A2A delegation |
| 5 | G05 | 01, 02 | traces in Cloud Trace; Model Armor floor setting blocks a jailbreak; `adk eval` and platform eval reports |
| optional | G03 | 04, 05 | Memory Bank recall across sessions; Agent Search grounding |
| 6 | G08 | 01 | data store and RAG corpus from code; agent cites policy documents |
| 7 | G06 | 01 | tuned vs base eval side by side |
| 8 | G07 | 01 | same agent answering from Gemma 4 locally |

G04 and G05 labs assume the agents G03 labs 01–03 create (`ticket-agent`, `ticket-agent-workflow`) and `AGENT_RUNTIME_RESOURCE` in `.env`.

## Rules the code follows (do not regress)
ADC only (`gcloud auth application-default login`; `google.auth.default()` in code); no `GOOGLE_API_KEY`. `GOOGLE_GENAI_USE_VERTEXAI=TRUE` everywhere so ADK and google-genai talk to the platform. `google-adk` 2.x; `LlmAgent`/`Agent` from `google.adk.agents`; `Runner` from `google.adk.runners`. Deploy through `adk deploy agent_engine` or `agentplatform.Client().runtimes` (map A5, C2), never the old `vertexai.agent_engines` surface except in the one "old vs new" sketch. `McpToolset` from `google.adk.tools.mcp_tool`, defined synchronously in `agent.py`; one built-in tool per agent, wrapped in `AgentTool` when combined (map D4). `identity_type=AGENT_IDENTITY` on every Agent Runtime deploy; service accounts only in the G04 lab 01 comparison. Model ids from `.env`, never hard-coded. Get-or-create by `display_name`; delete test agents (`delete(force=True)`); revisions cap at 950 per agent (map A10).
