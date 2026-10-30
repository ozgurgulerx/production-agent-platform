# Environment group rules, filled in for a UK bank (F2, F3; 25 Oct 2026)

Rules are set once on the group and inherited by every environment in it. Only Managed Environments can join a group. Two groups are enough for this track: **Makers** (routed personal dev environments) and **Production** (shared, Pipelines target).

| Rule (F2) | Makers | Production | Why |
|---|---|---|---|
| Transcript access | makers can read own agents | admins and Analytics Viewer role only | transcripts contain customer text; `REDACTED` for SharePoint-grounded answers only |
| Advanced Connector Policies | advisory list | **ACP-only mode** (preview): only pre-approved connectors and actions | the MCP switch; also blocks the Friday-afternoon server |
| AI prompts (prompt tools) | on | on, premium models by approval | prompt tools bill 1 / 15 / 100 credits per 10 responses (K6) |
| Copilot credit draw from tenant pool | per-agent cap 2,000 / month | per-agent cap set per business case, alert at 80 % | agents stop at 125 % of prepaid (K6) |
| Generative AI settings | on | on | |
| Cross-geo data movement | off | off | UK data residency; also a tenant switch (C11) |
| External models (Anthropic, Mistral, xAI) | allowed (Anthropic is a Microsoft subprocessor; K3) | allowed only after model-risk sign-off; Mistral / xAI off | externally hosted providers leave the Microsoft boundary |
| Preview and experimental AI models | allowed | off | retirement wave Oct–Nov 2026 (K1) shows how fast these move |
| Knowledge sources for agents | all | SharePoint, Dataverse, Azure SQL, Foundry IQ | public websites and uploaded files are hardest to audit |
| Agent sharing | Editor to individuals, Viewer to individuals and groups, viewer cap 50 | Viewer to named security groups only, no Everyone | F4 |
| Skills in Copilot Studio | on | on | |
| Viva Insights data sharing | off | off | |
| Content security policy (web canvas) | default | `frame-ancestors` bank intranet domains only | iframe embedding of the demo website |
| Default environment routing (F3) | create per-maker dev environments in the Makers group | n/a | keeps the default environment empty of agents |

What a group cannot do: allow or block MCP by name (use DLP / ACP), enforce Conditional Access (Entra), cap one tool's arguments (the tool or a gateway).
