# B06 labs — fine-tune the ticket agent's tone, then prove it

Runnable proof for the B06 chapter. Setup is shared: [`../../labs-setup/`](../../labs-setup/) (venv, `.env` at the track root, `verify.sh` printing OK). Each lab README ends with a **proof checklist**; a lab is done when the boxes are ticked with real output.

```
labs/
└── 01-sft-ticket-tone/    ~60 Nova JSONL rows from the policy documents → SFT job on Nova 2 Lite → on-demand deployment → base vs tuned eval
```

| Lab | Chapter section | Creates | Time |
|---|---|---|---|
| 01 | §3 data, §4 job, §5 serving, §6 eval loop | custom model `ticket-tone-nova2lite`, one custom model deployment | 1 session + job wait |

```bash
source ../../labs-setup/.venv/bin/activate
cd 01-sft-ticket-tone && python make_dataset.py
```
