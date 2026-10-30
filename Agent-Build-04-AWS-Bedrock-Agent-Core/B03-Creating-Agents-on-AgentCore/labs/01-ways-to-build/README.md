# 01 — Create the same agent every way AgentCore allows

One agent, the support-ticket assistant, built every way AgentCore allows. The point is not the agent. The point is to see where the **definition** lives and where the **loop** runs in each case, because that decides what you can version, govern, trace and roll back. Every variant is then called through the same data-plane surface: `InvokeAgentRuntime` (or `InvokeHarness`) with a `runtimeSessionId`.

| # | Way | Definition lives | Loop runs | Status | File |
|---|---|---|---|---|---|
| 1 | Harness (managed loop) | AgentCore, versioned | AgentCore | GA Jun 2026 | `01-harness.md`, `01-harness-sdk.py`, `harness/` |
| 2 | Runtime, direct code deploy (zip) | your code, versioned by AgentCore | AgentCore microVM | GA Nov 2025 | `02-runtime-code-deploy.py`, `agent/` |
| 3 | Runtime, container image | your container | AgentCore microVM | GA Oct 2025 | `../02-runtime-containers/container-deploy/` |
| 4 | Runtime on Instances (EC2 capacity) | your container | your EC2, AgentCore-managed | GA Aug 2026 | `../02-runtime-containers/instances/` (described) |
| 5 | Ephemeral Strands, Bedrock direct | your process | your process | GA | `03-ephemeral-strands.py` |
| 6 | Self-hosted (Lambda/ECS) behind a Gateway | your infra | your infra | GA | `../02-runtime-containers/self-hosted-lambda/` |
| 7 | Classic Bedrock Agent | Bedrock Classic | Bedrock Classic | maintenance mode, closed 30 Jul 2026 | `../03-multi-agent/appendix-classic-agent-migration/` |

Then `04-invoke-everything.py` calls whichever of them exist, identically, and `05-versions-and-endpoints.py` shows versions, the `DEFAULT` endpoint and a pinned endpoint moving forward and back.

Decision rule to carry: *managed loop and fastest path → Harness; custom loop or dependencies → Runtime code deploy; system packages or non-Python → container; GPU or sessions longer than 8 h → Instances; nothing to manage → ephemeral Strands; your own platform constraints → self-hosted behind a Gateway.*

## Prerequisites
`labs-setup/` done: venv, `.env` at the track root with `AWS_REGION`, `AWS_PROFILE`, `BEDROCK_MODEL_ID`, `AGENTCORE_RUNTIME_ROLE_ARN`, `CODE_BUCKET`; `aws sso login`; `verify.sh` printing OK. The Node CLI (`@aws/agentcore` 1.0) is only needed for the `01-harness.md` CLI path.

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
cd 01-ways-to-build
python 03-ephemeral-strands.py                 # way 5: no resource created; watch the 480 GBP refusal
python 02-runtime-code-deploy.py --keep        # way 2: zip -> S3 -> Runtime READY; writes TICKET_AGENT_RUNTIME_ARN
python 01-harness-sdk.py --keep                # way 1: harness + return-of-control tool loop; writes TICKET_AGENT_HARNESS_ARN
python 04-invoke-everything.py                 # one surface: session, second turn, new session, qualifier, StopRuntimeSession
python 05-versions-and-endpoints.py --keep     # V2 minted by an update; `stable` pinned to V1, promoted, rolled back
jupyter nbconvert --execute 01-walkthrough.ipynb   # optional, same calls as cells
python 02-runtime-code-deploy.py --cleanup && python 01-harness-sdk.py --cleanup   # when B04/B05 are done with them
```

## What each script proves
- **03** The loop is a Strands `Agent` on `BedrockModel`; the >250 GBP rule lives in the tool, so the model cannot talk its way past it. No ARN anywhere.
- **02** `create_agent_runtime` with `codeConfiguration` (zip at S3, `PYTHON_3_13`, `entryPoint ["main.py"]`) is the whole deploy. The container contract is satisfied by `BedrockAgentCoreApp` (`/invocations`, `/ping`, 8080). `platformVersion="V2"` opts into snapshot cold starts.
- **01** `create_harness` stores model, prompt and tools server-side. Inline tools come back as `toolUse` blocks in a Converse-shaped stream and you answer with `toolResult`. The gateway tool type is where you go when tools must not run in the caller.
- **04** `runtimeSessionId` is the only state handle; same id = same microVM and conversation, new id = clean slate. `qualifier` picks `DEFAULT` or a named endpoint. `StopRuntimeSession` ends it early.
- **05** `update_agent_runtime` always mints a version. `DEFAULT` follows latest. A named endpoint is the rollback pointer; nothing else moves.

## Proof checklist (tick with real output)
- [ ] `03` prints an issued 4.50 refund and a refused 480 refund
- [ ] `02` prints `status=READY` and `.env` has `TICKET_AGENT_RUNTIME_ARN`
- [ ] `01` prints at least one `tool get_ticket(...)` line and a final answer; `.env` has `TICKET_AGENT_HARNESS_ARN`
- [ ] `04` turn 2 knows the name, the new session does not; `qualifier=stable` fails before 05 and works after `05 --keep`
- [ ] `05` prints `versions: ['1', '2']`, `stable -> 1`, `promoted stable -> 2`, `rolled back stable -> 1`
- [ ] CloudWatch log group `/aws/bedrock-agentcore/runtimes/<id>-DEFAULT` exists (B05 picks it up)
