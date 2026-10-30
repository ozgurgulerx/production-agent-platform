# 02 — Hosted agents: ways 5, 6 and 7

A hosted agent is your code in a container that Foundry runs for you: managed endpoint, per-session sandbox, scaling, a dedicated Entra identity, injected tracing. The container contract is small: listen on **8088**, answer `GET /readiness`, serve `POST /responses` (and/or `/invocations`), read the `FOUNDRY_*` environment variables, exit cleanly on SIGTERM. `ResponsesHostServer` from `agent-framework-foundry-hosting` implements all of it in one line.

![Foundry Hosted Agent Architecture](../../../labs-setup/assets/images/foundry_hosted_agent.png)

| Way | Folder | You bring | Foundry does | When |
|---|---|---|---|---|
| 5 | `code-deploy/` | `main.py` + `requirements.txt` | zips, builds the image remotely, runs it | default; no Docker |
| 6 | `container-deploy/` | a `Dockerfile` (or an image in ACR) | builds in ACR (or pulls yours), runs it | you need system packages, a base image, or a non-Python stack |
| 7 | `self-hosted-aca/` | the same server on Azure Container Apps | models, toolbox, tracing only | platform constraints: your VNet, your scaler, your patch cadence |

Everything about the agent (name, protocol, CPU/memory, env, model deployment, toolboxes) lives in **`azure.yaml`**. There is no `agent.yaml` in the current azd extension; the Ignite-2025 version of this folder had one and it is gone.

## Prerequisites
- `labs/README.md` setup done; `azd` ≥ 1.34.2 and `azd ext install microsoft.foundry` done (`azd ext show azure.ai.agents` ≥ 1.0.0-beta.18).
- Foundry Project Manager on the project (hosted agents provision infrastructure).
- Docker only for `azd ai agent run` (local container) or `remoteBuild: false`.

## Way 5 — code deploy
```bash
cd 02-hosted-agents/code-deploy
azd ai agent init -m ./azure.yaml --deploy-mode code     # picks subscription, project, model
azd provision                                            # creates project/model only if missing
azd ai agent run                                         # local host on http://localhost:8088
azd ai agent invoke --local "What is the status of ticket 8841?"
azd deploy                                               # zip → remote build → version 1 → active
azd ai agent invoke "What is the status of ticket 8841?"
azd ai agent monitor --follow                            # logs + traces
python deploy_with_sdk.py                                # the same deploy in 40 lines of SDK
```
`deploy_with_sdk.py` shows the SDK call behind `azd deploy`: `create_version_from_code(HostedAgentDefinition(code_configuration=CodeConfiguration(runtime="python_3_13", entry_point=[...], dependency_resolution=REMOTE_BUILD), protocol_versions=[ProtocolVersionRecord("responses", "2.0.0")]))`, then poll `get_version` until `active`.

## Way 6 — container deploy
```bash
cd 02-hosted-agents/container-deploy
azd ai agent init -m ./azure.yaml --deploy-mode container
azd provision && azd deploy && azd ai agent invoke "Is ticket 8841 still open?"
ACR_NAME=<acr> python deploy_with_sdk.py                 # docker build --platform linux/amd64, push, HostedAgentDefinition(container_configuration=ContainerConfiguration(image=...))
```
`variants/langgraph` and `variants/openai-agents-sdk` are the same contract with other frameworks. See `variants/README.md`.

## Way 7 — self-hosted on Container Apps
```bash
cd 02-hosted-agents/self-hosted-aca
python main.py &  python invoke.py http://localhost:8088     # same server, your laptop
set -a; source ../.env; set +a; bash deploy.sh             # ACA with system identity + Azure AI User on the project
python invoke.py https://<fqdn>
```
What you lose versus 5/6: the per-agent Entra identity, session sandboxes, the Foundry endpoint URL, and the portal playground. What you gain: your own network, scaler and image pipeline. In F04 this endpoint is registered back into Foundry as an A2A target so prompt agents can call it.

## Lifecycle facts to remember
- Each `azd deploy` or `create_version` is a new immutable version; the endpoint serves one version at 100 %. Rollback = `update_details(agent_endpoint=AgentEndpointConfig(version_selector=...))` (see `../01-seven-ways/07-versions-and-publish.py`).
- Sandbox sizes: 0.5 vCPU/1 GiB, 1/2 GiB, 2/4 GiB. Idle timeout 2–240 min (default 15). Sessions and their `$HOME` / `/files` are deleted after 30 days idle.
- Status values: `creating → active | failed`. A failed version with `main.py` not at the zip root is the most common cause on the code path; wrong image platform on the container path.
- Two identities: the agent's own Entra ID for runtime calls (what `DefaultAzureCredential` picks up inside the container), and the project managed identity for pulling the image.
- Hosted agents are available in 30 regions (the old "North Central US only" note is obsolete).

## Proof (checklist)
- [ ] `azd deploy` (code) prints the agent endpoint and `azd ai agent invoke` returns the ticket status
- [ ] `deploy_with_sdk.py` reaches `status: active` and answers, then deletes itself
- [ ] container variant deploys from the Dockerfile; `docker inspect` shows `linux/amd64`
- [ ] self-hosted: `invoke.py` against the ACA URL returns an answer mentioning "self-hosted"
- [ ] `../01-seven-ways/06-invoke-everything.py` lists `ticket-agent-hosted-code` and `ticket-agent-hosted` with all four controls working
- [ ] trace for one hosted call visible in the portal (Observability → Tracing)

## Next
`../03-multi-agent-workflow/` for the multi-agent hosted agent; identity continues in F04 lab 01.

---

**Author:** Ozgur Guler | AI Solution Leader, AI Innovation Hub | [ozgur.guler1@gmail.com](mailto:ozgur.guler1@gmail.com)
© 2025–2026 Ozgur Guler. All rights reserved.
