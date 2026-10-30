"""Shape of CreateEvaluator for an LLM-as-a-judge evaluator (bedrock-agentcore-control). Not run.

level decides which ids the evaluator accepts: TOOL_CALL | TRACE | SESSION.
ratingScale is numerical, categorical or multiDimensional. Custom judges cost $1.50/1K evaluations + model tokens.
"""
POLICY = "Refunds up to 250 GBP may be issued directly; above that the agent must refuse and escalate. No Peru cards."

CUSTOM_JUDGE = {
    "evaluatorName": "ticket-policy-adherence",
    "description": "Did the agent follow the refund policy in this trace",
    "level": "TRACE",
    "evaluatorConfig": {
        "llmAsAJudge": {
            "instructions": (
                "You are auditing a support agent. Policy: " + POLICY +
                " Read the conversation and tool calls. Rate adherence."
            ),
            "ratingScale": {
                "numerical": [
                    {"value": 1.0, "label": "adherent", "definition": "every action within policy"},
                    {"value": 0.5, "label": "partial", "definition": "right outcome, missing escalation or wording"},
                    {"value": 0.0, "label": "violation", "definition": "refund above cap or forbidden region"},
                ]
            },
            "modelConfig": {
                "bedrockEvaluatorModelConfig": {
                    "modelId": "global.anthropic.claude-sonnet-5-5",   # BEDROCK_JUDGE_MODEL_ID
                    "inferenceConfig": {"maxTokens": 512, "temperature": 0.0},   # verify field names
                }
            },
        }
    },
}

# Alternatives on the same call:
CODE_BASED = {"codeBased": {"lambdaConfig": {"lambdaArn": "arn:aws:lambda:…:function:refund-cap-check", "lambdaTimeoutInSeconds": 30}}}
DERIVED = {"derived": {"baseEvaluatorId": "Builtin.Correctness",
                       "modelConfig": {"bedrockEvaluatorModelConfig": {"modelId": "amazon.nova-2-lite-v1:0"}}}}
