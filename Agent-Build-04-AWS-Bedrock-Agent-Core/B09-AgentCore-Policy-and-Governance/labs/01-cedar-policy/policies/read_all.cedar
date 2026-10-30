permit(
  principal is AgentCore::OAuthUser,
  action in [
    AgentCore::Action::"TicketTools___get_ticket",
    AgentCore::Action::"TicketTools___list_tickets",
    AgentCore::Action::"TicketTools___get_policy"
  ],
  resource == AgentCore::Gateway::"<GATEWAY_ARN>"
);
