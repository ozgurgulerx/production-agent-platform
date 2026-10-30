# 03 — Agent 365 and Purview

The tenant view: the registry that lists and blocks agents across Copilot Studio and Foundry, the Tooling Gateway that governs MCP servers through APIM, the approval queue for new servers, and Purview as the record of what every agent did.

## Start with the failure
The MCP server added on a Friday. Nobody approved it, nobody can list its tools, and the only trace is a connector row. After this lab, a new server waits in an approval queue, a gateway block removes a tool from every agent at once, and the audit log shows who published what and who called which tool.

## Prerequisites
Labs 01 and 02. Agent 365 licence in the tenant; Global or AI admin; Purview audit enabled; Graph `AuditLog.Read.All` on the app registration. The APIM instance from the Foundry track in front of `TICKET_MCP_URL` for the Tooling Gateway step (optional but the cross-track proof).

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
# follow agent365_registry.md (block / reassign / gateway / approval)
python purview_audit.py --hours 24
# follow purview.md, cmk_firewall.md, defender.md
```

## What each file proves
- **agent365_registry.md** block and reassign; one gateway-level block removes a tool from every agent; approval before availability.
- **purview_audit.py** `BotPublish` and `CopilotInteraction` are one query apart.
- **purview.md** transcripts live in DSPM for AI, not in the audit record; retention drops text, keeps events.
- **cmk_firewall.md** what CMK covers and what the firewall does not.
- **defender.md** the licence boundary and the protection status column.

## Proof checklist
- [ ] ticket agent found and blocked / unblocked in the Agent 365 registry
- [ ] owner reassigned and reverted
- [ ] Tooling Gateway connected; `issue_refund` blocked once at the gateway and the tool vanished from the agent
- [ ] `purview_audit.py` prints your `BotPublish` and at least one `CopilotInteraction`
- [ ] DSPM for AI shows the `issue_refund` tool call inside an interaction
- [ ] IP firewall tested from outside the range and disabled again
- [ ] a Defender alert from the XPIA test, answered with quarantine, then released
