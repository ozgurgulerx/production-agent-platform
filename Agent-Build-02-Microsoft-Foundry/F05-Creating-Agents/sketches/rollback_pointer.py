"""Untested sketch. Rollback is a pointer: one version serves 100% of traffic. Runnable: ../labs/01-seven-ways/07-versions-and-publish.py."""
from azure.ai.projects.models import AgentEndpointConfig, FixedRatioVersionSelectionRule, VersionSelector

def route_to(project, agent_name: str, version: str) -> None:
    project.agents.update_details(agent_name=agent_name, agent_endpoint=AgentEndpointConfig(
        version_selector=VersionSelector(version_selection_rules=[
            FixedRatioVersionSelectionRule(agent_version=version, traffic_percentage=100)])))
