"""One invocation surface. Call every agent in this repo the same way and show the four
Responses-API controls that matter in production: conversation, previous_response_id,
stream, background.

Agents are looked up by name; those that do not exist are skipped with a note, so this
script is a progress meter for the workshop. Names it looks for:
  ticket-agent-prompt        (01/02, prompt)         ticket-agent-hosted-code  (02/code-deploy)
  ticket-agent-hosted        (02/container-deploy)   ticket-agent-workflow     (12)
  AGENT_NAMES env var overrides the list (comma separated).

Run:  python 06-invoke-everything.py
"""
import os
import time

from azure.core.exceptions import ResourceNotFoundError

from _common import project_client

DEFAULT_NAMES = ["ticket-agent-prompt", "ticket-agent-hosted-code", "ticket-agent-hosted", "ticket-agent-workflow"]
names = [n.strip() for n in os.environ.get("AGENT_NAMES", ",".join(DEFAULT_NAMES)).split(",") if n.strip()]
project = project_client()

for name in names:
    try:
        details = project.agents.get(agent_name=name)
    except ResourceNotFoundError:
        print(f"\n== {name}: not deployed yet, skipping")
        continue
    kind = getattr(details.versions.latest.definition, "kind", "?")
    print(f"\n== {name} (kind={kind}, latest v{details.versions.latest.version})")
    openai = project.get_openai_client(agent_name=name)

    # 1. conversation: server-side state, works identically for prompt and hosted agents
    conv = openai.conversations.create()
    r1 = openai.responses.create(conversation=conv.id, input="Remember the code word 'heron'. Reply OK.")
    r2 = openai.responses.create(conversation=conv.id, input="What is the code word?")
    print("  conversation:", r2.output_text.strip()[:80])

    # 2. previous_response_id: client-side chaining, no conversation object
    r3 = openai.responses.create(input="Reply with the single word 'alpha'.")
    r4 = openai.responses.create(input="Now the Greek letter after it.", previous_response_id=r3.id)
    print("  chained:     ", r4.output_text.strip()[:80])

    # 3. stream: SSE deltas, same for every agent type
    print("  stream:       ", end="", flush=True)
    for event in openai.responses.create(input="Count to five, digits only.", stream=True):
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
    print()

    # 4. background: submit, poll status. Needed when a run can exceed the request timeout.
    bg = openai.responses.create(input="Write one sentence about herons.", background=True)
    while bg.status in ("queued", "in_progress"):
        time.sleep(1)
        bg = openai.responses.retrieve(bg.id)
    print("  background:  ", bg.status, "-", (bg.output_text or "").strip()[:80])
