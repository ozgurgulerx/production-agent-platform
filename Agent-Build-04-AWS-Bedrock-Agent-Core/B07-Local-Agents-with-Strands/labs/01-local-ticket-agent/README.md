# 01 — The ticket agent on a local model, and the Runtime contract without AWS

Same Strands agent as B03 lab 01, different model constructor. The `bedrock` provider is there only to show the diff; the other two need no `.env`, no SSO, no credential.

## Prerequisites
- Ollama: `brew install ollama`, then `ollama serve` (or the app) and `ollama pull qwen3:8b` (about 5 GB, Q4_K_M, tool calling) or `ollama pull gpt-oss:20b` (about 13 GB, MXFP4, needs 16 GB RAM). `ollama show qwen3:8b` lists `tools` under capabilities. Tag quant defaults: verify on ollama.com before quoting.
- Shared venv plus the Ollama client: `source ../../../labs-setup/.venv/bin/activate && pip install "strands-agents[ollama]"`.
- Optional llama.cpp path: `brew install llama.cpp`, then `llama-server --jinja -hf Qwen/Qwen3-8B-GGUF --port 8080`.
- Optional AgentCore CLI 1.0 for `agentcore dev`: `npm install -g @aws/agentcore` (Node 20.12+).

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
python local_ticket_agent.py --provider ollama                 # default model qwen3:8b
python local_ticket_agent.py --provider ollama --model gpt-oss:20b
python local_ticket_agent.py --provider llamacpp               # llama-server on :8080
python local_ticket_agent.py --provider bedrock                # only with AWS_PROFILE + SSO; shows the one-line diff

python local_runtime_contract.py &                             # the B03 Runtime app on 0.0.0.0:8080, local model
bash curl_local.sh                                             # GET /ping, two POST /invocations with a session id
kill %1

bash gguf_quant.sh Qwen/Qwen3-8B                               # optional: HF -> GGUF -> Q4_K_M -> ollama create
```
`agentcore_dev_note.md` has the CLI 1.0 flow (`agentcore dev`, `agentcore dev "<prompt>"`, `agentcore invoke --local`).

## What to notice
- The only diff between providers is `make_model()`. Tools, prompt, the refusal and the Runtime app are shared.
- `qwen3:8b` will sometimes call `issue_refund` for 300 GBP. The tool refuses. That is the control that survives going local; the guardrail did not come with you.
- `curl` on 8080 is exactly what AgentCore Runtime does to your container. If `/ping` says `Healthy` and `/invocations` answers here, the zip in B03 lab 01 will work there.
- There is no guardrail, no identity, no trace, no policy. Compare the same three questions against `TICKET_AGENT_RUNTIME_ARN` with B03 `04-invoke-everything.py` when you have an account.

## Proof (checklist)
- [ ] three answers printed with `provider=ollama model=qwen3:8b` and the tool calls listed
- [ ] `issue_refund` 300 GBP returns `refused`, whatever the model wanted
- [ ] `curl_local.sh` prints `{"status":"Healthy"}` and two `/invocations` answers with the same session id
- [ ] optional: `ollama list` shows the `Q4_K_M` model built by `gguf_quant.sh`, and it answers the first question
- [ ] optional: `agentcore dev "What is the status of ticket T-1001?"` answers through the dev server

## Known gaps
macOS tested path only (Metal via Ollama). Nothing here has been run yet. Ollama tag quant defaults and the gpt-oss Bedrock model id are marked verify. `agentcore dev` flags are from the CLI 1.0 docs of 25 Oct 2026 and may move.
