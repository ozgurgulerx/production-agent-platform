# B08 labs — the knowledge base as an agent capability

Runnable proof for the B08 chapter. Setup is shared: [`../../labs-setup/`](../../labs-setup/) (venv, `.env` at the track root). This lab builds on the B04 gateway and Cognito pool; run B04 labs 01 and 03 first.

```
labs/
└── 01-managed-knowledge-base/   S3 → Managed KB → ingestion → gateway target → Strands agent with citations; MemoryManager variant
```

| Lab | Chapter section | Creates | Time |
|---|---|---|---|
| 01 | §2 managed KB, §4 retrieval calls, §5 giving it to an agent | `ticket-policies-kb`, gateway target `TicketPolicies` | 1 session |

```bash
source ../../labs-setup/.venv/bin/activate
cd 01-managed-knowledge-base && python provision_kb.py
```
Every lab README ends with a proof checklist; tick it with real output only.
