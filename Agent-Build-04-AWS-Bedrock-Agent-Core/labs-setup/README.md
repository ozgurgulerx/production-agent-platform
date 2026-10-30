# labs-setup — the one environment shared by the B-chapter labs

Each chapter carries its own `labs/` so a subject stays in one place; what they share lives here once: the Python environment, the pinned requirements, the setup and verify scripts, the model-access step and the notebook helper. The `.env` sits one level up, at the track root, so every script in every chapter finds it by walking up. This track is the AWS mirror of `../../Agent-Build-02-Microsoft-Foundry/`; the chapter numbers line up (B03 ↔ F03 creating agents, B04 ↔ F04 tooling and identity, B05 ↔ F05 evals, B09 ↔ F09 the gateway/governance slot).

```
Agent-Build-04-AWS-Bedrock-Agent-Core/
├── .env.example                      copy to .env (same folder); IAM/SSO only, no access keys
├── labs-setup/
│   ├── 00-setup/                     account + CLI prerequisites, scripts/bootstrap_venv.sh, scripts/verify.sh, execution role, proof checklist
│   ├── 01-models/                    model access, inference profiles, service tiers, prompt router; smoke_test.py through Converse with SigV4
│   ├── .venv/                        Python 3.13; bedrock-agentcore 1.25.0, strands-agents 1.62.0, strands-agents-evals 1.7.0, boto3 1.43.118
│   ├── requirements.txt              fully pinned
│   ├── assets/                       diagrams
│   └── tools/nb_from_py.py           regenerate a notebook from a `# %%`-sectioned script
├── reference/                        dated reading map (25 Oct 2026), letters A–M cited by every chapter
├── B01-AWS-Landing-Zones-for-Agents/            skeleton (Organizations, SCPs, VPC egress, PrivateLink)
├── B02-AgentCore-SDKs-and-Automated-Deployment/ skeleton (boto3 planes, AgentCore CLI 1.0 + CDK, Runtime V1/V2, pricing)
├── B03-Creating-Agents-on-AgentCore/labs/       01 ways to build · 02 runtime containers · 03 multi-agent · 04 memory
├── B04-AgentCore-Tooling-Identity-and-MCP/labs/ 01 identity inbound · 02 MCP on Runtime · 03 gateway · 04 auth matrix · 05 registry · 06 A2A + runtime targets
├── B05-AgentCore-Evals-and-Observability/labs/  01 observability · 02 evals · 03 guardrails
├── B06-Bedrock-Fine-Tuning/labs/                01 SFT for tone on Nova 2 Lite, custom-model on-demand deploy, eval tuned vs base
├── B07-Local-Agents-with-Strands/labs/          01 the ticket agent on Ollama / llama.cpp (no AWS), Runtime contract locally
├── B08-Bedrock-Knowledge-Bases/labs/            01 managed knowledge base → Gateway KB target → agent with citations
└── B09-AgentCore-Policy-and-Governance/labs/    01 Cedar policy · 02 guardrails in policy · 03 org controls
```

## Set up once
```bash
cd Agent-Build-04-AWS-Bedrock-Agent-Core
bash labs-setup/00-setup/scripts/bootstrap_venv.sh       # creates labs-setup/.venv on python3.13
source labs-setup/.venv/bin/activate
cp .env.example .env                                      # AWS_REGION, AWS_PROFILE, BEDROCK_MODEL_ID at minimum
brew install awscli node                                  # aws CLI v2, Node 20.12+ (not installed on this machine on 25 Oct 2026)
npm install -g @aws/agentcore                             # the AgentCore CLI 1.0; NOT pip bedrock-agentcore-starter-toolkit (deprecated)
aws configure sso && aws sso login --profile <name>       # IAM Identity Center; put the profile name in .env
bash labs-setup/00-setup/scripts/verify.sh                # must print OK
python labs-setup/01-models/smoke_test.py                 # one Converse call through the inference profile in .env
```
Details, the execution role and the proof checklist: [`00-setup/README.md`](00-setup/README.md).

## Order across chapters
| Session | Chapter | Labs | Outcome |
|---|---|---|---|
| 1 | setup + B03 | 00, 01-models, B03 01 | `ticket-agent-runtime` READY; `04-invoke-everything.py` streams an answer; a Harness answers the same question |
| 2 | B03 | 02, 03 | container runtime active; graph agent and A2A server deployed; A2A client gets a card |
| 3 | B04 | 01, 02, 03 | Cognito JWT accepted on a runtime (401 first, then 200); MCP server on Runtime answers `list_tools`; gateway with semantic search finds `issue_refund` |
| 4 | B04 | 04, 05, 06 | auth matrix rows that have credentials pass; registry record approved and discoverable; runtime as a gateway target |
| 5 | B05 | 01, 02 | spans in the per-agent log group; on-demand `Builtin.*` scores; online config ACTIVE at 10 % |
| 6 | B05 + B09 | 03, 01 | guardrail blocks a prompt attack; Cedar `LOG_ONLY` logs a would-deny for a 900 GBP refund, `ENFORCE` denies it |
| 7 | B09 | 02, 03 | guardrails-in-policy on the gateway; CloudTrail audit of who created what |
| optional | B03 | 04 | memory recall across two sessions |
| 8 | B08 | 01 | knowledge base ingested from code; agent cites the card policy and refuses the Peru case |
| 9 | B06 | 01 | tuned vs base side by side from the same cases; promote-or-hold verdict |
| 10 | B07 | 01 | same agent answering from a local model; `curl /ping` on 8080 returns Healthy |

B04, B05 and B09 labs assume the resources B03 lab 01 and B04 labs 01–03 create (`TICKET_AGENT_RUNTIME_ARN`, `COGNITO_*`, `TICKET_GATEWAY_ID`), written into `.env` by the scripts.

## Rules the code follows (do not regress)
IAM/SSO or Cognito JWT only; no `aws_access_key_id` in any file. boto3 `bedrock-agentcore-control` for control plane, `bedrock-agentcore` for data plane. `BedrockAgentCoreApp` with `@app.entrypoint` that checks `prompt` is a string; `/invocations` + `/ping` on 8080, MCP on 8000, A2A on 9000. `runtimeSessionId` ≥33 characters. The AgentCore CLI is `@aws/agentcore` (Node); never `agentcore configure|launch`, never `.bedrock_agentcore.yaml`, never the Python starter toolkit. ARM64 images. Evaluator ids spelled `Builtin.<Name>`. Every created resource has a `--cleanup` path; destroy runtimes at the end of a session (per-second billing continues while a session is active). Proof checklists ticked only with real output.

## Cost guard
Everything is per-second consumption. A lab day that destroys its runtimes at the end should stay under about USD 20 (Runtime V1 USD 0.0895 per vCPU-hour, Gateway USD 0.005 per 1,000 calls, Policy USD 0.000025 per authorisation, Evaluations USD 0.0024 / 0.012 per 1,000 judge tokens; reading map L8).
