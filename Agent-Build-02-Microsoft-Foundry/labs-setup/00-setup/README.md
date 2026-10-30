# 00 — Environment setup

## Goal
One repeatable local environment shared by the F03, F04 and F05 labs: Python 3.13 (the same runtime Foundry builds hosted agents on), `az` and `azd` logged in, the azd Foundry extension bundle, and a `.env` that names your project endpoint and model deployments. Authentication is Entra only. No API keys appear anywhere in this repo.

## You will end with
- `labs-setup/.venv/` on Python 3.13 with the pinned package set in `requirements.txt`
- `az login` and `azd auth login` done, `azd ext install microsoft.foundry` done
- `.env` at the track root (`Agent-Build-02-Microsoft-Foundry/.env`) with `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL`
- `bash labs-setup/00-setup/scripts/verify.sh` printing `OK`

## Prerequisites
- A Foundry project (Standard setup if you want private MCP in F04 labs 02–04). Endpoint shape: `https://<resource>.services.ai.azure.com/api/projects/<project>`.
- RBAC on the project: **Foundry User** to run agents, **Foundry Project Manager** to create hosted agents (F03 labs 02–03).
- Model deployments: created in `../01-models/` (a chat model, `gpt-5-mini` throughout; an embedding model for F03 lab 04; `gpt-realtime` for the voice step in F03 lab 01).
- Tools: Python 3.13+, Azure CLI, Azure Developer CLI **1.34.2 or later** (the `azure.ai.agents` extension beta.18+ refuses older azd), Docker only if you take the container path in F03 lab 02.

## Install tooling
```bash
brew install azure-cli
brew trust azure/azd && brew install --cask azure/azd/azd      # or upgrade: brew upgrade --cask azd
azd ext install microsoft.foundry      # pulls azure.ai.agents, .connections, .toolboxes, .skills, .routines, .projects, .inspector
azd ext show azure.ai.agents           # expect 1.0.0-beta.18 or later
```

## Create the virtual environment
```bash
cd "Agent-Build-02-Microsoft-Foundry"
bash labs-setup/00-setup/scripts/bootstrap_venv.sh     # picks python3.13, installs labs-setup/requirements.txt
source labs-setup/.venv/bin/activate
```
`requirements.txt` is fully pinned. `agent-framework-foundry` 1.15.0 requires `azure-ai-projects<2.8`, so this venv runs 2.7.0. `F08-Evals-Tracing-and-Release/labs/02-evals` needs the 2.9 evaluation surface and ships its own `requirements.txt`; create a second venv there when you reach it.

## Configure `.env`
```bash
cp .env.example .env            # at the track root; every lab walks up to find it
```
Fill `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL` first. Everything else is per lab and documented in that lab's README. The old `AZURE_OPENAI_*` keys are gone: every script authenticates with `DefaultAzureCredential` against the project endpoint.

## Sign in
```bash
az login
azd auth login
```

## Verify
```bash
bash labs-setup/00-setup/scripts/verify.sh
```
The script checks tooling, both logins, the azd extension, the Python package generation (it fails on `azure-ai-projects` 1.x or the retired `azure-ai-agentserver-agentframework`), the `.env` contract, and finally lists the agents in your project to prove the endpoint and RBAC work.

## Proof (checklist)
- [ ] `verify.sh` prints `OK`
- [ ] `azd ext show azure.ai.agents` shows 1.0.0-beta.18 or later
- [ ] `.env` holds `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL`

## Next
`../01-models/` — choose and deploy the models every lab points at. Then F03 `labs/01-seven-ways/`.

---

**Author:** Ozgur Guler | AI Solution Leader, AI Innovation Hub | [ozgur.guler1@gmail.com](mailto:ozgur.guler1@gmail.com)
© 2025–2026 Ozgur Guler. All rights reserved.
