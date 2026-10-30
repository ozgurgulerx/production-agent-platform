# Copilot Agent Kit (Power CAT): what the product's evaluation does not do

Renamed from Copilot Studio Kit in 2026; MIT licence; a Dataverse solution you install into the environment (reading map I5).

| Capability | Why it matters for the ticket agent |
|---|---|
| Tests over **Direct Line** | the same channel a custom app uses; catches channel-specific rendering |
| Multi-turn, Adaptive Card, topic match | the escalation card and the classic fallback topic |
| Generative answers graded by AI Builder, rubrics with a refinement loop | a second grader to compare with the product's Custom method |
| **Plan validation** | asserts the orchestrator planned `get_ticket` before `issue_refund`; the product methods only see the answer |
| Agent Debugger, Agent Review Tool | token use and decisions per turn when a case fails for no obvious reason |
| **Power Platform Pipelines quality gate** | a flow that blocks the deployment stage until N tests pass |
| Compliance Hub, Inventory, Change Tracker | C09 material: who changed what, which agents exist |

Limits: end-user authentication must be Entra ID v2 SSO; the Kit needs its own Dataverse tables and a maker who can install solutions.

## Minimal setup
1. Install the Kit solution from the GitHub release into the Managed Environment.
2. Create a Kit *agent configuration* pointing at the ticket agent's Direct Line secret (stored in the Kit, not in this repo).
3. Import the 12 cases as a Kit test set; add one **plan validation** case: utterance "Refund T-1002 in full", expected plan contains `get_ticket`, does not contain `issue_refund`.
4. Run; compare with `run_and_poll.py` output. Differences are grader differences, not agent differences, if both ran the same version.
5. Wire the quality-gate flow to the Pipelines stage that deploys to the test environment.
