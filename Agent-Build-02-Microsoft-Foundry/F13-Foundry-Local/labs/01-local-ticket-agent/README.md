# 01 — The ticket agent on Foundry Local

Same Agent Framework agent as F03 way 4, different `ChatClient`. No Azure, no `.env`, no credential.

## Prerequisites
- Foundry Local: `brew tap microsoft/foundrylocal && brew install foundrylocal` (macOS) or `winget install Microsoft.FoundryLocal`; `foundry --version`. CLI is preview.
- Shared venv plus `pip install foundry-local-sdk` (pinned in `labs-setup/requirements.txt`; Windows: `foundry-local-sdk-winml`).
- 8 GB RAM minimum; the 0.5B Qwen model is ~500 MB, `phi-4-mini` several GB.

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
foundry model list --device gpu          # what your silicon can run; omit --device for everything
python local_ticket_agent.py             # qwen2.5-0.5b: fast, weak at tool calls
python local_ticket_agent.py phi-4-mini  # better tool use, slower
bash olive_optimize.sh                   # optional: your own INT4 model into the cache
```

## What to notice
- The port comes from `manager.urls[0]`. `foundry server status` shows it when you use the CLI server instead.
- The 0.5B model will probably call `issue_refund` for 300 GBP anyway. The policy refusal lives in the tool, which is the right place regardless of model size; smaller models make that lesson louder.
- There is no guardrail, no identity and no trace. Compare with the same three questions against `ticket-agent-prompt` in F03 lab 01.

## Proof (checklist)
- [ ] three answers printed with the local endpoint and model id shown
- [ ] `foundry model list --cached` shows the downloaded variant and its execution provider
- [ ] optional: `foundry cache list` shows `qwen2.5-local` after Olive, and it answers the first question

## Known gaps
macOS only tested path (WebGPU/CPU). NPU variants and Windows ML untested. Responses API on the local server unverified; the client uses Chat Completions. Nothing here has been run yet.
