permit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"TicketTools___issue_refund",
  resource == AgentCore::Gateway::"<GATEWAY_ARN>"
) when { context.input.amount_gbp <= 250 };
