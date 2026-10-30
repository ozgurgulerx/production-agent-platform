# `agentcore dev`: the Runtime contract with hot reload (AgentCore CLI 1.0, 22 Oct 2026)

The Node CLI replaced the Python starter toolkit; `agentcore launch --local` and `.bedrock_agentcore.yaml` are gone (reading map C1, L2). The local loop is now:

```bash
npm install -g @aws/agentcore                     # Node 20.12+
agentcore create --template agent-python-strands  # or point it at this folder's local_runtime_contract.py (verify: --entrypoint flag name)
agentcore dev                                     # uvicorn + hot reload on the entrypoint; Docker only for container templates
agentcore dev "What is the status of ticket T-1001?"
agentcore dev --mode browser                      # Agent Inspector UI
agentcore invoke --local --runtime <name> '{"prompt": "Refund 300 GBP on ticket T-1003."}'   # verify exact payload flag
```

Config lives in `agentcore/agentcore.json` (resources) and `.env.local` (secrets for local runs). With `--provider ollama` in the entrypoint nothing reaches AWS; the CLI itself may still read your AWS profile for `status`.

What `agentcore dev` does not give you: Guardrails, Identity, Gateway, Policy, Observability. It gives you the contract. The deployed twin is `agentcore deploy` (thin CDK), covered in B03 §2 and B02.
