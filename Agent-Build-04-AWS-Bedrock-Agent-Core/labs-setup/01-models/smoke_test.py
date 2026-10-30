"""One Converse call through the inference profile in .env, signed with SigV4 from the SSO profile.

Proves: model access works without any key; the id you use is a profile, not a bare model id;
service_tier is a request-level choice. Prints model id, stop reason, tokens and latency.
"""
import os, time
import boto3
from dotenv import load_dotenv

_TRACK_ROOT = Path(__file__).resolve().parents[2]   # track root, where .env lives (never walk up past it)
load_dotenv(str(_TRACK_ROOT / ".env"))
sess = boto3.Session(profile_name=os.getenv("AWS_PROFILE") or None, region_name=os.getenv("AWS_REGION", "us-east-1"))
rt = sess.client("bedrock-runtime")
model = os.environ["BEDROCK_MODEL_ID"]

t0 = time.time()
kwargs = dict(modelId=model,
              system=[{"text": "You are the support assistant of a UK card issuer. Answer in one sentence."}],
              messages=[{"role": "user", "content": [{"text": "A customer was charged twice for one purchase. What do you do first?"}]}],
              inferenceConfig={"maxTokens": 120, "temperature": 0.2})
tier = os.getenv("BEDROCK_SERVICE_TIER")        # priority | default | flex; omit to use the model's default
if tier:
    kwargs["serviceTier"] = {"type": tier}       # Converse.serviceTier.type, verified against boto3 1.43.118
r = rt.converse(**kwargs)
dt = time.time() - t0
print("inferenceProfile=", model)
print("answer:", r["output"]["message"]["content"][0]["text"])
print("stop:", r["stopReason"], "| tokens in/out:", r["usage"]["inputTokens"], r["usage"]["outputTokens"], f"| {dt:.2f}s")
