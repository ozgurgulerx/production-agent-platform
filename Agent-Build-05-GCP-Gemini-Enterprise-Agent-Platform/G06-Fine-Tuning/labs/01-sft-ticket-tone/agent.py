"""ticket-agent-tuned: the G03 ticket agent with one line changed, the model string (map G9).

Needs TUNED_ENDPOINT in .env after submit_sft.py prints it, ADC, and GOOGLE_GENAI_USE_ENTERPRISE=TRUE (G9; the
track also sets GOOGLE_GENAI_USE_VERTEXAI=TRUE, which of the two ADK 2.13.0 reads for endpoint models is unverified).
Run:  adk run .      or      adk eval . "$EVALSET" --config_file_path "$EVAL_CONFIG"
"""

import os

from dotenv import find_dotenv, load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

load_dotenv(find_dotenv(usecwd=True))  # .env at the track root (walks up)

MODEL = os.environ.get("TUNED_ENDPOINT") or os.environ.get(
    "GEMINI_LITE_MODEL", "gemini-3.5-flash-lite"
)
# TUNED_ENDPOINT form: projects/P/locations/eu/endpoints/ENDPOINT_ID (map G4, G9). Unset falls back to the base lite model
# so the same folder can serve as the "base" side of the comparison if the G03 agent is not to hand.

INSTRUCTION = (
    "You are the UK card team's support assistant. Warm, brief, British English, no exclamation marks. "
    "Use the ticket tools to look tickets up; never invent amounts or dates. "
    "Refunds above 250 GBP need a second approver: refuse, say why in one clause, and say it has been flagged."
)

tools = []
if os.environ.get("TICKET_MCP_URL"):
    # The G04 lab 03 MCP Toolbox on Cloud Run. Defined synchronously in agent.py as map D3 requires.
    tools.append(
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=os.environ["TICKET_MCP_URL"]
            ),
            tool_filter=["get_ticket", "list_tickets"],
        )
    )

root_agent = LlmAgent(
    name="ticket_agent_tuned",
    model=MODEL,
    description="Support ticket agent on the tuned gemini-3.5-flash-lite endpoint.",
    instruction=INSTRUCTION,
    tools=tools,
)
