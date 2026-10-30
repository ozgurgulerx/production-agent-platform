"""Shapes only, untested. The three Gateway target classes as `create_gateway_target(...)` kwargs.

Dumped from botocore 1.43.118 (`CreateGatewayTarget`) on 2026-10-25. Pass one of these dicts as **kwargs.
"""

TOOL_SCHEMA = [  # inline toolSchema for a Lambda MCP target; one entry per tool
    {
        "name": "get_ticket",
        "description": "Return one support ticket by id.",
        "inputSchema": {"type": "object", "properties": {"ticket_id": {"type": "string"}}, "required": ["ticket_id"]},
    },
    {
        "name": "issue_refund",
        "description": "Refund an amount in GBP against a ticket. Over 250 needs a human.",
        "inputSchema": {
            "type": "object",
            "properties": {"ticket_id": {"type": "string"}, "amount": {"type": "number"}, "reason": {"type": "string"}},
            "required": ["ticket_id", "amount"],
        },
    },
]

LAMBDA_MCP_TARGET = {  # class 1: MCP target, aggregated and searchable; the Gateway role invokes the Lambda
    "gatewayIdentifier": "<gatewayId>",
    "name": "tickets-lambda",
    "targetConfiguration": {"mcp": {"lambda": {"lambdaArn": "arn:aws:lambda:eu-west-2:123456789012:function:ticket-tools", "toolSchema": {"inlinePayload": TOOL_SCHEMA}}}},
    "credentialProviderConfigurations": [{"credentialProviderType": "GATEWAY_IAM_ROLE"}],
}

OPENAPI_OAUTH_TARGET = {  # class 1: MCP target from an OpenAPI document, outbound OAuth client-credentials
    "gatewayIdentifier": "<gatewayId>",
    "name": "tickets-api",
    "targetConfiguration": {"mcp": {"openApiSchema": {"s3": {"uri": "s3://<bucket>/openapi/tickets.yaml"}}}},
    "credentialProviderConfigurations": [
        {
            "credentialProviderType": "OAUTH",
            "credentialProvider": {
                "oauthCredentialProvider": {
                    "providerArn": "arn:aws:bedrock-agentcore:eu-west-2:123456789012:token-vault/default/oauth2credentialprovider/tickets-idp",
                    "scopes": ["tickets.read", "tickets.refund"],
                    "grantType": "CLIENT_CREDENTIALS",  # AUTHORIZATION_CODE for 3LO, TOKEN_EXCHANGE for OBO
                }
            },
        }
    ],
}

RUNTIME_HTTP_TARGET = {  # class 2: HTTP target; a Runtime agent becomes a tool at /<name>/invocations (GA Jul 2026)
    "gatewayIdentifier": "<gatewayId>",
    "name": "ticket-agent",
    "targetConfiguration": {"http": {"agentcoreRuntime": {"arn": "arn:aws:bedrock-agentcore:eu-west-2:123456789012:runtime/ticket_agent-abc123", "qualifier": "DEFAULT"}}},
    "credentialProviderConfigurations": [{"credentialProviderType": "CALLER_IAM_CREDENTIALS"}],  # or JWT_PASSTHROUGH
}

A2A_PASSTHROUGH_TARGET = {  # class 2: passthrough to any A2A endpoint, with session stickiness
    "gatewayIdentifier": "<gatewayId>",
    "name": "refund-specialist",
    "targetConfiguration": {
        "http": {
            "passthrough": {
                "endpoint": "https://bedrock-agentcore.eu-west-2.amazonaws.com/runtimes/<urlencoded-arn>/invocations",
                "protocolType": "A2A",
                "stickinessConfiguration": {"identifier": "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id", "timeout": 900},
            }
        }
    },
    "credentialProviderConfigurations": [{"credentialProviderType": "JWT_PASSTHROUGH"}],
}

INFERENCE_TARGET_NOTE = "class 3: targetConfiguration.inference.provider {endpoint, modelMapping, operations}; see reading map D5"
