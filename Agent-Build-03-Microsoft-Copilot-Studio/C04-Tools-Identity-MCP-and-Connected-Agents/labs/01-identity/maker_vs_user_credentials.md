# Maker credentials vs end-user credentials, and the security scan (reading map D1, E6, E7)

## Switch, scan, revert
1. Tools → `issue_refund` (the MCP tool from lab 02, or any connector tool) → Settings → "Authentication" / "Connection" → change from **End user** to **Maker-provided** → Save.
2. Publish. The pre-publish **security scan** lists the finding: a tool runs with maker credentials. Screenshot it.
3. Run `python ../01-identity/inventory_entry.py`: the tool row shows `connectionProvider: Maker` and `connectionIdSharedByMaker`.
4. Ask the agent, as a second user, to refund a ticket that user does not own. With maker credentials the API sees the maker and allows it.
5. Revert to End user, publish; the scan is clear; the second user is refused by the API.

## When maker credentials are defensible
Read-only, non-personal data (a public price list through a connector), with the reason written in the tool description and the agent restricted to viewers. Never for anything that writes on behalf of a person.

## The three findings the scan knows (E6)
No authentication on the agent; maker credentials on a tool; tenant-wide sharing. All three also surface in the inventory (E7) and, with Agent 365, in the registry.
