# 01 — Models: access, inference profiles, service tiers, routing

The decisions behind `BEDROCK_MODEL_ID`. On Foundry you pick a model, a deployment type and a capacity; on Bedrock there is no deployment object for foundation models. You pick a **model**, the **inference profile** that decides where it may run, and a **service tier** that decides price and priority, then you invoke. Facts from the reading map, section L (25 Oct 2026).

## 1. Access
Most models are enabled on first invoke when your principal has `aws-marketplace:Subscribe` and `aws-marketplace:ViewSubscriptions`. Anthropic models need a one-time use-case form per account: console → Bedrock → Model access, or `PutUseCaseForModelAccess`. `gpt-oss` has no Marketplace product. GovCloud still uses the Model access page. To **block** a model for everyone, deny `bedrock:InvokeModel` on its ARN in an SCP (B09 lab 03). `model_access.py` checks what your account can invoke today.

## 2. Inference profiles, not bare model ids
| Prefix | Routes to | Use when |
|---|---|---|
| none (`anthropic.claude-...`) | this Region only | residency rule names one Region; not offered for new Claude models |
| `us.` / `eu.` / `au.` / `jp.` | a geography | residency rule names a geography; most quota headroom |
| `global.` | any commercial Region | latency and availability first; data may leave the geography |
New Claude models (Haiku 5.5 on 7 Oct 2026) are geo/global only. `.env` holds `global.anthropic.claude-haiku-5-5` by default; change it to `eu.` for the UK bank scenario and say so in the review.

## 3. Service tiers and batch
`service_tier` on Converse / InvokeModel: `priority` (+75 %), `default`, `flex` (−50 %), `reserved`; batch inference ≈ −50 %. Support is per model: Nova 2 Lite has Priority and Flex, the Claude Haiku 5.5 card lists Standard only. Strands exposes it as `BedrockModel(service_tier=...)`.

## 4. Intelligent Prompt Routing
Default routers (Nova, Llama) and configured routers via `CreatePromptRouter` with `responseQualityDifference`; USD 1 per 1,000 requests; English only; not available for Nova 2 Lite or Claude 5.5. The Foundry analogue is the model router deployment. On AgentCore the newer answer is a **Gateway inference target** with fallback and circuit breaker (reading map D8), so routing lives next to the tools.

## 5. The second endpoint
`bedrock-mantle` serves OpenAI- and Anthropic-native APIs (chat completions, Responses, Messages) in addition to Converse. Harness model configs expose this as `apiFormat: converse_stream | responses | chat_completions`.

## Run
```bash
source ../.venv/bin/activate
python model_access.py          # which of the four models in .env your account can call
python smoke_test.py            # one Converse call with SigV4 through BEDROCK_MODEL_ID; prints id, tier, latency
```

## Proof checklist
- [ ] `model_access.py` shows `BEDROCK_MODEL_ID` as invokable, or prints the use-case-form step
- [ ] `smoke_test.py` prints an answer and `inferenceProfile=global...` (or `eu.` if you changed it)
- [ ] You can say in one sentence why the UK bank case uses `eu.` and what it costs in headroom
