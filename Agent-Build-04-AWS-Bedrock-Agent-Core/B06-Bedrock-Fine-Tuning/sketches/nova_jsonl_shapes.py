"""Untested sketch. The training-data and job shapes side by side. Runnable: ../labs/01-sft-ticket-tone/."""

# SFT, one line per conversation (reading map K5)
SFT_NOVA = {
    "schemaVersion": "bedrock-conversation-2024",
    "system": [{"text": "UK card team support assistant. Warm, brief, British English, no exclamation marks."}],
    "messages": [
        {"role": "user", "content": [{"text": "Can I get £300 back on ticket 1042?"}]},
        {"role": "assistant", "content": [{"text": "I can't approve that myself: refunds above £250 need a second "
                                                   "approver. I've flagged it; you'll hear back within 4 business hours."}]},
    ],
}

# Same row in OpenAI chat JSONL for the bedrock-mantle Files + Fine-tuning APIs (gpt-oss-20b, Qwen3-32B; K4)
SFT_MANTLE = {"messages": [
    {"role": "system", "content": "UK card team support assistant."},
    {"role": "user", "content": "Can I get £300 back on ticket 1042?"},
    {"role": "assistant", "content": "I can't approve that myself: above £250 needs a second approver."},
]}

# RFT: prompt-only rows plus a grader. The reward comes from a Lambda (or a judge model) the job calls per sample (K1, K3).
RFT_ROW = {"schemaVersion": "bedrock-conversation-2024",
           "messages": [{"role": "user", "content": [{"text": "Can I get £300 back on ticket 1042?"}]}],
           "metadata": {"must_mention": "second approver"}}          # verify: reference-field name for the grader
RFT_JOB_CONFIG = {
    "customizationType": "REINFORCEMENT_FINE_TUNING",
    "customizationConfig": {"rftConfig": {
        "graderConfig": {"lambdaGrader": {"lambdaArn": "arn:aws:lambda:us-east-1:123456789012:function:ticket-tone-grader"}},
        "hyperParameters": {"epochCount": 2, "trainingSamplePerPrompt": 4, "reasoningEffort": "low"}}},   # typed ints, not strings
}


def lambda_grader_stub(event, _context):
    """Reward in [0,1]: 1 if the sample mentions the approver rule without inventing an amount."""
    sample = event["sample"]["output_text"]                  # verify: event envelope of the RFT Lambda grader
    ok = "second approver" in sample.lower() and "£300" not in sample
    return {"score": 1.0 if ok else 0.0}


# Distillation: the teacher answers your prompts, the student (e.g. Nova 2 Lite) is trained on them (K1)
DISTILLATION_JOB_CONFIG = {
    "customizationType": "DISTILLATION",
    "customizationConfig": {"distillationConfig": {"teacherModelConfig": {
        "teacherModelIdentifier": "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-2-pro-v1:0",   # verify id
        "maxResponseLengthForInference": 512}}},
}

# What Bedrock does NOT have: a DPO / preference job. Foundry's {"input", "preferred_output", "non_preferred_output"}
# has no Bedrock counterpart on 25 Oct 2026 (K1). Encode the preference in an RFT judge or in the B05 custom evaluator.
