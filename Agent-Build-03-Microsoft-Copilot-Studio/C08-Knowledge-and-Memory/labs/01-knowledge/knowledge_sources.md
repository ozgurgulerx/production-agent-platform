# Knowledge sources for the ticket agent: what you added and what each one did

Fill the last column from your own run. The first three rows are the lab; the rest are the catalogue for reference (chapter §1, map J1, J2, J7).

| Source as added                                        | Harness        | Live or ingested                | Permission check at answer time    | Travels with the solution           | Citation points at             | Observed in your run |
| ------------------------------------------------------ | -------------- | ------------------------------- | ---------------------------------- | ----------------------------------- | ------------------------------ | -------------------- |
| SharePoint, connector ("UK card team policies (live)") | Standard       | live, Graph search              | yes, the signed-in user's          | yes (site URL)                      | the SharePoint item            |                      |
| Upload files (the same three `.md`)                    | Standard       | ingested into Dataverse         | no                                 | **no**, re-upload after import (J7) | the uploaded file              |                      |
| Foundry IQ tool (`kb-ticket-policies`)                 | GitHub harness | live, Foundry IQ owns the index | depends on the auth mode you chose | yes (reference)                     | the Foundry IQ source document |                      |
| Upload files → SharePoint/OneDrive folder              | both           | ingested copy, re-synced 4–6 h  | no                                 | no                                  | the copied file                | not used             |
| Dataverse table                                        | both           | live                            | Dataverse security roles           | yes                                 | the record                     | not used             |
| Enterprise data (Graph connector)                      | both           | live, Microsoft Search          | yes                                | yes                                 | the external item              | not used             |
| Azure OpenAI on your data (classic node)               | Standard       | live, your index                | your index's auth                  | yes                                 | your index document            | not used             |

## The one line to write for the UK bank

Which source would you ship, and why? (Expected shape: "the SharePoint connector with Authenticate with Microsoft and tenant graph grounding, because the card team's folder has an ACL, labels must show in citations, and the site URL survives `pac solution import`; uploads only for the public FAQ.")

> _your answer_

## Settings you confirmed

- [ ] Generative orchestration on
- [ ] Allow ungrounded responses off
- [ ] Content moderation High
- [ ] End-user authentication: Authenticate with Microsoft
- [ ] Source descriptions name the team, the document and the effective date
