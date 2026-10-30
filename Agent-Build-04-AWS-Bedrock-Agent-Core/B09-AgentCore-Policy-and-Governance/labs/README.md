# B09 labs — put the rule where the model cannot reach it

Runnable proofs for the B09 chapter. Setup is shared: [`../../labs-setup/`](../../labs-setup/) (venv, `.env` at the track root). These labs assume the gateway from B04 lab 03 exists (`TICKET_GATEWAY_ID`, `TICKET_GATEWAY_URL`, target `TicketTools`) and the Cognito pool from B04 lab 01 (`COGNITO_*`). Nothing here has run against AWS yet; every proof checklist is unticked.

```
labs/
├── 01-cedar-policy/            engine → attach LOG_ONLY → two policies → exercise → ENFORCE → NL-to-Cedar → temporal
├── 02-guardrails-in-policy/    PromptAttack + SensitiveInformation on the refund reason, at the gateway
└── 03-org-controls/            execution role, resource policy, SCPs, CloudTrail audit, PrivateLink notes
```

| Lab | Chapter section | Creates | Time |
|---|---|---|---|
| 01 | §2, §3 | policy engine, two or three policies, gateway association | 1 session |
| 02 | §4 | one policy with a guardrails clause, role permission | 30 min |
| 03 | §5, §6 | nothing by default (prints documents); `--apply` creates the role and resource policy | 30 min |

```bash
source ../../labs-setup/.venv/bin/activate
cd 01-cedar-policy && python 01_create_engine.py
```

Cleanup: every script accepts `--cleanup`; run `05_enforce.py --cleanup` last so the gateway is left without an engine. Policy pricing is per authorisation, so leaving the engine attached costs nothing while idle.
