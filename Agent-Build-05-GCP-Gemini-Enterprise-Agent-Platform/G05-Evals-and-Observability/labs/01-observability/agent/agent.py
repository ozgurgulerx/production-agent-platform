"""ticket-agent for G05 lab 01: same agent as G03/G04, plus a before_tool_callback that logs every tool call (map B4)
and explicit Gemini safety settings (map F3). Model and MCP URL come from .env; ADC only.

Deployed with: adk deploy agent_engine ... --otel_to_cloud agent   (map B6, E4)
"""
import logging
import os

from dotenv import find_dotenv, load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.genai import types

load_dotenv(find_dotenv(usecwd=True))
log = logging.getLogger("ticket-agent")
logging.basicConfig(level=logging.INFO)  # stdout → reasoning_engine_stdout in Cloud Logging (map E6)

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
TICKET_MCP_URL = os.environ.get("TICKET_MCP_URL", "")

INSTRUCTION = """You are the support ticket agent. Look tickets up with the ticketing tool before answering.
Refunds are allowed only within 30 days of purchase; refuse anything outside that and say why.
Cite the policy document you relied on."""


def log_tool_call(tool, args, tool_context):
    """before_tool_callback (map B4). Returning None lets the call proceed.

    TODO(learner): log tool name and args (not customer text) with the engine id from GOOGLE_CLOUD_AGENT_ENGINE_ID (map E6).
    """
    raise NotImplementedError


# Explicit threshold because the default is OFF on gemini-3.5-flash and later (map F3).
# TODO(learner): the google-genai class names SafetySetting / HarmCategory / HarmBlockThreshold are not in the map; confirm in the SDK.
SAFETY = types.GenerateContentConfig(
    safety_settings=[
        types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
    ]
)

tools = []
if TICKET_MCP_URL:
    # Defined synchronously in agent.py (map D3). Auth headers as in G04 lab 03.
    tools.append(McpToolset(connection_params=StreamableHTTPConnectionParams(url=TICKET_MCP_URL), tool_filter=["lookup_ticket"]))

root_agent = LlmAgent(
    name="ticket_agent",
    model=MODEL,
    description="Answers customer support tickets, refuses refunds outside policy, cites policy documents.",
    instruction=INSTRUCTION,
    tools=tools,
    generate_content_config=SAFETY,
    before_tool_callback=log_tool_call,
)
