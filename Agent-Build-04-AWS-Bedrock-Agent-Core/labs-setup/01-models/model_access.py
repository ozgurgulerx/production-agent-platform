"""Show which of the models named in .env this account can invoke, and the Anthropic use-case-form status.

Proves: access is per model and per account; a bare model id and an inference profile are different
objects (ListInferenceProfiles vs ListFoundationModels).
"""
import os
from pathlib import Path
import boto3
from dotenv import load_dotenv

_TRACK_ROOT = Path(__file__).resolve().parents[2]   # track root, where .env lives (never walk up past it)
load_dotenv(str(_TRACK_ROOT / ".env"))
sess = boto3.Session(profile_name=os.getenv("AWS_PROFILE") or None, region_name=os.getenv("AWS_REGION", "us-east-1"))
br = sess.client("bedrock")

profiles = {p["inferenceProfileId"]: p for page in br.get_paginator("list_inference_profiles").paginate() for p in page["inferenceProfileSummaries"]}
models = {m["modelId"]: m for m in br.list_foundation_models()["modelSummaries"]}
wanted = [os.getenv(k) for k in ("BEDROCK_MODEL_ID", "BEDROCK_JUDGE_MODEL_ID", "BEDROCK_FT_BASE_MODEL_ID") if os.getenv(k)]
for mid in wanted:
    if mid in profiles:
        p = profiles[mid]
        print(f"profile  {mid:55} status={p['status']} type={p['type']} regions={len(p.get('models', []))}")
    elif mid in models:
        m = models[mid]
        print(f"model    {mid:55} lifecycle={m.get('modelLifecycle', {}).get('status')} inference={m.get('inferenceTypesSupported')}")
    else:
        print(f"unknown  {mid:55} not in ListInferenceProfiles or ListFoundationModels for this region")
try:
    u = br.get_use_case_for_model_access()
    print("Anthropic use-case form: submitted" if u.get("formData") else "Anthropic use-case form: NOT submitted (PutUseCaseForModelAccess)")
except Exception as e:   # noqa: BLE001
    print("use-case form check:", type(e).__name__, "(submit via console → Model access if Anthropic calls fail)")
