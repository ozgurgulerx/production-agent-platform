# 01 — Model deployments: pick, deploy, prove

Every lab in F03, F04 and F05 assumes four deployments exist in the project: a chat model, a reasoning model, an embedding model and a realtime voice model. This lab creates them reproducibly and teaches the three decisions behind each one: which model, which deployment type, which name.

Why deploy at all rather than call a public assistant: the deployment runs inside your tenant, prompts are not used to train anyone's model, and you control the version, the guardrails, the quota and the parameters. A deployment is also the only thing an agent can point at: `PromptAgentDefinition(model=...)` takes a **deployment name**, not a model name.

## 1. Choose the model

Four questions, in this order, with the ticket agent as the worked example:

| Question | Ticket agent answer | `.env` key |
|---|---|---|
| Task: chat, reasoning, embedding, realtime audio, vision? | short support answers with tool calls → a small chat model | `FOUNDRY_MODEL=gpt-5-mini` |
| Does one step need to think longer? | triage of ambiguous tickets → same model, higher `reasoning.effort` | `FOUNDRY_REASONING_MODEL=gpt-5-mini` |
| Memory or retrieval? | memory store in F03 lab 04 → embeddings | `FOUNDRY_EMBEDDING_MODEL=text-embedding-3-small` |
| Voice? | F03 lab 01 way 3 → realtime model | `FOUNDRY_VOICE_MODEL=gpt-realtime` |

Then compare candidates on the portal **leaderboards** (preview, page dated 2026-08-28). The four axes and what they actually measure:

- **Quality index** 0–1: mean of accuracy scores (`exact_match`, `pass@1`, `arena_hard`) over eight datasets (MMLU-Pro, GPQA, BigBench-Hard, MBPP+, MuSR, ChemBench, FrontierScience, τ²-telecom). Higher is better.
- **Safety**: HarmBench attack success rate, lower is better; plus WMDP (higher is worse) and Toxigen F1 (higher is better). Measured with Foundry Guardrails **off**, so it is the bare model.
- **Cost**: USD to run the quality datasets with real input, reasoning and output tokens. The "estimated cost" column still uses a 3:1 input:output blend; the two are not the same number.
- **Performance**: 14-day aggregate, 800-in/200-out prompts, streaming, East US. Read P90 latency and time-to-first-token for a chat agent, generated tokens per second for long outputs.

Rule of thumb for an agent: pick the smallest model whose quality index clears your eval threshold (F05), then buy latency and cost with it. Compare `gpt-5.2` against `gpt-5.2-chat` against `gpt-5.2-codex` on the Compare page before trusting a suffix.

## 2. Choose the deployment type

Deployment types apply to serverless (pay-per-token or PTU) deployments; they decide **where inference runs** and **how you pay** (Learn, 2026-08-12). Data at rest always stays in the Azure geography.

| SKU name (CLI / Bicep) | Inference runs | Billing | Pick when |
|---|---|---|---|
| `GlobalStandard` | any Azure region | per token | default; launches first, highest default quota, cheapest |
| `DataZoneStandard` | within the data zone (US, EU, APAC) | per token | EU/US data-processing boundary required |
| `Standard` | within the Azure geography | per token | strict geography, low volume |
| `GlobalProvisionedManaged` / `DataZoneProvisionedManaged` / `ProvisionedManaged` | as above | reserved PTU | predictable high throughput, latency SLA |
| `GlobalBatch` / `DataZoneBatch` | as above | 50 % discount, 24 h target | offline eval and bulk jobs (own enqueued-token quota) |
| `DeveloperTier` | any region | per token | evaluating a fine-tuned model only; 24 h lifetime, no SLA |

Interview line: Global means the request may be served anywhere; Data Zone fences processing to a continent; Standard fences it to the geography. None of them move your data at rest.

**Model router** (deploy like any model, version `2025-11-18`, Global Standard or Data Zone Standard only): routes each request across OpenAI, Anthropic, xAI, DeepSeek, Meta and others in `Balanced`, `Quality` or `Cost` mode, with failover on by default. Claude targets must be deployed separately first. Use it when quality per cost across a mixed workload matters more than a fixed model name in traces.

## 3. Deploy

```bash
source ../.venv/bin/activate          # from labs-setup/01-models
bash deploy_models.sh                 # reads ../../.env; creates the four deployments if missing
python smoke_test.py                  # Entra-only call to each deployment through /openai/v1
```

What the script does, and the CLI you should recognise (`az cognitiveservices account deployment create`, GA, page dated 2026-09-25):

```bash
az cognitiveservices account list-models -n "$FOUNDRY_ACCOUNT_NAME" -g "$AZ_RESOURCE_GROUP" \
  --query "[?name=='gpt-5-mini'].{name:name,format:format,version:version,sku:skus[0].name}" -o table

az cognitiveservices account deployment create -n "$FOUNDRY_ACCOUNT_NAME" -g "$AZ_RESOURCE_GROUP" \
  --deployment-name gpt-5-mini --model-name gpt-5-mini --model-version "<version from list-models>" \
  --model-format OpenAI --sku-name GlobalStandard --sku-capacity 50
```

`--sku-capacity` is thousands of tokens per minute for pay-per-token SKUs and PTUs for provisioned ones. `--model-format` is `OpenAI` for Azure OpenAI models and the publisher name (`Microsoft`, `Meta`, `DeepSeek`, ...) for other Foundry Models. `deployments.bicep` is the same four deployments as infrastructure, for F02 step 3; `main.bicepparam` holds the names.

Deployment name versus model name: the agent, the SDK and the traces all use the **deployment name**. Keep it equal to the model name unless you run two versions side by side (`gpt-5-mini` and `gpt-5-mini-next`), which is how you A/B a model upgrade without touching agent code.

## 4. Call it, Entra only

The book-style sample with `api_key=` is what you will see everywhere; this repo never does that. The OpenAI client speaks to `https://<account>.openai.azure.com/openai/v1/` with a bearer token for `https://cognitiveservices.azure.com/.default`:

```python
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI
token = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
client = OpenAI(base_url=f"https://{account}.openai.azure.com/openai/v1/", api_key=token)
r = client.responses.create(model="gpt-5-mini", input="One sentence: what is a deployment type?")
```

Use the Responses API, as every agent in F03 does; Chat Completions still works and is what older samples show. Playground changes to instructions and parameters are not saved anywhere; they become durable only when you create a prompt agent (F03 way 1).

## Proof (checklist)
- [ ] `az cognitiveservices account deployment list` shows the four deployments with `GlobalStandard`
- [ ] `smoke_test.py` prints one line per deployment, no key in `.env`
- [ ] you can say which SKU you would pick for an EU bank's ticket agent and why (`DataZoneStandard`, EU zone)

## Not covered here
Quota increase requests, PTU sizing and spillover (`--spillover-deployment-name`), fine-tuning deployments, managed-compute (GPU) deployments for Hugging Face models, and Instant Access (preview) which calls a model without a deployment. The Learn how-to for Bicep model deployment returned 404 on 2026-10-25; the resource shape in `deployments.bicep` follows the `Microsoft.CognitiveServices/accounts/deployments` API that the CLI wraps.

## Next
`../../F05-Creating-Agents/labs/01-seven-ways/`
