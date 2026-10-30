#!/usr/bin/env python3
"""
Deploy 2-Agent Workflow to Azure AI Foundry

Creates a workflow that connects analyzer-agent → responder-agent:
  - analyzer-agent: Analyzes customer inquiry (category, sentiment, urgency)
  - responder-agent: Crafts customer response based on analysis

Usage:
    python deploy_workflow.py          # Deploy workflow
    python deploy_workflow.py --test   # Test workflow
    python deploy_workflow.py --delete # Delete workflow
"""

import os
import argparse

# Load environment
def load_env_file(path):
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if key.strip() not in os.environ:
                        os.environ[key.strip()] = value.strip().strip('"').strip("'")

for _up in ["", "../", "../../", "../../../", "../../../../", "../../../../../"]:
    load_env_file(_up + ".env")  # .env lives at the track root

# Configuration
PROJECT_ENDPOINT = os.environ.get(
    "AZURE_AI_PROJECT_ENDPOINT",
    "https://ozgurguler-7212-resource.services.ai.azure.com/api/projects/ozgurguler-7212"
)
WORKFLOW_NAME = "customer-support-workflow"

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

# Workflow YAML - 2 agents, output of first feeds into second
WORKFLOW_YAML = '''kind: workflow
trigger:
  kind: OnConversationStart
  id: trigger_workflow
  actions:
    # Step 1: Analyzer examines the customer inquiry
    - kind: InvokeAzureAgent
      id: analyzer-step
      agent:
        name: analyzer-agent
      conversationId: =System.ConversationId
      input:
        messages: =System.LastMessage.Text
      output:
        messages: Local.Analysis

    # Step 2: Responder uses analysis to craft response
    - kind: InvokeAzureAgent
      id: responder-step
      agent:
        name: responder-agent
      conversationId: =System.ConversationId
      input:
        messages: =Local.Analysis
      output:
        autoSend: true
        messages: Local.FinalResponse

    - kind: EndConversation
      id: end-workflow

id: ""
name: customer-support-workflow
description: "2-Agent Workflow: Analyzer -> Responder"
'''


def get_client():
    """Get Azure AI Project client."""
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient

    return AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential()
    )


def deploy_workflow(client):
    """Deploy the workflow."""
    from azure.ai.projects.models import WorkflowAgentDefinition

    print(f"\n{CYAN}Deploying: {WORKFLOW_NAME}{RESET}")
    print(f"{DIM}─────────────────────────────────────{RESET}")
    print(f"\n{DIM}Agents:{RESET}")
    print(f"  • analyzer-agent  → responder-agent")

    try:
        result = client.agents.create_version(
            agent_name=WORKFLOW_NAME,
            description='2-Agent Workflow: Analyzer -> Responder',
            definition=WorkflowAgentDefinition(workflow=WORKFLOW_YAML),
        )
        version = result.version if hasattr(result, "version") else "?"
        print(f"\n{GREEN}✓ Deployed workflow v{version}{RESET}")
        return True
    except Exception as e:
        print(f"\n{RED}✗ Failed: {str(e)}{RESET}")
        return False


def test_workflow(client):
    """Test the workflow."""
    print(f"\n{CYAN}{BOLD}Testing 2-Agent Workflow{RESET}\n")

    openai_client = client.get_openai_client()
    query = "I was charged twice for my subscription and the app crashes when uploading files"

    print(f"{BOLD}Query:{RESET} {query}\n")

    # Test analyzer
    print(f"1. {BOLD}analyzer-agent{RESET}...", end=" ", flush=True)
    try:
        response = openai_client.responses.create(
            extra_body={"agent": {"name": "analyzer-agent", "type": "agent_reference"}},
            input=query,
        )
        analysis = response.output_text if hasattr(response, "output_text") else str(response)
        print(f"{GREEN}✓{RESET}")
        print(f"   {DIM}{analysis[:120].replace(chr(10), ' ')}...{RESET}")
    except Exception as e:
        print(f"{RED}✗{RESET} {str(e)[:50]}")
        return

    # Test responder with analysis
    print(f"\n2. {BOLD}responder-agent{RESET} (using analysis)...", end=" ", flush=True)
    try:
        response = openai_client.responses.create(
            extra_body={"agent": {"name": "responder-agent", "type": "agent_reference"}},
            input=analysis,
        )
        final = response.output_text if hasattr(response, "output_text") else str(response)
        print(f"{GREEN}✓{RESET}")
        print(f"   {DIM}{final[:120].replace(chr(10), ' ')}...{RESET}")
    except Exception as e:
        print(f"{RED}✗{RESET} {str(e)[:50]}")

    print(f"\n{BOLD}View workflow in portal:{RESET}")
    print(f"  Build → Workflows → {WORKFLOW_NAME}")


def delete_workflow(client):
    """Delete the workflow."""
    print(f"\n{RED}Deleting: {WORKFLOW_NAME}{RESET}")
    try:
        client.agents.delete(agent_name=WORKFLOW_NAME)
        print(f"{GREEN}✓ Deleted{RESET}")
    except Exception as e:
        print(f"{DIM}Not found: {str(e)[:40]}{RESET}")


def main():
    parser = argparse.ArgumentParser(description="Deploy 2-Agent Workflow")
    parser.add_argument("--test", action="store_true", help="Test workflow")
    parser.add_argument("--delete", action="store_true", help="Delete workflow")
    args = parser.parse_args()

    print(f"""
{CYAN}{BOLD}╔════════════════════════════════════════════╗
║     2-Agent Workflow - Azure AI Foundry    ║
╚════════════════════════════════════════════╝{RESET}

{DIM}Project:{RESET}  {PROJECT_ENDPOINT.split('/')[-1]}
{DIM}Workflow:{RESET} {WORKFLOW_NAME}
""")

    client = get_client()

    if args.test:
        test_workflow(client)
    elif args.delete:
        delete_workflow(client)
    else:
        if deploy_workflow(client):
            print(f"\n{BOLD}Next:{RESET} python deploy_workflow.py --test")


if __name__ == "__main__":
    main()
