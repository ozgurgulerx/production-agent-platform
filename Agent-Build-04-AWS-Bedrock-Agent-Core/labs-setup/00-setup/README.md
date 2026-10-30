# 00 — Setup: account, tooling, venv, execution role

Nothing in this track has run against AWS yet (25 Oct 2026). This page is the exact list of what an account needs before session 1. Tick the proof checklist with real output.

## Account prerequisites
1. **An AWS account with IAM Identity Center (SSO)** and a permission set for you that includes `BedrockAgentCoreFullAccess`, `AmazonBedrockFullAccess`, IAM role creation, Lambda, S3, ECR, CloudWatch, X-Ray, Cognito and CloudTrail read. In production you would narrow this; B09 lab 03 shows why `BedrockAgentCoreFullAccess` is too wide (it grants `GetWorkloadAccessTokenForUserId`).
2. **Region**: `us-east-1` or `us-west-2`. Evaluations (9 regions), Policy (13), Harness and Guardrails-in-Policy (7) all include both; Runtime V2 is in 5 regions. Stay in one region for the whole track.
3. **Model access**: most models are enabled on first invoke if your principal has `aws-marketplace:Subscribe`. Anthropic models need the one-time use-case form (`PutUseCaseForModelAccess`). `labs-setup/01-models/README.md` walks through it.
4. **CloudWatch Transaction Search** enabled once per account/region (B05 lab 01 does it; it is a prerequisite for GenAI Observability and for Evaluations to find spans).
5. **A Cognito user pool** for the JWT labs (B04 lab 01 creates it from code).
6. **S3 bucket** for direct-code-deploy zips and datasets (`CODE_BUCKET` in `.env`; create it with `aws s3 mb`).

## Local tooling
```bash
brew install awscli node                 # aws CLI v2; Node 20.12+
npm install -g @aws/agentcore            # AgentCore CLI 1.0.0 (22 Oct 2026)
agentcore --version
pip uninstall -y bedrock-agentcore-starter-toolkit   # if present: deprecated and shadows the new binary
docker --version                          # only for B03 lab 02 container deploy (buildx, linux/arm64)
```
The CLI stores project config in `agentcore/agentcore.json` and deploys through a thin CDK app; the labs use it for the "CLI twin" of each boto3 script and never as the only path.

## Python environment
```bash
bash scripts/bootstrap_venv.sh            # labs-setup/.venv, python3.13, requirements.txt pinned on 25 Oct 2026
source ../.venv/bin/activate
```
To regenerate the API ground truth the labs were written against (operation names, input shapes, SDK signatures):
```bash
python - <<'EOF2'
import boto3; c=boto3.client("bedrock-agentcore-control", region_name="us-east-1")
print(sorted(c.meta.service_model.operation_names))
EOF2
```

## Execution role for Runtime
Runtime needs a role that `bedrock-agentcore.amazonaws.com` can assume, scoped with `aws:SourceAccount` and `aws:SourceArn`, and that can pull from ECR, write logs and X-Ray, call `bedrock:InvokeModel*`, and mint workload tokens. `scripts/create_execution_role.py` creates `agentcore-ticket-runtime-role` and writes `AGENTCORE_RUNTIME_ROLE_ARN` to `.env`. B09 lab 03 prints the least-privilege version and the diff.

## Verify
```bash
bash scripts/verify.sh
```
Checks: `.env` present with region and model id; `aws sts get-caller-identity` works with the profile; `bedrock list-foundation-models` returns; `agentcore --version` is 1.x; venv imports `bedrock_agentcore`, `strands`, `strands_evals`; Docker optional.

## Proof checklist
- [ ] `verify.sh` prints `OK`
- [ ] `aws sts get-caller-identity` shows the SSO role, not an IAM user with keys
- [ ] `AGENTCORE_RUNTIME_ROLE_ARN` in `.env` and `aws iam get-role` shows the `SourceArn` condition
- [ ] `python ../01-models/smoke_test.py` prints one answer and the inference-profile id it used
