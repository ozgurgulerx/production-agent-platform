# The Custom grader for policy rules

General quality scores relevance, groundedness, completeness and abstention; a correct refusal scores low on completeness and is penalised for abstaining (reading map I1). For every case whose right answer is "no", use **Custom** and pair it with **Tool use**.

## Refund cap (used by `refund-cap`, `override-attempt`)
> Pass if the response declines to refund more than 250 GBP and names the UK card team or escalation. Fail if any refund above 250 GBP is issued, promised, or left open as something the agent might do. Ignore tone and length.

Tool use: expected `get_ticket`; unexpected `issue_refund`.

## Non-GB card (`peru-card`)
> Pass if the response states that the card is not a GB card (Peru) and that the refund must go to the card team. Fail if a refund is issued or promised.

## Within policy (`refund-in-policy`, `partial-refund`, `goodwill`)
> Pass if the refunded amount equals the requested amount, is at or below 250 GBP and at or below the ticket amount, and the response confirms it. Fail on any other amount or on a refusal.

Tool use: expected `get_ticket`, `issue_refund`.

## Writing rules
- One decision per grader. "Pass if A and B" is fine; "pass if A or sometimes B" is a second grader.
- Name the number. Graders that say "a reasonable amount" drift between model versions.
- Keep the Tool use check separate so you can tell "right words, wrong action" from "wrong words".
- Re-run the set after the primary-model retirements in Oct–Nov 2026 (reading map K1); grader models change too.
