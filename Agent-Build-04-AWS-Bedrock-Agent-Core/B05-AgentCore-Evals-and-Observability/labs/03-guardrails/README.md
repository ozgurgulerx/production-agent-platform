# 03 — Runtime guardrails: on the model, on the tool, at the gateway

Evals grade yesterday; guardrails act now. One Bedrock guardrail, three attachment points, and the demonstration that the second point is not optional.

| Step | Script | What it proves |
|---|---|---|
| 1 | `create_guardrail.py` | one resource: PROMPT_ATTACK + harm filters, a denied topic, PII anonymise, contextual grounding; Standard tier via a cross-Region profile; a frozen version |
| 2 | `agent_with_guardrail.py` | `BedrockModel(guardrail_id, guardrail_version, guardrail_trace="enabled", guardrail_redact_output=True)`: a normal turn, a blocked prompt attack, a blocked topic |
| 3 | `tool_output_guardrail.py` | `--no-hook` leaks a card number from a tool result; the `AfterToolCallEvent` hook with `ApplyGuardrail(source=OUTPUT)` anonymises it |
| 4 | `bridge_to_policy.md` | the same two rules as Cedar `when guardrails { ... }` for B09 |

```bash
source ../../../labs-setup/.venv/bin/activate
python create_guardrail.py            # --classic if Standard tier is not available in your region
python agent_with_guardrail.py
python tool_output_guardrail.py --no-hook && python tool_output_guardrail.py
python create_guardrail.py --cleanup
```

## Notes
- `guardrail_trace="enabled"` puts the assessment (which policy, which filter, strength) in the Converse response and in the span; keep it on in non-prod.
- Automated Reasoning checks (`automatedReasoningPolicyConfig`) need a policy built from a rule document first (bedrock `CreateAutomatedReasoningPolicy`); out of scope here, named in the chapter.
- There is no AWS-native red-team service for agents. `strands_evals.redteam` (`AdversarialCaseGenerator`, `CrescendoStrategy`, `GoatStrategy`, `AttackSuccessEvaluator`) runs locally against the same agent; a 10-case run is a good addition to lab 02 step 6.
- Pricing per 1K text units: content filters and denied topics $0.15, PII and grounding $0.10, Automated Reasoning $0.17 per policy; both tiers the same.

## Proof (checklist)
- [ ] step 1 prints a guardrail id and version `1`; `.env` updated
- [ ] step 2: prompt 2 returns the blocked-input message; prompt 3 is blocked by `financial-advice`
- [ ] step 3: `--no-hook` output contains `4111`; hooked run prints `[hook] get_ticket -> GUARDRAIL_INTERVENED` and no card number
- [ ] cleanup run, guardrail gone from `aws bedrock list-guardrails`
