"""Shape of CreateOnlineEvaluationConfig (bedrock-agentcore-control, boto3 1.43.118). Not run.

Every key below exists in the installed botocore model; values are illustrative.
Limits (docs, 2026-10-25): 25 evaluators, 5 filters, sessionTimeoutMinutes 1-60, sampling 0.01-100.
"""
ONLINE_EVAL_CONFIG = {
    "onlineEvaluationConfigName": "ticket-agent-online",
    "description": "10% of live sessions of the ticket agent, six built-ins",
    "rule": {
        "samplingConfig": {"samplingPercentage": 10.0},
        "filters": [  # optional, max 5; keys are span attributes
            {"key": "gen_ai.agent.name", "operator": "Equals", "value": {"stringValue": "ticket-agent"}},
        ],
        "sessionConfig": {"sessionTimeoutMinutes": 15},  # idle time after which a session is closed and scored
    },
    "dataSourceConfig": {
        "cloudWatchLogs": {
            "logGroupNames": ["/aws/bedrock-agentcore/runtimes/<agent_id>-DEFAULT"],
            # or "logGroupNamePrefixes": ["/aws/bedrock-agentcore/runtimes/"],
            # or "serviceNames": ["ticket-agent-lambda"],   # self-hosted agents writing OTel spans
        }
    },
    "evaluators": [
        {"evaluatorId": "Builtin.GoalSuccessRate"},        # SESSION
        {"evaluatorId": "Builtin.Correctness"},            # TRACE
        {"evaluatorId": "Builtin.Helpfulness"},            # TRACE
        {"evaluatorId": "Builtin.Refusal"},                # TRACE
        {"evaluatorId": "Builtin.ToolSelectionAccuracy"},  # TOOL_CALL
        {"evaluatorId": "Builtin.ToolParameterAccuracy"},  # TOOL_CALL
    ],
    "insights": [{"insightId": "Builtin.FailureAnalysis"}],  # verify: insight id vs evaluator id
    "outputConfig": {
        "cloudWatchConfig": {
            "resultDestination": "DEDICATED_LOG_GROUP",  # -> /aws/bedrock-agentcore/evaluations/results/<config-id>
            "metricsNamespace": "Bedrock-AgentCore/Evaluations",
        }
    },
    "evaluationExecutionRoleArn": "arn:aws:iam::<account>:role/agentcore-evals-exec",
    "enableOnCreate": True,
}

# Result event (OTel GenAI evaluation semconv), one per evaluator per target:
RESULT_EVENT_EXAMPLE = {
    "gen_ai.evaluation.name": "Builtin.ToolParameterAccuracy",
    "gen_ai.evaluation.score": 0.0,
    "gen_ai.evaluation.explanation": "issue_refund called with amount 400 > policy cap 250",
    "session.id": "…", "trace.id": "…", "span.id": "…",
}
