"""F05 step 5 — AI red teaming in the cloud against the agent target. Run: python 05_red_team.py"""
import time

from azure.ai.projects.models import AttackStrategy, AzureAIAgentTarget, RedTeam, RiskCategory

from _common import AGENT_NAME, agent_version, project_client

project = project_client(allow_preview=True)
scan = project.beta.red_teams.create(
    red_team=RedTeam(
        display_name=f"{AGENT_NAME} red team",
        target=AzureAIAgentTarget(name=AGENT_NAME, version=agent_version(project)),
        risk_categories=[RiskCategory.PROHIBITED_ACTIONS, RiskCategory.SENSITIVE_DATA_LEAKAGE, RiskCategory.HATE_UNFAIRNESS],
        attack_strategies=[AttackStrategy.BASELINE, AttackStrategy.JAILBREAK, AttackStrategy.BASE64, AttackStrategy.MULTI_TURN],
        num_turns=3,
        application_scenario="UK bank card-team support assistant; must never refund outside policy or reveal other customers' data",
    )
)
print("scan", scan.name, scan.status)
while scan.status in ("Queued", "Running", "queued", "running", "in_progress"):
    time.sleep(30)
    scan = project.beta.red_teams.get(name=scan.name)
    print("  ", scan.status)
print("done:", scan.status, "- open the Red teaming tab in the portal for attack-success-rate per category")
