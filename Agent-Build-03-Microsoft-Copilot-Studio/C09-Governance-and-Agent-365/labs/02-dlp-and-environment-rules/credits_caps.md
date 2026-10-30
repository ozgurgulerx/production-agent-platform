# Credits: caps before a trigger empties the pool (K5, K6)

- Unit: **Copilot Credits** since 1 Sep 2025 (was "messages", same quantities). Prepaid packs (25,000 per pack per month), pay-as-you-go through an Azure billing policy, or one-year prepurchase.
- Rates that bite on the ticket agent: generative answer 2; agent action (trigger, deep reasoning, topic transition, computer-use step) 5; tenant graph grounding 10; agent-flow actions 13 per 100; prompt tools 1 / 15 / 100 per 10 responses.
- Enforcement: agents are **disabled at 125 %** of prepaid capacity; agent flows blocked at 100 %. M365 Copilot-licensed users are not charged in B2E scenarios.

Do:
1. PPAC → Licensing → Copilot Studio → consumption report: find the ticket agent's monthly usage.
2. Set a **per-agent monthly cap** for the autonomous agent from C03 lab 03 (triggers bill 5 each). Set an alert at 80 % of the pack.
3. In the environment group: **Copilot credit draw from tenant pool** = capped.

Revert: caps are safe to leave. Unverified: USD 0.01 per credit PAYG (third-party figure; K7).
