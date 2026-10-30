# F06 labs — Fine-tuning

Shared setup: [`../../labs-setup/`](../../labs-setup/). Assumes F03 lab 01 (base agent) and F05 lab 02 (eval) exist; reads F08 lab 01's policy documents.

```
labs/
└── 01-sft-ticket-tone/   generate + review 60 SFT rows, train gpt-4.1-mini (Developer), deploy 24 h, eval tuned vs base
```

| Lab | Chapter section | Needs |
|---|---|---|
| 01 | §3 data, §4 cost, §5 job and eval loop | a fine-tunable region; ~1 hour wall clock |
