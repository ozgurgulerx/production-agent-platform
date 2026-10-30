"""Multi-agent as ONE hosted agent: an Agent Framework workflow wrapped with .as_agent() and
served by ResponsesHostServer. Callers see a single Responses endpoint; inside, three agents run
in sequence (triage -> specialist -> responder) with each step seeing only the previous output.

This replaces the Foundry declarative workflow (kind: workflow YAML) that this folder deployed in
2025. Foundry retires those on 1 Dec 2026; see ../../appendix-foundry-workflow-retiring-2026-12-01/ (lab 03).
"""
import os

from agent_framework import Agent, AgentExecutor, WorkflowBuilder
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


def build_workflow_agent():
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME") or os.environ["FOUNDRY_MODEL"],
        credential=DefaultAzureCredential(),
    )
    triage = Agent(
        client=client, name="triage",
        instructions=("Classify the customer message as BILLING, TECHNICAL or GENERAL and extract: "
                      "ticket/order ids, amounts, urgency (low/med/high). Output 4 short lines: "
                      "category, ids, amounts, urgency, then the original message verbatim."),
    )
    specialist = Agent(
        client=client, name="specialist",
        instructions=("You are the back-office specialist. Given the triage note, decide the action "
                      "(refund, escalate, explain, ask-for-info) and write the internal resolution in 3 lines. "
                      "For duplicate card charges the policy is: refund the duplicate within 5 working days."),
    )
    responder = Agent(
        client=client, name="responder",
        instructions=("Write the customer-facing reply for a UK bank card team: warm, brief, no internal jargon, "
                      "state the action and the timeline. Sign off as 'Card Services'."),
    )
    # context_mode="last_agent": each executor sees only the previous step's output, not the whole history
    t, s, r = (AgentExecutor(a, context_mode="last_agent") for a in (triage, specialist, responder))
    return (
        WorkflowBuilder(start_executor=t, output_executors=[r])   # only the responder's text is the output
        .add_edge(t, s)
        .add_edge(s, r)
        .build()
        .as_agent(name="ticket-agent-workflow")
    )


if __name__ == "__main__":
    ResponsesHostServer(build_workflow_agent()).run()
