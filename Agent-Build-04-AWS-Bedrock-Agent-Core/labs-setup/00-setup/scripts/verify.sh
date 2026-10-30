#!/usr/bin/env bash
# Prints OK when the account, CLI, venv and .env are ready for session 1. Read-only.
set -uo pipefail
here="$(cd "$(dirname "$0")/../../.." && pwd)"             # track root
venv="$here/labs-setup/.venv"
fail=0; ok(){ echo "  ok   $1"; }; bad(){ echo "  FAIL $1"; fail=1; }
[ -f "$here/.env" ] && ok ".env present" || bad ".env missing (cp .env.example .env)"
set -a; [ -f "$here/.env" ] && . "$here/.env"; set +a
[ -n "${AWS_REGION:-}" ] && ok "AWS_REGION=$AWS_REGION" || bad "AWS_REGION empty"
[ -n "${BEDROCK_MODEL_ID:-}" ] && ok "BEDROCK_MODEL_ID=$BEDROCK_MODEL_ID" || bad "BEDROCK_MODEL_ID empty"
prof=${AWS_PROFILE:+--profile $AWS_PROFILE}
command -v aws >/dev/null && ok "aws $(aws --version 2>&1 | cut -d' ' -f1)" || bad "aws CLI not installed (brew install awscli)"
if command -v aws >/dev/null; then
  arn=$(aws sts get-caller-identity $prof --query Arn --output text 2>/dev/null) && ok "caller $arn" || bad "sts get-caller-identity failed (aws sso login?)"
  case "$arn" in *":user/"*) bad "caller is an IAM user; use SSO/assumed role";; esac
  aws bedrock list-foundation-models $prof --region "${AWS_REGION:-us-east-1}" --query 'length(modelSummaries)' --output text >/dev/null 2>&1 && ok "bedrock reachable" || bad "bedrock list-foundation-models failed"
fi
command -v agentcore >/dev/null && ok "agentcore CLI $(agentcore --version 2>/dev/null | head -1)" || bad "agentcore CLI missing (npm i -g @aws/agentcore)"
"$venv/bin/python" -c "import bedrock_agentcore, strands, strands_evals, boto3; print('  ok   venv imports, boto3', boto3.__version__)" 2>/dev/null || bad "venv imports (run scripts/bootstrap_venv.sh)"
"$venv/bin/pip" show bedrock-agentcore-starter-toolkit >/dev/null 2>&1 && bad "deprecated starter toolkit installed in venv" || ok "no deprecated starter toolkit"
command -v docker >/dev/null && ok "docker present (B03 lab 02 only)" || echo "  note docker missing; only B03 lab 02 container deploy needs it"
[ $fail -eq 0 ] && echo OK || { echo "NOT READY"; exit 1; }
