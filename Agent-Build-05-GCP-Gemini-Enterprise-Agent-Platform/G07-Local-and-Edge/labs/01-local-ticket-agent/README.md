# 01 — The ticket agent on Gemma 4, locally

Same ADK agent as G03 lab 01, different model string, and a local stdio MCP stub in place of the Toolbox on Cloud Run. No ADC, no `.env` values beyond `OLLAMA_API_BASE` and `LOCAL_MODEL`, nothing leaves the machine until the comparison step.

Status on 25 Oct 2026: scaffold only, functionality unverified.

## Goal

Three ticket answers from `gemma4:e4b`, a tool call that round-trips through the stub, and an `adk eval` table for local next to one for cloud on the same evalset.

## Prerequisites

- Ollama installed and running; `ollama pull gemma4:e4b` (tags `e2b|e4b|26b|31b`, map H2). Disk and RAM per tag are not in the map; expect several GB for E4B.
- Shared venv active; `litellm>=1.84` is already pinned there (map H8 advisory: 1.82.7 and 1.82.8 compromised 2026-03-24).
- `.env` at the track root has `OLLAMA_API_BASE=http://localhost:11434` and `LOCAL_MODEL=ollama_chat/gemma4:e4b` (the `.env.example` defaults).
- For the comparison only: G05 lab 02's evalset as `EVALSET`, its criteria file as `EVAL_CONFIG`, and ADC for the cloud agent.

## Steps

```bash
cd Agent-Build-05-GCP-Gemini-Enterprise-Agent-Platform/G07-Local-and-Edge/labs/01-local-ticket-agent
source ../../../labs-setup/.venv/bin/activate
ollama pull gemma4:e4b                                     # map H2
curl -s http://localhost:11434/api/generate -d '{"model":"gemma4:e4b","prompt":"Say ready.","stream":false}'   # map H2 endpoint
python ticket_mcp_stub.py --selftest                      # lists the two tools over stdio and exits
adk run .                                                  # ask: status of 1042 / refund 300 GBP on 1042 / refund 120 GBP on 1042
python compare_with_cloud.py                               # adk eval twice: this folder, then the G03 agent; prints both tables
pytest -q                                                  # collects the skeleton; "scaffold only" until you write the tests
```

Optional, Gemini CLI as a second client for the same stub (map H6):

```json
{
  "mcpServers": {
    "tickets": {
      "command": "python",
      "args": ["<absolute path>/ticket_mcp_stub.py"],
      "timeout": 30000,
      "trust": false
    }
  }
}
```

Put that in `~/.gemini/settings.json`, start `gemini`, run `/mcp`, ask for ticket 1042.

## Expected output

- `adk run .` prints the model as `ollama_chat/gemma4:e4b` in the first event and answers all three; the 300 GBP refund is refused.
- `compare_with_cloud.py` prints two `adk eval` tables with the same case ids. Only `tool_trajectory_avg_score` and `response_match_score` are expected on the local row; rubric criteria need the platform or an API key (map E1) and are expected to be absent or skipped for local.

## What to notice

- E4B may still try to approve 300 GBP. The refusal belongs in the instruction and in the tool contract regardless of model size; a smaller model makes that lesson louder.
- Nothing screened these prompts, no identity was attached to the tool call, no trace was written. That is README §7's right-hand column; you own it here.
- The stub and the Toolbox both speak MCP; `agent.py` differs from the cloud agent only in the connection params (stdio versus streamable HTTP, map D3) and the model string.

## Proof (checklist)

- [ ] `ollama pull gemma4:e4b` done; the curl line returns a response
- [ ] `ticket_mcp_stub.py --selftest` lists `get_ticket` and `list_tickets`
- [ ] three answers from `adk run .` recorded below, with the 300 GBP refusal
- [ ] two `adk eval` tables (local, cloud) pasted below; the criteria that ran locally named
- [ ] optional: Gemini CLI `/mcp` shows `tickets` and a ticket question is answered through it

## Cleanup

`ollama rm gemma4:e4b` if disk matters. Remove the `tickets` entry from `~/.gemini/settings.json`. Nothing was created in the cloud.

## Known gaps

Written for macOS; Linux and Windows paths untested. The MCP Python server package used by the stub is not in the reading map; the stub names it and the learner confirms the import. llama.cpp path (map H3) described in the chapter, not scripted. Nothing here has run yet.

## Results

_(paste answers and the two eval tables here)_
