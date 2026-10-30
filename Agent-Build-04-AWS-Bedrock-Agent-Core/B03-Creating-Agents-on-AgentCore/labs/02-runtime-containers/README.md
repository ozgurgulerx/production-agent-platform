# 02 — Runtime from a container, on Instances, and self-hosted

Ways 3, 4 and 6 from lab 01's table. Lab 01 showed the Runtime as a zip; here the same `main.py` is a container (way 3), the same container could land on your EC2 capacity (way 4, described only), and the same Strands agent runs on Lambda with no AgentCore Runtime at all (way 6).

```
02-runtime-containers/
├── container-deploy/          Dockerfile (arm64, ADOT entrypoint), main.py, deploy.sh (ECR), create_runtime.py (containerConfiguration)
│   └── variants/              langgraph/ and openai-agents/ on the same /invocations contract
├── instances/                 capacity provider + capacityProviderConfiguration, 14-day sessions (described)
└── self-hosted-lambda/        handler.py + SAM template; becomes a Gateway HTTP target in B04 lab 06
```

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
cd container-deploy && AWS_ACCOUNT_ID=... ./deploy.sh --keep      # builds arm64, pushes to ECR, creates ticket_agent_container
python ../../01-ways-to-build/04-invoke-everything.py             # set TICKET_AGENT_RUNTIME_ARN to the container ARN to reuse it
cd ../self-hosted-lambda && sam build && sam deploy --guided        # way 6; note the FunctionUrl output for B04 lab 06
```
Variants are container-only (their dependencies are not in the shared venv); build them with the same Dockerfile by swapping `main.py` and `requirements.txt`.

## What it proves
- The artifact is the only difference between ways 2 and 3: `codeConfiguration` vs `containerConfiguration`. Ports, `/ping`, session header, versions, endpoints are identical.
- `opentelemetry-instrument` as the container entrypoint is what makes Strands spans appear in CloudWatch GenAI Observability without code changes (B05 lab 01).
- The framework inside the container is irrelevant to the Runtime (LangGraph, OpenAI Agents SDK, Strands).
- Self-hosted keeps the model and tools and loses the per-session microVM, identity injection and managed observability; B04 lab 06 shows how a Gateway target gives some of it back.

## Proof checklist
- [ ] `docker buildx build --platform linux/arm64` succeeds and the image is in ECR
- [ ] `create_runtime.py` prints `READY` and `.env` has `TICKET_AGENT_CONTAINER_RUNTIME_ARN`
- [ ] `04-invoke-everything.py` against the container ARN gives the same two-turn behaviour as the zip
- [ ] a trace for the container runtime appears under CloudWatch → GenAI Observability → Bedrock AgentCore
- [ ] `sam deploy` outputs a FunctionUrl and an IAM-signed `POST {"prompt": ...}` returns a result
