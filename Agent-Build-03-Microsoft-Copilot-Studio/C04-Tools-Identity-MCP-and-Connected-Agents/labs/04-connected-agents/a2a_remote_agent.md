# Add an A2A remote agent (reading map B3, GA April 2026)

Any agent that serves an A2A card works. Two candidates from the other tracks: the AWS track's `ticket_refund_a2a` runtime (card at the Runtime's `/invocations/.well-known/agent-card.json` with a bearer token; `TICKET_A2A_CARD_URL` in that track's `.env`), or the Foundry F04 lab 06 A2A endpoint.

1. Agents → Add → **A2A agent**. Paste the card URL. Auth: **None** for a public card, **API key** or **OAuth 2.0** for protected ones (the AWS card needs the Cognito bearer: use OAuth 2.0 manual with the Cognito endpoints, or front it with a Gateway `authorizerType: NONE` for the demo only).
2. The dialog reads the card and lists the skills (`Issue refund`). Description for routing: "Refund decisions for UK card tickets."
3. Test: "Refund 100 pounds on 1042" → the plan routes to the remote agent; the AWS Runtime log shows the call.

Transport is JSON-RPC over HTTPS; streaming depends on the card's `capabilities`.
