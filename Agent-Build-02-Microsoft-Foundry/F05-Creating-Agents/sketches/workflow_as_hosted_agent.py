"""Untested sketch. Multi-agent = Agent Framework workflow wrapped as one agent, served on :8088.
Runnable: ../labs/03-multi-agent-workflow/src/ticket-workflow/main.py. Foundry declarative workflows retire 2026-12-01."""
from agent_framework import Agent, AgentExecutor, WorkflowBuilder
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential

client = FoundryChatClient(project_endpoint="...", model="gpt-5-mini", credential=DefaultAzureCredential())
t, s, r = (AgentExecutor(Agent(client=client, name=n, instructions=i), context_mode="last_agent")
           for n, i in (("triage", "classify"), ("specialist", "decide"), ("responder", "reply")))
ResponsesHostServer(WorkflowBuilder(start_executor=t, output_executors=[r]).add_edge(t, s).add_edge(s, r).build().as_agent()).run()
