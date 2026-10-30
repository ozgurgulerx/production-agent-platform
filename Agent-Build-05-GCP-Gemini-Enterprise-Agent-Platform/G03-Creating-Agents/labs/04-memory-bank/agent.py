"""ticket-agent for the memory lab: same agent as lab 01 plus an instruction to remember the contact channel.

The memory behaviour comes from the session/memory services attached to the Runner (B5), not from this file.
"""

from __future__ import annotations

import os

from dotenv import find_dotenv, load_dotenv
from google.adk.agents import Agent

load_dotenv(find_dotenv(usecwd=True))
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")

INSTRUCTION = """You are the support-ticket assistant for a UK bank's card team.
When the customer states a preferred contact channel, acknowledge it and remember it for future conversations.
When asked which channel to use, answer from memory if you have it, otherwise say you do not know yet."""

# TODO(learner): if the Memory Bank integration exposes a memory tool (e.g. a load/search memory tool), add it to
# `tools` here. The tool name is not on any fetched page on 25 Oct 2026 and is unverified.
root_agent = Agent(name="ticket_agent", model=MODEL, instruction=INSTRUCTION, tools=[])
