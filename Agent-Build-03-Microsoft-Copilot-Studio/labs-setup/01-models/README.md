# 01 — Models: the dropdown, the retirement wave, consent, credits

There is no deployment to make. A Copilot Studio agent names a **primary model** from a curated dropdown, a separate model for deep reasoning and for generative responses, and each Prompt tool picks its own. Facts from the reading map section K (25 Oct 2026).

## 1. The primary model
Standard harness (K1): default **GPT Chat Latest**, which follows the current GPT chat snapshot. GA today: GPT-4.1, GPT-5 Chat, GPT-5.5 Chat, Claude Sonnet 4.6, Claude Opus 4.6 / 4.7 / 4.8. Preview: GPT-5 Reasoning, GPT-5 Auto, GPT-5.3 Chat. Experimental: Grok 4.2 (US early access). GitHub Copilot harness (K2) adds GPT-6 Astra, Claude Sonnet 5, Claude Fable 5 / 5.1, Claude Opus 5, tagged General / Auto / Deep.

## 2. The retirement wave
| Date | Retired | Replacement |
|---|---|---|
| 15 Oct 2026 | GPT-5.3 Chat, GPT-5.4 | GPT Chat Latest |
| 31 Oct 2026 | GPT-5.5 Chat | GPT Chat Latest |
| 12 Nov 2026 | GPT-4.1, GPT-4.1 Mini, GPT-5 Chat, GPT-5 Auto, GPT-5 Reasoning | GPT Chat Latest |
An agent pinned to a retired model is moved to GPT Chat Latest. Run the C05 test set before and after; version comparison shows the drift.

## 3. External providers
Anthropic runs as a Microsoft subprocessor; Mistral and xAI are hosted externally. Two admin switches (K3): accept the provider terms in the Microsoft 365 admin centre, and enable external models in PPAC (an environment-group rule in F2). Without both, the dropdown hides them.

## 4. Where your own model can go
Nowhere near the orchestrator. A Prompt tool can call a Foundry **chat-completions** deployment by endpoint and deployment name (K4; GPT-5 family excluded, Responses endpoints fail). C06 covers it, including the F06 fine-tuned deployment as the candidate (verify).

## 5. Credits by feature (K6)
Classic answer 1 · generative answer 2 · agent action (trigger, deep reasoning, topic transition, computer-use step) 5 · tenant graph grounding 10 · agent-flow actions 13 per 100 · AI tools basic 1 / standard 15 / premium 100 per 10 responses · voice 10–75 per minute. Enforcement: agents disabled at 125 % of prepaid, flows blocked at 100 %, per-agent monthly caps in PPAC.

## Run
```bash
source ../.venv/bin/activate
python read_primary_model.py      # after C03 lab 01: reads the agent row from Dataverse and prints the model setting
```

## Proof checklist
- [ ] `read_primary_model.py` prints the agent name and its configured primary model
- [ ] You can state the 12 Nov 2026 retirement list and what replaces it
- [ ] PPAC shows the external-models setting for the lab environment
