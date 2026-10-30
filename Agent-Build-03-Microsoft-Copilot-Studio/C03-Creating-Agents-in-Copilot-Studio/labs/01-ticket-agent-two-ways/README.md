# 01 — The ticket agent two ways: portal, then Git

One agent, built in the portal on the Standard harness, then cloned to YAML, edited, pushed and published from the command line. Then called from code two ways. The point is to see where the **definition** lives (Dataverse, then also Git) and that the harness does not change when the authoring surface does.

| Way | File | Proves |
|---|---|---|
| 1 portal | this README §A | generative orchestration + instructions + knowledge is a complete agent; Authenticate with Microsoft; publish |
| 2 code-first | `clone_pull_push.sh`, `create_from_yaml.sh` | `pac copilot clone / pull / push / publish`; offline `pack` + `pac solution import` |
| 6 calling direction | `invoke_direct_to_engine.py` | Direct-to-Engine with a delegated token; refusal over 250 GBP happens in the agent |
| channel for code | `invoke_directline.py` | Direct Line v3 against the Mobile app token endpoint |
| plumbing | `find_agent_id.py` | the agent is a `bot` row; schema name is the handle |

## Prerequisites
`labs-setup/` done: venv, `.env` at the track root with `TENANT_ID`, `CLIENT_ID`, `ENVIRONMENT_ID`, `ENVIRONMENT_URL`; `pac auth create --deviceCode` done; the device-code app registration consented for `CopilotStudio.Copilots.Invoke` and Dynamics CRM `user_impersonation`.

## A. Portal (way 1)
1. https://copilotstudio.microsoft.com → pick the environment (top right) → **Create** → **New agent** → **Skip to configure**.
2. Name `Ticket Agent`. Paste [`instructions.md`](instructions.md) into Instructions. Orchestration: **Generative** (default for new agents; required for MCP, B1).
3. Knowledge → **Add knowledge** → Upload files → the three policy documents from `../../../C08-Knowledge-and-Memory/labs/01-knowledge/data/policies/` (or SharePoint, see C08). Note: uploaded files are not ALM-portable (C4).
4. Settings → **Security** → Authentication → **Authenticate with Microsoft** → Save.
5. Settings → **Generative AI** → Primary model: leave **GPT Chat Latest** (K1; do not pin GPT-4.1, it retires 12 Nov 2026).
6. Settings → **Advanced** → Metadata → copy the **Schema name** into `.env` as `AGENT_SCHEMA_NAME`.
7. Test pane: "What does the refund policy say about duplicate charges?" → expect a cited answer. "Refund 400 GBP on ticket T-2041" → expect a refusal (tools arrive in C04 lab 02; until then the instruction alone refuses).
8. **Publish** → Channels → Demo website → open the link → repeat the two questions. Then Channels → Teams and Microsoft 365 Copilot → Add.

## B. Code-first (way 2)
```bash
source ../../../labs-setup/.venv/bin/activate
python find_agent_id.py                 # writes AGENT_ID
./clone_pull_push.sh                    # clone → edit → pull → push → publish
./create_from_yaml.sh                   # a second agent from a local scaffold, packed offline and imported
```
Open `agent/` in VS Code with the Copilot Studio extension (C2) to see the same tree with IntelliSense and a diff view.

## C. From code
```bash
python invoke_direct_to_engine.py       # device-code prompt once; three turns
DIRECTLINE_TOKEN_ENDPOINT='<from Channels > Mobile app>' python invoke_directline.py
```

## What each script proves
- **find_agent_id** the agent is a Dataverse `bot` row; `publishedon` empty means the client will not find it.
- **clone_pull_push** the definition is YAML you can diff; `push` refuses on conflict; `publish` is a CLI verb.
- **create_from_yaml** `pack` needs no credentials, so a build agent can produce the solution zip.
- **invoke_direct_to_engine** no Direct Line, no Azure Bot; a delegated Power Platform API token and the schema name.
- **invoke_directline** the older channel-for-code; still what the Copilot Agent Kit uses for tests (I5).

## Proof checklist
- [ ] Test pane answers the policy question with a citation
- [ ] Demo website link opens and answers; Teams app shows the agent
- [ ] `find_agent_id.py` prints the bot row and `publishedon`
- [ ] `clone_pull_push.sh` leaves an `agent/` tree in Git; a pushed instruction edit is visible in the portal
- [ ] `create_from_yaml.sh` imports a solution and `pac copilot list` shows the second agent
- [ ] `invoke_direct_to_engine.py` turn 2 refused, turn 3 proceeds
- [ ] `invoke_directline.py` prints an agent reply
