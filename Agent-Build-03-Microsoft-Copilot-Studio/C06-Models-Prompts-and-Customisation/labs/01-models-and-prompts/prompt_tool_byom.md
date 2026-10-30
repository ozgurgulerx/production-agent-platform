# A Prompt tool on your own Foundry deployment

Reading map K4 (2026-07-14, GA). The only door through which a model you control, including a fine-tuned one, enters a Copilot Studio agent.

## Prerequisites
- A Foundry **chat-completions** deployment in a resource you can reach: endpoint `https://<resource>.openai.azure.com/`, deployment name in `.env` as `FOUNDRY_PROMPT_DEPLOYMENT`. Candidates: a plain `gpt-4.1-mini`, or the F06 tuned deployment (fine-tuned deployments are not mentioned on K4; `verify` by trying).
- Not a GPT-5 family deployment; not a Responses API endpoint (both fail, K4).
- Your maker account has `Cognitive Services OpenAI User` on the Foundry resource (Entra connection; no key is typed anywhere).

## Steps
1. Agent → Tools → Add a tool → **New prompt**.
2. In the Prompt builder, Model → **Bring your own model**; enter the endpoint and `FOUNDRY_PROMPT_DEPLOYMENT`; create the connection when asked (signed-in identity).
3. Prompt text: "Draft the customer-facing refusal for ticket {{ticket}} citing {{policy_clause}} in house tone. Do not change the amount." Inputs `ticket`, `policy_clause`. Output: text.
4. Test in the builder with a ticket id and clause; then add to the agent and describe when to use it: "after a refund is refused, to word the reply".
5. Instructions: add one line so the orchestrator calls `issue_refund` first and the prompt second.
6. Measure (C05): Custom grader "house tone" on the drafted message; Tool use still lists `issue_refund`.
7. Remove the tool at the end of the lab unless the test set says keep it.

## Failure you should see once
Point the prompt at a Responses-API deployment or a `gpt-5-mini`: the builder's test fails. Read the error, then switch to the supported deployment. That is the K4 restriction, not an auth problem.
