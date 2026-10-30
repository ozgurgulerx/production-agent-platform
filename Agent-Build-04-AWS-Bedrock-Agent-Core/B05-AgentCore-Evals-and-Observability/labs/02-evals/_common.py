"""Shared bits for the evals lab. IAM/SSO only; `.env` at the track root (walks up)."""
import json
import os
import re
import time
import uuid
from pathlib import Path

import boto3
from dotenv import load_dotenv

_TRACK_ROOT = Path(__file__).resolve().parents[3]   # track root, where .env lives (never walk up past it)
ENV_PATH = str(_TRACK_ROOT / ".env")
load_dotenv(ENV_PATH)
REGION = os.environ.get("AWS_REGION", "us-east-1")
PROFILE = os.environ.get("AWS_PROFILE") or None
MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "global.anthropic.claude-haiku-5-5")
JUDGE_MODEL_ID = os.environ.get("BEDROCK_JUDGE_MODEL_ID", "global.anthropic.claude-sonnet-5-5")
RUNTIME_ARN = os.environ.get("TICKET_AGENT_RUNTIME_ARN", "")
EVAL_ROLE_ARN = os.environ.get("AGENTCORE_EVAL_ROLE_ARN") or os.environ.get("AGENTCORE_RUNTIME_ROLE_ARN", "")
DATASET = Path(__file__).parent / "data" / "cases.jsonl"
EVALUATORS = ["Builtin.GoalSuccessRate", "Builtin.ToolSelectionAccuracy", "Builtin.ToolParameterAccuracy",
              "Builtin.Correctness", "Builtin.Helpfulness", "Builtin.Refusal"]


def session() -> boto3.Session:
    return boto3.Session(profile_name=PROFILE, region_name=REGION)


def control():
    return session().client("bedrock-agentcore-control")


def data():
    return session().client("bedrock-agentcore")


def agent_id() -> str:
    if not RUNTIME_ARN:
        raise SystemExit("set TICKET_AGENT_RUNTIME_ARN in .env (B03 lab 01) first")
    return RUNTIME_ARN.rsplit("/", 1)[-1]


def log_group(endpoint: str = "DEFAULT") -> str:
    return f"/aws/bedrock-agentcore/runtimes/{agent_id()}-{endpoint}"


def new_session_id() -> str:
    return f"b05-{uuid.uuid4()}-{int(time.time())}"      # runtimeSessionId must be >= 33 chars


def invoke(prompt: str, session_id: str) -> str:
    """One turn against the Runtime agent; returns the concatenated text (SSE or JSON)."""
    r = data().invoke_agent_runtime(agentRuntimeArn=RUNTIME_ARN, runtimeSessionId=session_id, qualifier="DEFAULT",
                                    contentType="application/json", accept="application/json",
                                    payload=json.dumps({"prompt": prompt}).encode())
    body = r["response"]
    if "text/event-stream" in r.get("contentType", ""):
        chunks = [line[6:] for line in body.iter_lines() if line.startswith(b"data: ")]
        return "".join(json.loads(c).get("text", c) if c.startswith("{") else c for c in map(bytes.decode, chunks))
    return body.read().decode()


def load_cases() -> list[dict]:
    return [json.loads(l) for l in DATASET.read_text().splitlines() if l.strip()]


def write_env(key: str, value: str) -> None:
    p = Path(ENV_PATH)
    text = p.read_text() if p.exists() else ""
    line = f"{key}={value}"
    text = re.sub(rf"^{key}=.*$", line, text, flags=re.M) if re.search(rf"^{key}=", text, flags=re.M) else text.rstrip("\n") + f"\n{line}\n"
    p.write_text(text)
    print(f".env <- {line}")


def print_results(results: list[dict]) -> None:
    for r in results:
        print(f"{r.get('evaluatorId','?'):34s} value={r.get('value')} label={r.get('label')}  {str(r.get('explanation',''))[:90]}")
