# 02 — The same agent on the GitHub Copilot harness (portal walkthrough)

Way 3. The GitHub Copilot harness (GA 3 Aug 2026, A5) has no topics: instructions, knowledge, tools, **skills**, **memory**, **hooks** and **workflows**, with a goal-decomposing orchestrator and usage-billed credits. Code-first coverage is partial today (no Direct-to-Engine client support, C8), so this lab is a portal walkthrough with the artefacts you would keep in Git anyway.

## Walkthrough
1. Create → New agent → choose the **GitHub Copilot harness** (the harness is picked at creation, A1). Name `Ticket Agent (GH)`.
2. Instructions: paste `../01-ticket-agent-two-ways/instructions.md`.
3. Knowledge: the three policy documents (SharePoint recommended; Foundry IQ as a tool is the C08 path, J3).
4. Tools: add the ticket MCP server (gallery or custom HTTPS URL; auth API key, OAuth client id/secret or signed-in identity, D5). Tool list is negotiated on add; check the activity trace after the first call.
5. Skills: create `ticket-triage` from [`skills/ticket-triage/SKILL.md`](skills/ticket-triage/SKILL.md).
6. Memory: switch on (production-ready preview, B10). See [`memory_note.md`](memory_note.md).
7. Workflow: build the refund-approval workflow from [`workflow.md`](workflow.md) (agent node + request-information, A7).
8. Model: pick from the harness dropdown (K2): GPT-5.5 Chat or Claude Sonnet 5 for chat, a "Deep" model only for the workflow's reasoning node.
9. Publish → Teams and Microsoft 365 Copilot. Channels available on this harness: M365 Copilot, Teams, demo website, web app, MCP client, A2A client (L2). No WhatsApp, SharePoint or Direct Line.
10. Optional: publish as an MCP server or A2A agent for Foundry ([`publish_as_mcp_a2a.md`](publish_as_mcp_a2a.md), B6).

## What to notice
- There is no topic list. A deterministic step is a workflow or a hook, not a topic.
- Billing is usage credits (K5): watch Monitor → Usage after ten test turns.
- The Direct-to-Engine script from lab 01 does not work here yet (C8). Teams or the web app are the test surfaces.

## Proof checklist
- [ ] Agent created on the GitHub Copilot harness; the Topics tab is absent
- [ ] Skill `ticket-triage` appears under Skills and is used in a triage question (activity trace shows it)
- [ ] Memory: a second session recalls the card type stated in the first
- [ ] Workflow runs and pauses on request-information for a 400 GBP refund
- [ ] Published to Teams; usage credits visible in Monitor
- [ ] (optional) A2A client channel enabled; Foundry's A2A tool reaches it
