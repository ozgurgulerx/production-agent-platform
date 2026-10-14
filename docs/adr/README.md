# Architecture decision records

One file per decision a reviewer would challenge. Numbered, never edited after acceptance — a reversal is a new ADR that supersedes the old one.

File name: `NNN-short-title.md`. Template:

```
# ADR-NNN: <decision in one line>

Date: YYYY-MM-DD · Status: proposed | accepted | superseded by ADR-MMM

## Context
What forced the decision: the constraint, the number, the failure.

## Options considered
1. … — cost / risk / what it would have given us
2. …

## Decision
What we chose, in two sentences.

## Consequences
What becomes easier, what becomes harder, what we will measure to know if it was right.
```

Index:

| # | Decision | Status |
|---|---|---|
| 001 | stdio transport for the Stage 3a server; Streamable HTTP deferred to the Azure stage | proposed |
