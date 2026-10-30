"""G03 section 4: the four multi-agent shapes as one `root_agent` each. Untested sketch.

Sequential, Loop and Parallel from map B2; custom BaseAgent from B3. Graph workflows are "new in ADK 2.0"
(A8) and supersede template workflows (B2), but the API is on no fetched page, so that slot is a comment.
Whatever the shape, deployment is the way-5 command on the one `root_agent` (C2).
"""

from __future__ import annotations

import os
from typing import AsyncGenerator

from google.adk.agents import (
    Agent,
    BaseAgent,
    LoopAgent,
    ParallelAgent,
    SequentialAgent,
)
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event

MODEL = os.environ.get(
    "GEMINI_MODEL", "gemini-3.5-flash"
)  # from .env, never hard-coded in labs

# --- state hand-off: output_key on one agent, {placeholder} in the next instruction (B2) ---------------
triage = Agent(
    name="triage",
    model=MODEL,
    output_key="category",
    instruction="Classify the ticket as billing, card, or other. Reply with the single word.",
)
lookup = Agent(
    name="lookup",
    model=MODEL,
    output_key="facts",
    instruction="Category: {category}. List the facts needed to answer. Do not answer yet.",
)
reply = Agent(
    name="reply",
    model=MODEL,
    instruction="Facts: {facts}. Write the customer reply. Refuse any refund outside policy.",
)

# 1. Sequential: fixed order, one trace tree, one resource when deployed (B2)
ticket_workflow = SequentialAgent(
    name="ticket_agent_workflow", sub_agents=[triage, lookup, reply]
)

# 2. Loop: refine until a checker is satisfied. The exit mechanism is on a page not fetched on 25 Oct 2026
#    (map Gaps); `max_iterations` is assumed, unverified.
checker = Agent(
    name="checker",
    model=MODEL,
    output_key="verdict",
    instruction="Say PASS if the reply cites a policy document, else say what is missing.",
)
refine_loop = LoopAgent(
    name="refine", sub_agents=[reply, checker], max_iterations=3
)  # unverified kwarg

# 3. Parallel: independent lookups, each writes its own output_key (B2)
fanout = ParallelAgent(
    name="fanout",
    sub_agents=[
        Agent(
            name="policy_facts",
            model=MODEL,
            output_key="policy",
            instruction="Summarise the refund policy.",
        ),
        Agent(
            name="account_facts",
            model=MODEL,
            output_key="account",
            instruction="Summarise the account state.",
        ),
    ],
)


# 4. Custom orchestration: subclass BaseAgent, override _run_async_impl, yield Events (B3)
class TicketRouter(BaseAgent):
    """Branch on ticket category from session state; one parent_agent per child (B3)."""

    billing: Agent
    card: Agent

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        category = ctx.session.state.get("category", "other")
        # TODO(learner): pick `self.billing` or `self.card` from `category` and
        # `async for event in <child>.run_async(ctx): yield event`. Write the state you want downstream agents
        # to see into ctx.session.state; the Runner commits the delta per event (B5).
        raise NotImplementedError


# 5. Graph workflow (ADK 2.0): API not on any fetched page; unverified. Keep the template agents above until
#    adk.dev's graph page is in the reading map.

root_agent = ticket_workflow  # what `adk deploy agent_engine` picks up; one resource for three agents
