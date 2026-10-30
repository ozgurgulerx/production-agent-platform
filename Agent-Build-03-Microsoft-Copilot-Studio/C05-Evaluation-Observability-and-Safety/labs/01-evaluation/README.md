# 01 — Evaluate the ticket agent: portal first, then the REST API

Twelve cases, the same ones the Foundry and AgentCore tracks use. Each case names a **method**; refusal cases use **Custom** instructions plus a **Tool use** check so that a correct "no" is not punished by the General quality grader (chapter §3, reading map I1). You build the set once in the portal to see the methods, then create and run the same set from code so a pipeline can gate on it (I3).

Agent evaluation is GA (March 2026); the REST API is preview (April 2026).

## Prerequisites
`labs-setup/` done (`.env` with `TENANT_ID`, `CLIENT_ID`, `ENVIRONMENT_ID`, `AGENT_ID`); maker access to the agent; the app registration has the delegated Power Platform API permission and admin consent. Credits: every case is one generative answer (2 credits) plus grader work.

## Portal path (10 minutes)
1. Copilot Studio → the ticket agent → **Monitor** → **Evaluations** → **New test set** → import `data/testset.csv` using the portal template columns (map `method` and `custom_instructions`), or add the 12 cases by hand.
2. Run it. Open the `refund-cap` case: the Custom grader's reason should say it declined and escalated; the Tool use row should show `get_ticket` and no `issue_refund`.
3. Change the instructions to "always try to help with refunds", publish, run again, and **compare versions**. The refusal rows flip; that is the regression you will later catch in CI.

## Code path
```bash
source ../../../labs-setup/.venv/bin/activate
python create_testset.py --dry-run          # shows the POST body built from the CSV
python create_testset.py                    # device-code sign-in once; writes TESTSET_ID to .env
python run_and_poll.py --threshold 0.8      # starts a run, polls, prints per-case results, exit 1 under threshold
python run_and_poll.py --run-id <id>        # re-read an earlier run
```
Authenticated tools in a headless run: create a user profile in Monitor → Evaluations → settings, copy its id, pass `--connection <mcsConnectionId>`.

| File | What it proves |
|---|---|
| `data/testset.csv` | one method per row; refusals carry Custom + Tool use; the Peru case forbids `issue_refund` |
| `create_testset.py` | the set is a POST to `.../makerevaluation/testsets`; keys marked `verify` until the first real run |
| `run_and_poll.py` | a run is a POST, a poll and a read of `metricsResults`; the exit code is the gate |
| `custom_grader.md` | the exact grader text and why General quality fails on refusals |
| `multi_turn_set.md` | the ≤20-case conversational set for the clarifying-question flows |
| `compare_versions.md` | prove a change before you publish it |
| `copilot_agent_kit.md` | plan validation over Direct Line and the Pipelines quality gate |
| `.github-workflow-snippet.yml` | OIDC → token → `run_and_poll.py`; no secrets |

## Proof checklist
- [ ] Portal run: `refund-cap` and `peru-card` pass on Custom and Tool use; `status` passes General quality
- [ ] `create_testset.py` returns an id and `.env` has `TESTSET_ID`
- [ ] `run_and_poll.py` prints 12 cases with scores and exits 0 at threshold 0.8
- [ ] After the "always help with refunds" edit, the same command exits 1 and names the failing cases
- [ ] You can say in one sentence why General quality is the wrong method for a refusal
