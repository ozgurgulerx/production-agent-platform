# Agent 365: registry, Tooling Gateway, BYO MCP approval (F15, E8, E9, D9, D10)

Agent 365 is GA since 1 May 2026; Copilot Studio agents auto-register. Security controls on Entra Agent ID and Defender for AI agents need the licence since 1 Jul 2026.

## Registry (E8, E9)
1. Microsoft 365 admin centre → Agents → All agents → find the ticket agent (same Entra Agent ID as `inventory.py` printed).
2. **Block** it. In Copilot Studio the agent stops answering on channels. Unblock. (Revert in the same page.)
3. **Reassign** owner to a second admin account and back: this is the leaver procedure; note that tool connections on maker credentials still belong to the old maker until each tool is re-authenticated.
4. Note the **AI Reader** role for auditors who should see but not act.

## Tooling Gateway with APIM (D10, preview)
Put the ticket MCP server behind the APIM instance from the Foundry track (F09 material, MCP passthrough with `validate-azure-ad-token` and a rate limit). Then:
1. M365 admin centre → Agents → Tools → Gateways → Connect APIM (AI Gateway tier). Discovery lists the ticket MCP server and its four tools.
2. Block `issue_refund` at the gateway level. In Copilot Studio the tool disappears from the agent's MCP tool list on the next refresh (D2 dynamic refresh). Unblock.
3. One block removed the tool from every agent in the tenant that uses that server, including Foundry agents calling the same APIM endpoint. That is the cross-track proof.

## BYO MCP approval (D9, preview)
With the Agent 365 CLI (install and exact commands: verify against D9 on the day):
```bash
agent365 mcp register --name tickets --url $TICKET_MCP_URL --auth EntraOAuth     # verify command set
```
Admin: M365 admin centre → Agents → Tools → pending → approve. Only then does the server appear for makers. Block one tool; Defender hunting table `ExecuteToolByGateway` shows calls. Clients today: Copilot Studio, VS Code, Claude Code, GitHub Copilot CLI. Foundry is not a client yet.

## Proof
- [ ] ticket agent found in the Agent 365 registry with its Entra Agent ID
- [ ] block / unblock observed from a channel
- [ ] reassign done and reverted
- [ ] Tooling Gateway connected to APIM and `issue_refund` blocked once, then unblocked
- [ ] BYO MCP registration approved (or the approval queue screenshot if the CLI differs)
