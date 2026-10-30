# 02 — DLP, environment rules, credits

Reach control in three admin objects: a DLP policy (blocks a connector, which blocks every MCP and REST tool on it, which disables publish), an environment group (rules travel with the group), and credit caps (so an autonomous trigger cannot disable every agent at 125 %).

## Start with the failure
A maker adds an MCP server on a Friday. It works in the test pane and in Teams. Nothing asked anyone. After this lab, the same action ends with a greyed-out Publish button and an entry in the ACP approval list.

## Prerequisites
Lab 01 done. Power Platform admin. The lab environment is a **Managed Environment**. The app registration needs the BAP admin scope (`https://service.powerapps.com/.default`, verify) for `dlp_check.py`; the edits themselves are done in PPAC so they stay visible and reversible.

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
python dlp_check.py                      # state 1
# follow dlp_policy.md: block HTTP (+ MCP connector), observe publish disabled, unblock
python dlp_check.py                      # state 2, then state 3 after revert
# follow environment_group_rules.md and credits_caps.md
```

## What each file proves
- **dlp_check.py** the classification is data, read from the admin API; HTTP endpoint rules print when present.
- **dlp_policy.md** the publish button is the gate; MCP is a connector.
- **environment_group_rules.md** the sharing dialog loses "Everyone" once the group rule is set.
- **credits_caps.md** the 125 % cliff and the per-agent cap that prevents it.

## Proof checklist
- [ ] three `dlp_check.py` outputs saved: before, blocked, reverted (identical to before)
- [ ] screenshot of the disabled Publish button naming the violating tool
- [ ] the MCP connector moved to Blocked also disables publish
- [ ] environment group `cs-track-makers` exists with the sharing rule; "Everyone" gone from the Share dialog
- [ ] per-agent credit cap set on the autonomous agent; consumption report located
- [ ] every change reverted or recorded as the intended state
