# G02 labs — SDKs and automated deployment

Shared setup: [`../../labs-setup/`](../../labs-setup/README.md) (venv, pins, `.env` at the track root). Assumes the G01 project is ready (roles from I6, staging bucket in region). The agent code is the S03 `ticket-agent`; G03 lab 02 deploys it by hand first, this lab puts the same deploy behind a pipeline. Facts cite [`../../reference/reading-map-gcp-agents-2026-10-25.md`](../../reference/reading-map-gcp-agents-2026-10-25.md).

```
labs/
└── 01-deploy-pipeline/
    ├── README.md                   goal, steps, proof checklist, cleanup
    ├── agent.py                    ticket-agent ADK definition (TODO(learner) tool bodies)
    ├── requirements.txt            pinned from labs-setup/requirements.txt
    ├── .agent_engine_config.json   identity_type AGENT_IDENTITY, staging bucket, env
    ├── cloudbuild.yaml             build → eval gate (placeholder) → deploy → traffic 10/90 → promote
    ├── test_01_deploy_pipeline.py  pytest skeletons, TODO(learner)
    └── terraform/                  main.tf + variables.tf variant of the deploy step (plan only)
```

| Lab | Chapter section                                                               | Creates                                                                                                                                | Time                         |
| --- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| 01  | §2 adk deploy, §3 SDK, §4 Terraform, §5 Cloud Build, §6 revisions and traffic | a Cloud Build trigger (or manual `gcloud builds submit`), one new revision of `ticket-agent`, a 10/90 split, then promote or roll back | 60 to 90 min plus build time |

## Run order

1. `source ../../labs-setup/.venv/bin/activate` from the track root; `bash labs-setup/00-setup/scripts/verify.sh` prints `OK`.
2. `AGENT_RUNTIME_RESOURCE` in `.env` is set (G03 lab 02) or the first `deploy` step creates it by display name.
3. Follow [`01-deploy-pipeline/README.md`](01-deploy-pipeline/README.md).

Next chapter: [G03 — Creating agents](../../G03-Creating-Agents/README.md).

Status on 25 Oct 2026: scaffold only, functionality unverified.
