# 05 — Agent Registry: publish records, not secrets

**Start with the failure.** The only list of agents and MCP servers in the company is a wiki page. A partner team copies the Gateway URL and a Cognito client secret from it. Now the same things are registry records: descriptors with an approval gate, discoverable through IAM, with no credential inside.

## Goal
Create a registry, add an MCP record (the lab 03 Gateway), an A2A record (the B03 specialist's agent card, synchronised from its URL) and a skills record (`SKILL.md`), push them through `PENDING_APPROVAL → APPROVED`, and discover them with the read-only `agent-registry` client.

## You will end with
- `TICKET_REGISTRY_ID` in `.env`; three records, all `APPROVED`
- a discovery transcript for the query "refund"

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
cd 05-agent-registry
python create_registry.py
python register_records.py     # A2A record only if TICKET_A2A_CARD_URL is set (B03 lab 03)
python discover.py
```

## Facts that matter
- AWS Agent Registry: preview 9 Apr 2026, GA Aug 2026 (31 Aug per What's New; one migration guide says 6 Aug). Management is on `bedrock-agentcore-control`; discovery is the separate `agent-registry` service with three read-only operations.
- `descriptorType` ∈ MCP, A2A, CUSTOM, AGENT_SKILLS; content inline or `synchronizationType: URL` with OAuth or IAM credentials for the fetch.
- Lifecycle: DRAFT, PENDING_APPROVAL, APPROVED, REJECTED, DEPRECATED. `approvalConfiguration.autoApproval` turns the gate off.
- Cross-account via AWS RAM, Organizations auto-detection, CMK, PrivateLink; the registry exposes an MCP endpoint for run-time discovery (console; the exact `GetRegistry` field is marked verify).

## Proof (checklist)
- [ ] `get_registry` status `ACTIVE`/`READY` with `approvalConfiguration.autoApproval = false`
- [ ] three records listed `APPROVED` (or two plus an honest "A2A skipped" line)
- [ ] `search_discoverable_registry_records("refund")` returns the MCP record and the skill record
- [ ] a second IAM principal with only `agent-registry:*Discoverable*` can run `discover.py` but not `register_records.py`

## Next
`../06-a2a-and-runtime-targets/` — agents as Gateway targets and A2A passthrough.
