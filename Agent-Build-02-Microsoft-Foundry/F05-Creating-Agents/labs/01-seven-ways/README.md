# 01 — Create the same agent seven ways

One agent, the support-ticket assistant, built every way Foundry allows. The point is not the agent. The point is to see where the **definition** lives and where the **loop** runs in each case, because that decides what you can version, govern, trace and roll back. Every variant is then called through the same surface, `POST /responses`.

| # | Way | Definition lives | Loop runs | Status | File |
|---|---|---|---|---|---|
| 1 | Prompt agent, portal | Foundry, versioned | Foundry | GA | `01-prompt-agent-portal.md` |
| 2 | Prompt agent, SDK / REST / azd | Foundry, versioned | Foundry | GA | `02-prompt-agent-sdk.py`, `02b-prompt-agent-azd/` |
| 2b | Same agent driven from Agent Framework (`FoundryAgent`), and exported from Agent Framework (`to_prompt_agent`) | Foundry | Foundry | GA | `05-foundry-agent-af.py` |
| 3 | Voice prompt agent | Foundry, `kind: voice` | Foundry + Voice Live | preview | `03-voice-prompt-agent.py` |
| 4 | Ephemeral agent (Responses API) | your request | Foundry runtime, nothing to version | GA | `04-ephemeral-agent.py` |
| 5 | Hosted agent from source zip | your container | Foundry sandbox | GA | `../02-hosted-agents/code-deploy/` |
| 6 | Hosted agent from container image | your container | Foundry sandbox | GA | `../02-hosted-agents/container-deploy/` |
| 7 | Self-hosted on your compute, Foundry models + toolbox | your infra | your infra | GA | `../02-hosted-agents/self-hosted-aca/` |

Then `06-invoke-everything.py` calls whichever of them exist, identically, and `07-versions-and-publish.py` shows versions, routing and what "publish" now means.

Decision rule to carry: *declarative loop → prompt agent; custom loop, dependencies or state → hosted; nothing to manage → ephemeral; your own platform constraints → self-hosted.*

## Prerequisites
`labs-setup/` done (shared venv, `.env` at the track root; see `../README.md`). Voice (way 3) additionally needs a `gpt-realtime` deployment, the voice preview enabled on the project, and `pip install "azure-ai-projects[voice]"` in `.venv`.

## Run
```bash
source ../.venv/bin/activate
cd 01-seven-ways
python 02-prompt-agent-sdk.py --keep      # way 2; --keep leaves ticket-agent-prompt for 05/06/07
python 05-foundry-agent-af.py             # FoundryAgent + to_prompt_agent
python 04-ephemeral-agent.py              # way 4, both spellings, plus reasoning effort
python 03-voice-prompt-agent.py           # way 3 (preview)
python 06-invoke-everything.py            # conversation / previous_response_id / stream / background
python 07-versions-and-publish.py         # creates v2, pins endpoint to v1, back to latest, deletes
cd 02b-prompt-agent-azd && azd ai agent init -m ./azure.yaml && azd provision && azd deploy   # way 2 via azd
```

## What each script proves
- **02** `create_version` is the only create call; `get_openai_client(agent_name=)` is pre-bound; a `conversation` carries state server-side; `previous_response_id` chains without one; versions list.
- **05** `FoundryAgent` replaces the removed `AzureAIAgentClient`; `to_prompt_agent()` moves a locally authored agent into Foundry as a prompt agent.
- **04** `FoundryChatClient` and a raw `OpenAI(base_url=.../openai/v1)` produce the same answer: the wire format is the OpenAI Responses API. No resource is created. The function tool runs in your process.
- **03** `VoiceAgentDefinition` goes through the same `create_version`; the endpoint is a realtime WebSocket; stored conversations are listable.
- **06** the four Responses controls behave the same for prompt and hosted agents.
- **07** one version serves 100 % of traffic; `update_details(agent_endpoint=…)` is the rollback; the agent already has an endpoint and an identity, so "publish" means Copilot/Teams distribution (`publish_to_microsoft365`), not creating an application.

## Proof (checklist)
- [ ] 02 prints turn 2 recalling the order number, and `versions: ['1']`
- [ ] 04 prints three answers (agent framework, streaming, reasoning) and the raw-client answer
- [ ] 05 prints the exported agent's answer mentioning Agent Framework
- [ ] 06 shows `conversation`, `chained`, `stream`, `background: completed` for `ticket-agent-prompt`
- [ ] 07 shows the v2 marker disappear after rollback and reappear after roll-forward
- [ ] 03 prints a transcript (or is marked skipped with the preview-access reason)
- [ ] `02b` `azd deploy` output shows the prompt agent version in the portal

## What changed since the Ignite 2025 version of this folder
`AzureOpenAIResponsesClient` with an API key and the classic `azure.ai.agents` threads/runs scripts are gone. Entra only; `azure-ai-projects` 2.x only; `FoundryChatClient` / `FoundryAgent` only.

## Next
`../02-hosted-agents/` — ways 5, 6 and 7.

---

**Author:** Ozgur Guler | AI Solution Leader, AI Innovation Hub | [ozgur.guler1@gmail.com](mailto:ozgur.guler1@gmail.com)
© 2025–2026 Ozgur Guler. All rights reserved.
