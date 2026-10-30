# 10 — Private tool catalog (API Center) → Foundry

## Goal
Register the APIM-fronted MCP server in Azure API Center so it appears in Foundry's **Build > Tools** catalog (preview) for everyone with API Center Data Reader, then consume it from an agent. The 2025 notebook only printed the `az apic` commands; `private_tool_catalog.py` runs them.

## Run
```bash
source ../.venv/bin/activate
APIC_NAME=<api-center> APIC_RESOURCE_GROUP=<rg> APIM_MCP_URL=https://<apim>.azure-api.net/mcp/ticketing/mcp python private_tool_catalog.py
```

## Proof (checklist)
- [ ] `az apic api list` shows `ticketing-mcp` with a production deployment pointing at the APIM URL
- [ ] the server is visible in the Foundry portal catalog and can be added to an agent from there
- [ ] `ticket-agent-catalog` lists the tools

## Next
`../06-a2a/` — agents calling agents.
