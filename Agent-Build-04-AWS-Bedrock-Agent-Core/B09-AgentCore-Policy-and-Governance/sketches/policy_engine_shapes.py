"""Shape-only: the four calls that put a Cedar policy in front of the ticket gateway.
Keys verified against boto3 1.43.118 on 2026-10-25 (bedrock-agentcore-control). Not run."""

CREATE_POLICY_ENGINE = {
    "name": "ticket-policy-engine",
    "description": "Cedar rules for TicketTools",
    # "encryptionKeyArn": "arn:aws:kms:...",      optional CMK
    "tags": {"track": "B09"},
}
# -> policyEngineId, policyEngineArn, status

ATTACH_TO_GATEWAY = {            # UpdateGateway requires name, roleArn, authorizerType again
    "gatewayIdentifier": "<gateway id>",
    "name": "<existing name>",
    "roleArn": "<existing role>",
    "authorizerType": "CUSTOM_JWT",
    "authorizerConfiguration": {"customJWTAuthorizer": {"discoveryUrl": "...", "allowedClients": ["..."]}},
    "policyEngineConfiguration": {"arn": "<policyEngineArn>", "mode": "LOG_ONLY"},   # LOG_ONLY | ENFORCE
    "exceptionLevel": "DEBUG",   # denial bodies carry the reason
}

CREATE_POLICY = {
    "policyEngineId": "<policyEngineId>",
    "name": "refund-cap-250",
    "definition": {"cedar": {"statement": open("cedar_examples.cedar").read() if False else "permit(...);"}},
    "validationMode": "FAIL_ON_ANY_FINDINGS",   # | IGNORE_ALL_FINDINGS
    "enforcementMode": "ACTIVE",                # | LOG_ONLY (per policy, inside an enforcing engine)
}

START_POLICY_GENERATION = {
    "policyEngineId": "<policyEngineId>",
    "name": "refund-rule-from-text",
    "resource": {"arn": "<gatewayArn>"},
    "content": {"rawText": "Support agents may refund up to 250 GBP on tickets they own."},
}
# -> policyGenerationId; GetPolicyGeneration.status; ListPolicyGenerationAssets ->
#    [{policyGenerationAssetId, definition.cedar.statement, rawTextFragment,
#      findings: [{type: VALID|INVALID|NOT_TRANSLATABLE|ALLOW_ALL|ALLOW_NONE|DENY_ALL|DENY_NONE, description}]}]
# Attach by reference:
CREATE_POLICY_FROM_GENERATION = {
    "policyEngineId": "<policyEngineId>",
    "name": "refund-rule-generated",
    "definition": {"policyGeneration": {"policyGenerationId": "<id>", "policyGenerationAssetId": "<asset id>"}},
    "validationMode": "FAIL_ON_ANY_FINDINGS",
    "enforcementMode": "LOG_ONLY",
}
