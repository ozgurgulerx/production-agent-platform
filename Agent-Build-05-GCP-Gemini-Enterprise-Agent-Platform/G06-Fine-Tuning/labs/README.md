# G06 labs — Fine-tuning

Shared setup: [`../../labs-setup/`](../../labs-setup/). Assumes the G03 lab 01 `ticket-agent` exists and G05 lab 02 wrote its evalset. Needs a Cloud Storage bucket the tuning job on `eu` can read (map G2; `TUNING_BUCKET` in `.env`, falls back to `AGENT_RUNTIME_STAGING_BUCKET`).

Status on 25 Oct 2026: scaffold only, functionality unverified.

```
labs/
└── 01-sft-ticket-tone/
    ├── README.md                 goal, steps, proof checklist, cleanup
    ├── agent.py                  ticket-agent-tuned: same ADK agent, model = tuned endpoint path (map G9)
    ├── make_dataset.py           100-row tone dataset from a template; TODO(learner) fills the generator
    ├── submit_sft.py             upload to GCS, client.tunings.tune on eu, poll, print endpoint (map G4)
    ├── requirements.txt          pins from ../../labs-setup/requirements.txt
    ├── test_sft_ticket_tone.py   pytest skeleton, TODO(learner)
    └── data/                     train.jsonl, validation.jsonl (written by make_dataset.py, gitignored)
```

| Lab | Chapter section                       | Creates                                                                                              | Time                                                     |
| --- | ------------------------------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 01  | §3 data, §4 job, §5 ADK, §7 eval loop | `data/*.jsonl`, a tuning job on `eu`, a tuned endpoint, `ticket-agent-tuned`, two `adk eval` reports | ~1 to 2 hours wall clock, most of it waiting for the job |

## Run order

1. `make_dataset.py`, then read every row.
2. `submit_sft.py`, wait for the endpoint.
3. `adk eval` twice (base, tuned) on the G05 lab 02 evalset; paste both results into the lab README.

Next chapter: [G07 — Local and edge](../../G07-Local-and-Edge/), where the same agent runs on Gemma 4 with no cloud at all.
