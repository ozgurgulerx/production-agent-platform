# Sketch: a Prompt tool on your own Foundry deployment (shape only, not run)

Source: reading map K4 (bring-your-own-model for prompts, 2026-07-14). Everything below is what the maker enters in the Prompt builder; there is no public API shape for it on Learn, so this is a form, not a payload.

| Field in the Prompt builder | Value for the ticket agent | Constraint (K4) |
|---|---|---|
| Model | "Bring your own model" | GA |
| Azure AI Foundry endpoint | `https://<resource>.openai.azure.com/` (the deployment's chat-completions base) | chat-completions deployment only; a Responses API endpoint fails |
| Deployment name | `ticket-tone-ft` (the F06 tuned `gpt-4.1-mini`) or any supported chat model | GPT-5 family not supported; fine-tuned deployments not mentioned on Learn, `verify` |
| Connection | Entra connection created by the maker | no keys typed into Copilot Studio |
| Prompt | "Draft the customer-facing refusal for ticket {{ticket}} citing policy {{policy_clause}} in house tone. Do not change the amount." | the rule stays in the tool / gateway, not in this text |
| Inputs | `ticket` (text), `policy_clause` (text) | |
| Output | text, or a JSON schema with `message` and `tone_score` | |

Where it sits in the agent: a tool the orchestrator calls after `issue_refund` has already refused; the Prompt tool never decides the refund.

What to measure (C05): a Custom grader "house tone" on the drafted message; General quality unchanged; Tool use still shows `issue_refund` before the prompt step.
