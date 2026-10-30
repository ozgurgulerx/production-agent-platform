# C08 labs — ground the ticket agent, three ways, and watch the citations

Runnable proof for the C08 chapter. Setup is shared: do [`../../labs-setup/`](../../labs-setup/) first (venv, `.env` at the track root, `verify.sh` printing OK, the public-client app registration with Graph and Power Platform API delegated scopes). The ticket agent from C03 lab 01 must exist (`AGENT_SCHEMA_NAME`, `ENVIRONMENT_ID` in `.env`).

```
labs/
└── 01-knowledge/      SharePoint library from Graph → connector source vs upload source → three questions with citations → Foundry IQ tool on the GitHub-harness copy → memory note
```

| Lab | Chapter section | Creates                                                                                                                        | Time      |
| --- | --------------- | ------------------------------------------------------------------------------------------------------------------------------ | --------- |
| 01  | §1–§6           | a `Policies` library with three files; two knowledge sources on the ticket agent; a Foundry IQ tool on the GitHub-harness copy | 1 session |

```bash
source ../../labs-setup/.venv/bin/activate
cd 01-knowledge && python upload_policies.py
```

Next chapter: [`../../C09-Governance-and-Agent-365/labs/`](../../C09-Governance-and-Agent-365/labs/), where the knowledge connectors you just used meet DLP.
