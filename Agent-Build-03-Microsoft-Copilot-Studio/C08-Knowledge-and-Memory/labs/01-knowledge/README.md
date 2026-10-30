# 01 — Knowledge for the ticket agent: live, ingested, and Foundry IQ

Three policy documents go to a SharePoint library from code. The ticket agent gets them twice, once as a **SharePoint connector** source (live, permission-trimmed) and once as **uploaded files** (a copy in Dataverse), and you compare what each does to citations, permissions and ALM. Then the GitHub-harness copy of the agent gets the F08 Foundry IQ knowledge base as a **tool**. The three canonical questions, including the Peru refusal, are asked through Direct-to-Engine from Python so the proof is a terminal transcript, not a screenshot.

## Prerequisites

- Shared setup done (`../../../labs-setup/`): venv, `.env` at the track root with `TENANT_ID`, `CLIENT_ID`, `ENVIRONMENT_ID`, `AGENT_SCHEMA_NAME`, `SHAREPOINT_SITE_URL` (a site you own, e.g. `https://contoso.sharepoint.com/sites/CardTeam`).
- The app registration (`CLIENT_ID`) is a public client with device-code flow enabled and delegated permissions `Sites.ReadWrite.All` (Graph, for the upload) and `CopilotStudio.Copilots.Invoke` (Power Platform API, for Direct-to-Engine), consented.
- The ticket agent from C03 lab 01 published once, with **Authenticate with Microsoft** (live sources need a user token, E5) and **generative orchestration** on (B1).
- For step 4 only: the F08 knowledge base `kb-ticket-policies` exists in your Foundry project, and a GitHub-harness copy of the ticket agent (C03 lab 02).

| Principal                      | Needs                                             | Why                                                                         |
| ------------------------------ | ------------------------------------------------- | --------------------------------------------------------------------------- |
| you, signed in by device code  | member of the SharePoint site; maker on the agent | upload; add knowledge; invoke                                               |
| the agent (Entra Agent ID, E1) | nothing extra for SharePoint connector sources    | Graph search runs as the user, not as the agent                             |
| end users                      | read access on the `Policies` library             | otherwise the connector source returns nothing for them, which is the point |

## Run

```bash
source ../../../labs-setup/.venv/bin/activate
python upload_policies.py                  # 1. three files into <site>/Shared Documents/Policies via Graph; prints web URLs
# 2. portal: Knowledge > Add > SharePoint > paste the site URL; name it "UK card team policies (live)"; description from sketches/knowledge_source_table.md
#    Settings > Generative AI: orchestration on, "Allow ungrounded responses" off, moderation High; publish
python ask_three_questions.py              # 3. Direct-to-Engine: three questions, text + citations; Peru must be a refusal
# 4. portal, second agent or a copy: Knowledge > Add > Upload files > the three files from data/policies; publish; run step 3 again against it
#    (set AGENT_SCHEMA_NAME to the copy, or pass --agent <schema name>)
# 5. GitHub-harness copy: follow foundry_iq_tool.md; ask the three questions in the test pane; read the activity trace
```

## What to notice

- The connector-source answer carries a citation to the SharePoint item and honours the user's permission: remove a test user from the library and the same question stops answering for them. The uploaded-files answer does not change (J2).
- `ask_three_questions.py` prints every `Activity` the client yields. Citations arrive as entities or attachments on the message activity; the exact shape is marked `# verify` in the script, print them raw the first time.
- Export the solution (C02) and import it into a second environment: the connector source is there, the uploaded files are not (J7).
- The Peru answer is a refusal because ungrounded responses are off, not because of moderation. Turn the switch on and it becomes "Lima"; turn it back off.

## Proof checklist

- [ ] `upload_policies.py` prints three web URLs under `.../Policies/`
- [ ] Q1 "Can I refund £300 to a customer's new card?" answered with citations to the refund and card policies
- [ ] Q2 "Do customers still need a travel notice?" answered "no, since May 2026" with a card-policy citation
- [ ] Q3 "What is the capital of Peru?" refused (no-knowledge message), ungrounded responses off
- [ ] Same three questions against the uploaded-files agent: same answers, citations point at uploaded files, and a user without library access still gets answers (write the sentence that explains why)
- [ ] Foundry IQ tool added on the GitHub-harness copy; activity trace shows a retrieval for Q2 and none usable for Q3
- [ ] One line in `knowledge_sources.md` filled in: which source you would ship for the UK bank and why
