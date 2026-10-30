// Cedar shapes for the ticket gateway. Schema facts from the AgentCore Policy scope page (F1), fetched 2026-10-25.
// Replace <GATEWAY_ARN> with arn:aws:bedrock-agentcore:<region>:<account>:gateway/<id>.

// 1. Read tools for every authenticated OAuth user. No wildcards exist, so the actions are listed.
permit(
  principal is AgentCore::OAuthUser,
  action in [
    AgentCore::Action::"TicketTools___get_ticket",
    AgentCore::Action::"TicketTools___list_tickets",
    AgentCore::Action::"TicketTools___get_policy"
  ],
  resource == AgentCore::Gateway::"<GATEWAY_ARN>"
);

// 2. Refund up to 250 GBP for the support group. The group claim path on the principal is not
// verified (# verify); the amount check uses the tool argument as typed in the target schema.
permit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"TicketTools___issue_refund",
  resource == AgentCore::Gateway::"<GATEWAY_ARN>"
) when {
  context.input.amount_gbp <= 250 &&
  principal.groups.contains("support")   // # verify attribute name
};

// 3. Temporal rule: at most three refunds per user in 24 hours. This is a Dogwood (session-aware)
// policy, max 20 per engine, 24-hour window. Syntax not fetched. # verify
// dogwood: limit principal on AgentCore::Action::"TicketTools___issue_refund" to 3 per 24h;

// 4. Guardrails in policy (GA 17 Jun 2026): content filter on get_policy output, suppress instead of deny.
// Clause grammar from the page summary. # verify
permit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"TicketTools___get_policy",
  resource == AgentCore::Gateway::"<GATEWAY_ARN>"
) when guardrails {
  BedrockGuardrails::ContentFilter(["HATE", "INSULTS"], [output])
} suppressOutput;

// 5. The nightly reconciliation job runs with an IAM role and may only list tickets.
permit(
  principal == AgentCore::IamEntity::"arn:aws:iam::123456789012:role/ticket-reconcile",
  action == AgentCore::Action::"TicketTools___list_tickets",
  resource == AgentCore::Gateway::"<GATEWAY_ARN>"
);
