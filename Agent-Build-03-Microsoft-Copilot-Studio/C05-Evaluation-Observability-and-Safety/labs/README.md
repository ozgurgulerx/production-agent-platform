# C05 labs — score the agent, read its spans, guard its tool calls

Runnable proofs for the C05 chapter. Setup is shared: do [`../../labs-setup/`](../../labs-setup/) first (venv, `.env` at the track root, `verify.sh` printing OK) and have C03 lab 01 done so `AGENT_ID` and `AGENT_SCHEMA_NAME` exist. Each lab README ends with a **proof checklist**; a lab is done when the boxes are ticked with real output.

```
labs/
├── 01-evaluation/     a 12-case test set in the portal, then the same set created and run through the REST API; Kit notes; CI snippet
├── 02-observability/  environment-level App Insights export, three KQL queries, transcripts read from Dataverse, Monitor and Purview tours
└── 03-safety/         moderation levels, an XPIA test document, a bring-your-own-protection webhook that blocks refunds above 250 GBP
```

| Lab | Chapter section | Creates | Time |
|---|---|---|---|
| 01 | §2–§5, §8 | one test set, test runs (credits: each case is a generative answer plus grader) | 1 session |
| 02 | §6 | an App Insights export setting (PPAC), nothing else | 45 min |
| 03 | §7 | a webhook (local or Container Apps) and an environment protection setting | 45 min |

Run them in order. Lab 01 needs a maker on the agent; lab 02 needs a **Managed Environment** and Power Platform admin for the export; lab 03 needs environment admin to register the webhook.

```bash
source ../../labs-setup/.venv/bin/activate
cd 01-evaluation && python create_testset.py && python run_and_poll.py --threshold 0.8
```

Nothing here has run against a tenant yet (written 25 Oct 2026). Next chapter: [`../../C09-Governance-and-Agent-365/labs/`](../../C09-Governance-and-Agent-365/labs/).
