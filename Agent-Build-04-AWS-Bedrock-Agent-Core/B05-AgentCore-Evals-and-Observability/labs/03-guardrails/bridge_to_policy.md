# The same rule at the gateway: Guardrails-in-Policy (hand-off to B09)

What `tool_output_guardrail.py` does in one process, AgentCore Policy does for every agent behind a Gateway (GA 17 Jun 2026; 7 regions; the gateway role needs `bedrock:InvokeGuardrailChecks`). The guardrail is referenced from a Cedar policy and evaluated on tool inputs and outputs; `suppressOutput` withholds a response.

```cedar
// deny get_ticket results that contain sensitive information (shape per the Guardrails-in-Policy page, # verify exact syntax)
forbid(
  principal,
  action == AgentCore::Action::"TicketTools___get_ticket",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-1:123456789012:gateway/ticket-gateway"
)
when guardrails {
  BedrockGuardrails::SensitiveInformation(["CREDIT_DEBIT_CARD_NUMBER"], [context.output])
};

// block prompt attacks arriving as tool arguments
forbid(
  principal,
  action == AgentCore::Action::"TicketTools___issue_refund",
  resource
)
when guardrails {
  BedrockGuardrails::PromptAttack([context.input.reason])
};
```

| Where | Sees | Owner |
| --- | --- | --- |
| `BedrockModel(guardrail_id=...)` | user turn, model answer | agent code (this lab) |
| `AfterToolCallEvent` hook + `ApplyGuardrail` | tool arguments and results, in-process | agent code (this lab) |
| Cedar `when guardrails { ... }` on the Gateway | tool inputs and outputs for every agent, outside agent code, `LOG_ONLY` first | platform team (B09 lab 02) |

Rule to keep: the model guardrail sees the model's turn only; put a second check where the tools are.
