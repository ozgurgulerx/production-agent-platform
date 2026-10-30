# Deep reasoning: when one turn is worth 5 credits

Reading map B9 (2026-08-28, preview) and K6 (credits).

- Enable: Settings → Generative AI → **Deep reasoning** (Standard harness; US and EU regions only). The turn runs on Azure OpenAI o3 when the user says `reason` or the instructions ask for it.
- Billing: each deep-reasoning turn is an **agent action**, 5 credits, in addition to the generative answer (2). A reasoning model used inside an AI tool bills as premium, 10 credits per 1,000 tokens.
- GitHub harness: reasoning is the "Deep" tag on the model itself (GPT-6 Astra, Claude Fable 5.1), billed by usage (K2, K5).

Lab step: enable it, ask the test pane a refund question with `reason` in front, read the plan in the activity map, then run `python credits_estimate.py --answers 3 --deep-reasoning 1 --conversations 40000` and compare with `--deep-reasoning 0`. Then turn it off unless a C05 case needs it: a Custom grader on multi-step policy questions is the honest test.
