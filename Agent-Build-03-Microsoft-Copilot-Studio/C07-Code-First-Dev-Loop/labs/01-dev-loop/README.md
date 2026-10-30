# 01 — The dev loop: YAML in Git, cloud as the only runtime

You will clone the C03 ticket agent as YAML, change one sentence of its instructions on a branch, push it back, publish it, then do the same from CI with `pack` and `pac solution import`. The second half runs the one piece of this track that executes on your laptop, the C03 lab 04 Agents SDK agent, in the Playground and behind a tunnel.

## Prerequisites
- `pac` installed and a profile on the dev environment: `pac auth create --deviceCode`, `pac env select --environment $ENVIRONMENT_ID`.
- The ticket agent from C03 lab 01 exists and has been published once; its schema name is `AGENT_SCHEMA_NAME` in the track-root `.env`.
- Shared venv activated for the SDK part: `source ../../../labs-setup/.venv/bin/activate`.
- Optional: the Copilot Studio VS Code extension; a dev tunnel tool (`devtunnel` or ngrok).

## Run
```bash
set -a; . ../../../.env; set +a
bash pac_init_local.sh                       # offline scaffold + clone of the real agent; prints the file tree the clone produced
# follow yaml_edit_and_push.md: branch, edit instructions, pac copilot pull, push, publish; confirm in the portal
# follow vscode_extension.md: open ./ticket-agent, use sync + apply instead of pull/push once
# follow local_mcp_for_pac.md: pac copilot mcp --run, then drive one pull from a coding agent
# follow agents_sdk_local/README.md: run the C03 lab 04 agent, Playground, tunnel, connected agent
# ci_pipeline.yml: copy into .github/workflows of the repo that holds ./ticket-agent; set the federated credential
```

## What each step proves
- `pac_init_local.sh`: an agent is a folder of YAML; `init` works offline, `clone` needs the environment (C1).
- `yaml_edit_and_push.md`: `pull` merges three ways, `push` refuses conflicts, `publish` is what makes new sessions see the change (C1, L1).
- `vscode_extension.md`: the same loop with schema IntelliSense and a diff preview (C2).
- `local_mcp_for_pac.md`: pac exposes itself as an MCP server for coding agents; scope it to dev (C1).
- `agents_sdk_local/`: your code runs locally; Copilot Studio reaches it only through the Activity endpoint with the auth mode you set (B5, C7, C9).
- `ci_pipeline.yml`: `pack` without login, `import` with a federated credential, the C05 evaluation call as the gate (C1, I3).

## Proof (checklist)
- [ ] `pac_init_local.sh` prints the clone's file tree and `git status` shows it as a clean initial commit
- [ ] after `push` + `publish`, a new test-pane session answers with the changed instruction wording; an old session does not until "start over"
- [ ] a deliberate conflict (edit the same topic in the portal and in YAML) makes `pac copilot push` stop with a conflict message
- [ ] `pac copilot pack` runs with no `pac auth` profile selected and produces a zip; `pac solution import` into the test environment succeeds under the pipeline identity
- [ ] the Playground shows a reply from `http://localhost:3978/api/messages`; the connected agent in Copilot Studio gets the same reply through the tunnel
- [ ] the CI run's evaluation step prints a pass rate from the C05 test set

## Known gaps
Flags in the scripts are from the pac reference of 10 Jul 2026 and marked verify until the first run. The clone's file layout is not enumerated on Learn; record yours in this README after the first clone. A third-party report says a one-time portal step is needed before pipeline exports; marked verify in `ci_pipeline.yml`. Nothing here has run yet.
