# F04 capability builds — Developer setup, model deployment and APIs

## Build contract

Status: **planned; functionality unverified**. Build one capability at a time using the existing module and labs. Record environment/dependency versions, permitted assistance, positive and negative results, and trace/test evidence. The learner writes code and tests; these contracts do not supply hidden implementations. Verify dated API and availability claims before execution.

### Git and reproducible developer environment

- [ ] Build: Create a small isolated branch exercise: inspect diff, stage selectively, commit, merge a conflict and revert a change. Establish per-lab interpreter, dependency lock, environment template and secret exclusion. Compare portal, SDK, REST, az and azd responsibilities.
- [ ] Verify: Reproduce the environment from the lock and run an import/config smoke check; prove missing required configuration fails clearly. Record assistance; timed F3 exercises remain learner-written.

### Model deployment and consumption tiers

- [ ] Build: Create and invoke a supported deployment using code, with deployment name distinct from model ID and management-plane permissions distinct from data-plane access. Compare Standard, Global/Data Zone, PTU, batch, Flex, Priority and managed compute using verified current availability.
- [ ] Verify: Measure a controlled workload and inspect actual service tier, quota behavior, token usage and latency. Do not provision expensive dedicated capacity merely to compare concepts; record unavailable options as not tested.

### Responses and alternative clients

- [ ] Build: Build a typed tool loop with structured output and streaming. Compare Responses and Chat Completions with explicit conversation state. Add bounded independent experiments for WebSocket mode, tool search, deep research, multi-agent Responses, predicted outputs, prompt caching, Decisions API and webhooks only after verifying support for the selected model/API.
- [ ] Verify: For each experiment show valid response and unsupported/invalid-input handling, cancellation or timeout where relevant, and request/trace evidence. Verify webhook authenticity and duplicate delivery. Preserve the unfinished all-tools link as an open source task.

### Provider and production application surface

- [ ] Build: Compare OpenAI and Anthropic clients against the appropriate Foundry endpoints; read an equivalent .NET example. Build a minimal async API with typed settings, timeouts, health/readiness, redacted logs and container packaging. Inspect Canvas/Toolkit/coding-agent skills as developer surfaces.
- [ ] Verify: Demonstrate timeout, malformed tool output and unavailable dependency. Keep request cancellation and resource closure explicit; no live secrets in examples. Delegate cloud release gates to F08 and credential design to F03.

## Exact checklist targets

Each ID below is a distinct occurrence in the [full coverage matrix](../reference/production-build-coverage.md). Source wording is retained, including historical names and unfinished placeholders; it is not a fresh API guarantee. Compound items may require several small builds. Mark complete only after recording evidence.

