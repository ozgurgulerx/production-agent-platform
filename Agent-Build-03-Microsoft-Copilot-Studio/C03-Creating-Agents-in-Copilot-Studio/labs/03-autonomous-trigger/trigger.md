# Trigger configuration (B2)

- Connector trigger: Dataverse "When a row is added, modified or deleted"; scope Organization; table `Ticket`; change type Added.
- Message to the agent (the trigger payload becomes the first input):
  ```
  New ticket {TicketId} from {Customer} ({Country}). Amount {AmountGBP} GBP. {Description}
  Triage it with the ticket-triage steps, write a two-line summary and a priority back to the ticket row, and start the refund approval flow if a refund is requested.
  ```
- Credentials: maker (only option for triggers).
- Other triggers worth knowing: SharePoint file created (policy document updated → re-check knowledge), Recurrence (nightly sweep of P1 tickets), Planner task, Outlook email arrives (with the mailbox connector).

Same thing elsewhere: AgentCore Harness triggers / EventBridge; Foundry has no built-in trigger, use Logic Apps calling the agent.
