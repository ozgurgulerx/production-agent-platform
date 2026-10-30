# C06 labs — model choice, prompt tools, credits

One lab. Setup is shared: [`../../labs-setup/`](../../labs-setup/) (venv, `.env` at the track root, device-code app registration, `pac`). It assumes the ticket agent from C03 lab 01 (`AGENT_ID`, `AGENT_SCHEMA_NAME` in `.env`) and the C05 lab 01 test set (`TESTSET_ID`).

```
labs/
└── 01-models-and-prompts/   switch the primary model and measure it; read the setting from Dataverse; a Prompt tool on your own Foundry deployment; deep reasoning; credits arithmetic
```

| Lab | Chapter section | Creates | Time |
|---|---|---|---|
| 01 | §2 primary model, §3 prompt tools, §4 credits, §5 eval loop | nothing permanent (one Prompt tool, removed at the end) | half a session |

```bash
source ../../labs-setup/.venv/bin/activate
cd 01-models-and-prompts && python credits_estimate.py --answers 3 --tool-calls 1 --conversations 40000
```