- [ ] **CB008** — Configure project endpoint, model deployment, and connection IDs via .env.
- [ ] **CB009** — Confirm region, model, tool, and preview support.
- [ ] **CB010** — Foundry Canvas
- [ ] **CB011** — Foundry Toolkit for VSC
- [ ] **CB012** — Foundry Skill for CC / Github Copilot
- [ ] **CB014** — Create and inspect every resource above from the CLI; role assignment commands; `az containerapp up`, revisions and traffic splitting for canaries; `az monitor` queries. Interviewers watch for CLI fluency as a proxy for having done it.
- [ ] **CB015** — C# / .NET awareness — `Azure.AI.Projects`, `Microsoft.Agents.AI.Foundry`, `Azure.AI.OpenAI`; read a .NET agent sample and map it to the Python one. Hays AI Developer names C#.
- [ ] **CB016** — Standard pay-per-token
- [ ] **CB017** — Provisioned Throughput -
- [ ] **CB018** — Managed Compute - OS models on dedicated GPU capacity wo building an inference stack
- [ ] **CB019** — Deploy with managed compute [link](https://learn.microsoft.com/en-us/azure/foundry/how-to/deploy-models-managed?tabs=openai-entra&pivots=ai-foundry-portal)
- [ ] **CB023** — Deploy using code [link](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/create-model-deployments?pivots=programming-language-cli)
- [ ] **CB024** — Deployment types
- [ ] **CB025** — flex processing
- [ ] **CB026** — priority processing
- [ ] **CB030** — Foundry resource vs project vs hub (classic vs new Foundry); project endpoint shape; model catalogue (OpenAI, Anthropic Claude in Foundry, Mistral, Llama, Phi, DeepSeek), serverless vs managed compute deployments, Models-as-a-Service billing.
- [ ] **CB031** — Deployment types: Standard, Global Standard, Data Zone (EU/US), Provisioned (PTU), Global Batch; data residency implications of each — the FS client question.
- [ ] **CB032** — Quotas and limits: TPM/RPM per deployment, quota per region, how to request more, how APIM smooths it.
- [ ] **CB033** — Responses API vs Chat Completions; structured outputs; function/tool calling; prompt caching; reasoning models and their cost/latency profile; fine-tuning options and when not to.
- [ ] **CB038** — Anthropic SDK against Foundry — `anthropic` client with `base_url` at the Foundry `/anthropic` endpoint and Entra token; tool use and MCP connector; for clients choosing Claude in Foundry.
- [ ] **CB039** — Responses API [link](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses?tabs=python)
- [ ] **CB040** — ….all the tools under it — [source link unfinished; resolve before build]
- [ ] **CB041** — websockets mode
- [ ] **CB042** — tool search
- [ ] **CB043** — deep research
- [ ] **CB044** — ==multi-agent orchestration== [link](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses-multi-agent)
- [ ] **CB045** — predicted outputs
- [ ] **CB046** — prompt caching
- [ ] **CB047** — Decisions API [link](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/decisions?tabs=python)
- [ ] **CB048** — Webhooks [webhooks](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/webhooks?tabs=python-key)
- [ ] **CB049** — Client construction with `azure_endpoint`, `api_version`, `azure_ad_token_provider`; deployments vs model names; Responses API (`client.responses.create`, `previous_response_id`, tools, `text.format` for structured outputs) and Chat Completions legacy; streaming (`stream=True`, event types), tool calling loop (tool_calls → execute → return tool results → loop with max iterations), structured outputs with Pydantic (`client.beta.chat.completions.parse` / Responses `text_format`), prompt caching behaviour, `usage` accounting for cost, timeouts and `max_retries`, handling content-filter errors (`content_filter` finish reason, 400 with `content_filter_result`), batch API, embeddings.
- [ ] **CB050** — Exercise (your standing 45-minute drill): tool-calling loop with two tools, typed with Pydantic, structured final output, retries, token/cost tally, tests mocking the client. Then the same with streaming.
- [ ] **CB075** — `AIProjectClient(endpoint, credential)` with the project endpoint `https://<resource>.services.ai.azure.com/api/projects/<project>`; getting an OpenAI-compatible client from the project (`project_client.get_openai_client()` style accessor — check the 2.x name), connections (AI Search, Storage, Key Vault connections and how a tool resolves them), deployments listing, datasets and indexes, evaluations (create run, built-in evaluator ids, read results), agents: create agent with instructions and tools, threads/conversations, runs, polling vs streaming, run steps and tool call inspection, file search / AI Search / OpenAPI / Azure Function / MCP / Bing grounding tool definitions, connected agents, tracing enablement.
- [ ] **CB076** — Exercise: create an agent with an AI Search tool and an OpenAPI tool, run a thread, print each tool call and its result, attach an evaluation run on the transcript, tear down. Know which parts are preview.
- [ ] **CB121** — `SecretClient`, caching secrets at startup, rotation handling, Key Vault references in Container Apps / App Service, App Configuration feature flags for prompt/model toggles.
- [ ] **CB141** — `httpx` async clients with timeouts/limits, `pydantic` v2 models and settings (`pydantic-settings` for env/Key Vault), `FastAPI` (dependencies, background tasks, SSE streaming endpoint, health/readiness), `pytest` + `pytest-asyncio` + `respx`/mocks, `tenacity` or hand-rolled backoff, `uv`, `ruff`, `mypy --strict`, `pre-commit`, structured logging (`structlog`), Dockerfile (multi-stage, non-root, `uv` lockfile), GitHub Actions (OIDC login to Azure with `azure/login`, build and push to ACR, deploy to Container Apps, run evals), `.env` discipline, secrets never in code.
- [ ] **CB224** — Check current SDK/API names before each build: the sources mix threads/runs/connected agents with newer conversations/responses/agent versions. Do not implement legacy names just because they are preserved here.
- [ ] **CB225** — Re-check package versions, preview/GA status, model availability, CLI commands, and roles against the local documentation and official sources at build time.
- [ ] **CB227** — Resolve Source A's unfinished Responses “all tools” link and fine-tuning ellipsis. The empty EVALS checkbox is retained as an unfilled source slot.

- [ ] **TOP-GIT** — Git fundamentals and reproducible version-control exercise described above.

## Completion evidence

- [ ] Store the artifact path, reproducible command, observed outcome, limitations and next gap in the existing study log.
- [ ] Preserve current labs; link to shared concepts rather than importing another stage’s implementation.
- [ ] Do not label a sample, empty test collection or planned experiment as verified functionality.
