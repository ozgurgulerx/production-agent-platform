"""# B03 lab 01 — the ticket agent, every way AgentCore allows

Run top to bottom after `labs-setup/` is done. Each cell is one of the scripts in this folder,
inlined, so you can see the data-plane calls change shape (or not) as the way of building changes.
Nothing is created unless you run the create cells; everything created is deleted at the end.
"""
# %% [markdown]
# ## 0. Session, clients, model
# %%
from _common import MODEL_ID, REGION, control, data, new_session_id, read_body
cp, dp = control(), data()
print(REGION, MODEL_ID, "session id example:", new_session_id())

# %% [markdown]
# ## 1. Ephemeral: Strands in this kernel, Bedrock Converse underneath, nothing registered
# %%
import sys; sys.path.insert(0, "agent")
from main import INSTRUCTIONS, get_policy, get_ticket, issue_refund, list_tickets
from strands import Agent
from strands.models import BedrockModel
local = Agent(model=BedrockModel(model_id=MODEL_ID), system_prompt=INSTRUCTIONS, tools=[get_ticket, list_tickets, get_policy, issue_refund])
print(local("Refund the full 480 on T-1003."))

# %% [markdown]
# ## 2. Runtime from code: see 02-runtime-code-deploy.py; here we only list what exists
# %%
for rt in cp.list_agent_runtimes(maxResults=50)["agentRuntimes"]:
    print(rt["agentRuntimeName"], rt["agentRuntimeVersion"], rt["status"], rt["agentRuntimeArn"])

# %% [markdown]
# ## 3. Invoke through the one surface (needs TICKET_AGENT_RUNTIME_ARN from the script)
# %%
import json, os
arn = os.environ.get("TICKET_AGENT_RUNTIME_ARN")
if arn:
    sid = new_session_id()
    for prompt in ["I am Mert. What is T-1002 about?", "Remind me of my name."]:
        r = dp.invoke_agent_runtime(agentRuntimeArn=arn, runtimeSessionId=sid, qualifier="DEFAULT",
                                    contentType="application/json", accept="application/json, text/event-stream",
                                    payload=json.dumps({"prompt": prompt}).encode())
        print(prompt, "->", read_body(r))
else:
    print("run 02-runtime-code-deploy.py --keep first")

# %% [markdown]
# ## 4. Versions and endpoints: what moves when you roll back
# %%
if arn:
    rid = arn.rsplit("/", 1)[-1]
    print([v["agentRuntimeVersion"] for v in cp.list_agent_runtime_versions(agentRuntimeId=rid)["agentRuntimes"]])
    print([(e["name"], e["liveVersion"]) for e in cp.list_agent_runtime_endpoints(agentRuntimeId=rid)["runtimeEndpoints"]])

# %% [markdown]
# ## 5. Harness: the managed loop (needs TICKET_AGENT_HARNESS_ARN from 01-harness-sdk.py --keep)
# %%
harn = os.environ.get("TICKET_AGENT_HARNESS_ARN")
if harn:
    out = []
    for ev in dp.invoke_harness(harnessArn=harn, runtimeSessionId=new_session_id(),
                                messages=[{"role": "user", "content": [{"text": "List the policies you know."}]}])["stream"]:
        if "contentBlockDelta" in ev and "text" in ev["contentBlockDelta"]["delta"]:
            out.append(ev["contentBlockDelta"]["delta"]["text"])
    print("".join(out))

# %% [markdown]
# ## 6. Cleanup: `python 02-runtime-code-deploy.py --cleanup` and `python 01-harness-sdk.py --cleanup`
