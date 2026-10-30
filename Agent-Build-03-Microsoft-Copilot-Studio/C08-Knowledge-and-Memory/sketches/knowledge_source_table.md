# Knowledge source decision table (sketch, 25 Oct 2026)

Use this when a stakeholder says "just add the SharePoint site". Walk the four questions top to bottom; the first "no" decides.

| Question                                                        | If yes                                                                                             | If no                                                   |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Does the content have an ACL anyone cares about?                | **Live source only**: SharePoint connector, Dataverse, Graph connector, Foundry IQ with Entra auth | an ingested source is acceptable                        |
| Must it survive `pac solution import` into another environment? | live source, or Foundry IQ tool (the reference travels, the index stays in Foundry)                | uploaded files are fine, re-upload per environment (J7) |
| Will more than one platform ground on it?                       | Foundry IQ knowledge base, one tool per platform (J3)                                              | platform-native source                                  |
| Is the agent on the Standard harness?                           | Azure AI Search via the classic generative-answers node if you need your own index (J4)            | Foundry IQ tool available (GitHub harness)              |

## Settings that go with every policy agent

```text
Generative orchestration        on          (required for MCP and web search; B1)
Allow ungrounded responses      off         (the Peru question becomes a refusal)
Content moderation              High        (default; F11)
End-user authentication         Authenticate with Microsoft   (live sources need a user token; E5)
Source description              "<team> <document> policy, effective <date>"   (the 25-source filter reads it; B1)
```

## Limits to recite

- 500 knowledge objects per agent; selection pass above 25 sources (B1)
- Uploaded files: 500 per agent, 512 MB each (J2)
- SharePoint upload: 1,000 files, 50 folders, 10 levels per source, 4–6 h sync (J2)
- SharePoint connector: 25 sites; 200 MB files with tenant graph grounding (J2, J6)
- Dataverse: 2 sources × 15 tables (J1)
- Foundry IQ: one knowledge base per agent, GitHub harness only (J3)
- Memory: per user, 28 days of inactivity, maker cannot read (G1)
