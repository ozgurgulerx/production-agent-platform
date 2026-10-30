"""Stand-in for the G03 lab 03 ticket-agent-workflow when running this lab alone (map B2).
Status: scaffold only, functionality unverified."""
import os

from google.adk.agents import LlmAgent, SequentialAgent

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")

triage = LlmAgent(name="triage", model=GEMINI_MODEL, output_key="triage",
                  instruction="Classify the ticket severity (low/medium/high) and say why.")
policy = LlmAgent(name="policy_check", model=GEMINI_MODEL, output_key="policy",
                  instruction="Given {triage}, state whether a refund is inside policy (<= 50, <= 30 days). Cite 'Refund policy v3 §2.1'. Never issue a refund.")
reply = LlmAgent(name="reply_draft", model=GEMINI_MODEL,
                 instruction="Draft a two-sentence customer reply from {triage} and {policy}.")

root_agent = SequentialAgent(name="ticket_agent_workflow", sub_agents=[triage, policy, reply],
                             description="Triage, policy check and reply draft for a support ticket.")
