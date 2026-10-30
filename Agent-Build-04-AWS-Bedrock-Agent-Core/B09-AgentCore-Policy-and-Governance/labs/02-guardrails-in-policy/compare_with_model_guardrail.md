# Model guardrail (B05 lab 03) vs guardrail in policy (this lab)

Same Bedrock Guardrail capabilities, two different places. Fill the right column after both labs have run.

| Case | B05 lab 03: `BedrockModel(guardrail_id=…)` + Strands hook `ApplyGuardrail` on tool I/O | This lab: `when guardrails {…}` on the gateway |
|---|---|---|
| Prompt attack typed by the user in chat | caught at model input (before the model sees it) | not seen (never becomes a tool argument) |
| Prompt attack smuggled into `issue_refund.reason` by the model or a retrieved document | caught only if your hook runs on tool input, and only in your process | caught for every caller of the gateway, including other agents and scripts |
| PII in a tool argument | same as above | caught at the boundary; the Lambda never logs it |
| Harmful text returned by `get_policy` | hook on tool output, if present | `suppressOutput` redacts before the response reaches the model |
| Agent runs outside your code (Harness, partner agent, batch job) | no coverage | covered: the control is on the gateway |
| Cost | guardrail units on every model turn | guardrail units only on governed tool calls |

Record here which rows each lab actually proved: ______
