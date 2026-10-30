# 01 — Model choice, prompt tools and credits on the ticket agent

The agent from C03 lab 01, measured across a primary-model switch, given one Prompt tool on a Foundry deployment you control, and priced in credits. Nothing is trained; the point is to see where the behaviour levers are and to prove every change with the C05 test set.

## Prerequisites
- Shared setup done (`labs-setup/00-setup`): venv, `.env` with `TENANT_ID`, `CLIENT_ID`, `ENVIRONMENT_URL`, `AGENT_ID` or `AGENT_SCHEMA_NAME`; the device-code app registration has Dynamics CRM `user_impersonation`.
- C05 lab 01 done (`TESTSET_ID` in `.env`) so the model switch has a judge.
- For the Prompt tool: a Foundry chat-completions deployment name in `FOUNDRY_PROMPT_DEPLOYMENT` (optional; the F06 tuned deployment is the candidate, marked verify).
- For Claude in the dropdown: an admin accepted the external-model terms (M365 admin centre) and enabled "external models" for this environment (PPAC) (K3, F2).

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
python credits_estimate.py --answers 3 --tool-calls 1 --conversations 40000            # cost of the session as designed
python credits_estimate.py --answers 3 --grounding --deep-reasoning 1 --conversations 40000   # same session with the two expensive switches
python read_model_setting.py            # the bot row in Dataverse; where the model setting lives (column names verify)
# then the portal walkthroughs, in order:
#   primary_model.md       switch to Claude Sonnet 4.6, run the test set twice, compare, decide
#   prompt_tool_byom.md    Prompt tool on FOUNDRY_PROMPT_DEPLOYMENT; see the Responses/GPT-5 failure once
#   deep_reasoning.md      enable, trigger with `reason`, price it, decide
```

## What each piece proves
- **credits_estimate** the budget is credits per feature; tenant graph grounding (10) and deep reasoning (5 per turn) dominate the model choice.
- **read_model_setting** the model is a configuration value on the `bot` row, read-only here; the code-first write path is `pac copilot push` (C07).
- **primary_model** a model switch is an experiment with two test-run ids and a decision, not a settings change.
- **prompt_tool_byom** the one place your own deployment enters; the restrictions (chat completions, no GPT-5) are product rules, not auth errors.
- **deep_reasoning** a per-turn action you enable for a step, priced before you enable it.

## Proof (checklist)
- [ ] `credits_estimate.py` output for the designed session pasted; packs per month stated
- [ ] `read_model_setting.py` prints the bot row; the model-related fields found (or the note that they live on a botcomponent) recorded
- [ ] two test-run ids (`TESTRUN_BASE`, `TESTRUN_CANDIDATE`) and the keep/revert decision written here; Tool use unchanged across models
- [ ] Prompt tool created on `FOUNDRY_PROMPT_DEPLOYMENT`, one house-tone draft produced in the builder, the Responses/GPT-5 failure seen once, tool removed or kept with a reason
- [ ] deep reasoning enabled, triggered once, priced, and switched back off (or a C05 case recorded that needs it)

## Known gaps
No API writes the primary model; the lab reads it and changes it in the portal. Fine-tuned deployments behind BYOM are not confirmed on Learn (K4). The Dataverse column names in `read_model_setting.py` carry `# verify`. Nothing here has run yet.
