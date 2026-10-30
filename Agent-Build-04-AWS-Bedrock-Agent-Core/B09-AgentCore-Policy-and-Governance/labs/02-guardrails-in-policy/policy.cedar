// Guardrails in policy (GA 17 Jun 2026, F3). Clause grammar from the fetched page summary. # verify
// Refund reasons are customer-supplied text: check them for prompt attacks and PII before the Lambda sees them.
permit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"TicketTools___issue_refund",
  resource == AgentCore::Gateway::"<GATEWAY_ARN>"
) when guardrails {
  BedrockGuardrails::PromptAttack([context.input.reason]) &&
  BedrockGuardrails::SensitiveInformation(["EMAIL", "PHONE", "UK_NATIONAL_INSURANCE_NUMBER"], [context.input.reason])
};

// Policy documents are returned to the model: filter the output instead of denying the call.
permit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"TicketTools___get_policy",
  resource == AgentCore::Gateway::"<GATEWAY_ARN>"
) when guardrails {
  BedrockGuardrails::ContentFilter(["HATE", "INSULTS", "MISCONDUCT"], [output])
} suppressOutput;
