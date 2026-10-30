# C03 labs — build the ticket agent every way Copilot Studio allows

Runnable proofs and portal walkthroughs for the C03 chapter. Setup is shared: do [`../../labs-setup/`](../../labs-setup/) first (venv, `.env` at the track root, `pac auth create --deviceCode`, the device-code app registration, `verify.sh` printing OK). Each lab README ends with a **proof checklist**; a lab is done when the boxes are ticked with real output. Nothing in this folder had run against the tenant when it was written (25 Oct 2026).

```
labs/
├── 01-ticket-agent-two-ways/   portal agent on the Standard harness, then clone → Git → push → publish; Direct-to-Engine and Direct Line from code
├── 02-github-copilot-harness/  the same agent on the new harness: skill, memory, workflow, publish as MCP / A2A (portal walkthrough)
├── 03-autonomous-trigger/      Dataverse row → agent run; agent flow with request-information; read the run from transcripts
└── 04-agents-sdk-connected/    a Python Agents SDK agent on /api/messages, added as a connected agent
```

| Lab | Chapter section | Creates | Time |
|---|---|---|---|
| 01 | §1, §2 ways 1, 2, 6 (calling direction), §3 publish and channels | `Ticket Agent` (`AGENT_SCHEMA_NAME`, `AGENT_ID`), a Git clone of it | 1 session |
| 02 | §2 ways 3, 5, §5 publish as MCP / A2A | `Ticket Agent (GH)` | 1 session, portal |
| 03 | §4 autonomy | a trigger, an agent flow | with 02 |
| 04 | §2 way 6 (connected direction), §5 | `ticket-sdk-agent` service + connected agent | 1 session |

Run them in order: 03 and 04 reuse `_common.py` patterns and the `.env` keys from 01. C04, C05 and C09 labs assume `Ticket Agent` exists and is published with Authenticate with Microsoft, so finish 01 before moving on.

```bash
source ../../labs-setup/.venv/bin/activate
cd 01-ticket-agent-two-ways && python find_agent_id.py && python invoke_direct_to_engine.py
```

Next chapter: [`../../C04-Tools-Identity-MCP-and-Connected-Agents/labs/`](../../C04-Tools-Identity-MCP-and-Connected-Agents/labs/).
