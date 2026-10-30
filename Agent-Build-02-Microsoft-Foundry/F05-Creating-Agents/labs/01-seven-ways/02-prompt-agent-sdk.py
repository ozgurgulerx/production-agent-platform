"""Way 2 — Prompt agent created with the Projects SDK, invoked through the Responses API.

The definition (model, instructions, tools) lives in Foundry as an immutable version.
Foundry runs the loop. You call it through the one invocation surface: POST /responses.

Run:  python 02-prompt-agent-sdk.py [--keep]
Proof: prints the created version, a two-turn conversation on the server side, the
       version list, and (unless --keep) deletes the agent.
"""
import sys

from azure.ai.projects.models import PromptAgentDefinition

from _common import MODEL, SUPPORT_INSTRUCTIONS, delete_agent, get_or_create, project_client

AGENT_NAME = "ticket-agent-prompt"

project = project_client()

# 1. Definition stored in Foundry. Tools are added in F04; here it is model + instructions.
definition = PromptAgentDefinition(model=MODEL, instructions=SUPPORT_INSTRUCTIONS)
agent = get_or_create(project, AGENT_NAME, definition)

# 2. Invoke. get_openai_client(agent_name=...) returns an OpenAI client pre-bound to the
#    agent endpoint, so you do not pass model/instructions and you do not need extra_body.
openai = project.get_openai_client(agent_name=AGENT_NAME)
conversation = openai.conversations.create()            # server-side state
r1 = openai.responses.create(conversation=conversation.id, input="My card was charged twice for order 8841.")
print("turn 1:", r1.output_text)
r2 = openai.responses.create(conversation=conversation.id, input="What did I just tell you the order number was?")
print("turn 2:", r2.output_text)                          # proves the conversation carried state

# 3. Same thing without a conversation object: chain by previous_response_id.
r3 = openai.responses.create(input="Say 'ready' and nothing else.")
r4 = openai.responses.create(input="Repeat what you just said.", previous_response_id=r3.id)
print("chained:", r4.output_text)

# 4. Versions are immutable and listable. Refer to one as name:version when you must pin.
versions = list(project.agents.list_versions(agent_name=AGENT_NAME))
print("versions:", [v.version for v in versions])

# 5. Cleanup unless asked to keep it (06-invoke-everything.py and 07 reuse it).
if "--keep" not in sys.argv:
    delete_agent(project, AGENT_NAME)
