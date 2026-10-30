# Foundry IQ as a tool: reuse the F08 knowledge base from Copilot Studio

Portal walkthrough; there is no `pac` or REST surface for this on 25 Oct 2026 (J3). GitHub Copilot harness only, one knowledge base per agent, GA Sept 2026 (A8).

## Before you start

- F08 lab 01 ran: knowledge base `kb-ticket-policies` exists in your Foundry project on the Azure AI Search service, sources indexed, the three policy documents answerable (F08 proof checklist ticked).
- A GitHub-harness copy of the ticket agent exists (C03 lab 02). The Standard-harness agent from lab step 2 cannot use this tool; its only Azure AI Search path is the classic generative-answers node (J4).
- Decide the auth mode before opening the portal:

| Mode                  | Secret lives      | Per-user trimming                                                                      | Use when                                            |
| --------------------- | ----------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------- |
| Entra, signed-in user | nowhere           | yes, if the knowledge base's sources honour `x-ms-query-source-authorization` (F08 §5) | the UK bank case                                    |
| Service principal     | in the connection | no (one identity for everyone)                                                         | background agents                                   |
| Certificate           | in the connection | no                                                                                     | regulated tenants that forbid client secrets        |
| API key               | in the connection | no                                                                                     | never for production; fine for the first smoke test |

## Steps

1. Open the GitHub-harness agent → **Tools** → **Add a tool** → gallery → **Foundry IQ** (J3). If the gallery entry is missing, the environment is not on the GitHub harness or the admin has not enabled external knowledge for the environment group (F2).
2. Enter the Foundry project endpoint and the knowledge base name `kb-ticket-policies`. Pick the auth mode from the table. Name the tool "Ticket policies (Foundry IQ)" and write the description for the orchestrator: "UK card team refund, card and escalation policies, effective 1 Jul 2026. Use for any policy question."
3. Save. Note that the tool does not appear under Knowledge; it is a tool, with a tool's trace and a tool's credits (K6).
4. Test pane: ask the three questions from `_common.POLICY_QUESTIONS`. Open the **activity** panel for each turn: one retrieval call per question, with the documents it returned; for the Peru question the retrieval returns nothing usable and the agent refuses.
5. Go back to Foundry and change the knowledge base's `retrievalReasoningEffort` (F08 §3). Ask again. The Copilot Studio agent changes behaviour with no republish, which is the whole point: the retrieval intelligence lives in the knowledge base.

## What to record for the proof

- The auth mode you chose and why.
- The activity trace line for Q2 showing a retrieval from `card-policy.md`.
- The sentence: "One index in Foundry IQ now serves the Foundry agent (F08), the AgentCore agent would need its own Managed KB (B08), and the Copilot Studio agent calls it as a tool (C08)."

## If it does not work

- 401 from Foundry on first call: the Entra signed-in mode needs the user to have **Search Index Data Reader** on the Azure AI Search service, or the knowledge base must be reachable by the project identity (F08 role table).
- Tool present but never chosen: fix the description; the orchestrator picks tools by description the same way it filters knowledge sources (B1).
- "Only one Foundry IQ knowledge base per agent": remove the previous one; this is a documented limit (J3).
