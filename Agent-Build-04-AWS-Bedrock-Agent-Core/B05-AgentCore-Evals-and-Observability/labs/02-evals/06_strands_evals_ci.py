"""Proves: the pre-release gate. Strands Evals runs the dataset against the local Strands twin of the ticket
agent (same prompt, same tools as B03 lab 01) with three evaluators and exits non-zero under threshold.

No Runtime needed; only Bedrock access for the agent model and the judge. Same evaluator names as the online
config so the two numbers are comparable.
"""
import sys
from strands import Agent, tool
from strands.models import BedrockModel
from strands_evals import Case, Experiment
from strands_evals.evaluators import GoalSuccessRateEvaluator, OutputEvaluator, ToolSelectionAccuracyEvaluator
from _common import JUDGE_MODEL_ID, MODEL_ID, REGION, load_cases, session

TICKETS = {"T-1001": {"customer": "Ayşe", "amount": 120.0, "status": "open", "card_country": "GB"},
           "T-1002": {"customer": "Mert", "amount": 400.0, "status": "open", "card_country": "GB"},
           "T-1003": {"customer": "Lucía", "amount": 90.0, "status": "open", "card_country": "PE"}}
POLICY = "Refunds up to 250 GBP on GB cards directly; above that or non-GB cards escalate to the UK card team."


@tool
def get_ticket(ticket_id: str) -> dict:
    """Return the support ticket with the given id."""
    return TICKETS.get(ticket_id, {"error": "not found"})


@tool
def list_tickets(customer: str) -> list:
    """Open tickets for a customer name."""
    return [k for k, v in TICKETS.items() if v["customer"].lower() == customer.lower()]


@tool
def get_policy() -> str:
    """The refund policy text."""
    return POLICY


@tool
def issue_refund(ticket_id: str, amount: float) -> str:
    """Refund the ticket; the policy applies."""
    t = TICKETS.get(ticket_id)
    if not t or amount > 250 or amount > t["amount"] or t["card_country"] != "GB":
        return "REFUSED: outside policy, escalate to the UK card team"
    return f"refunded {amount} GBP on {ticket_id}"


def make_agent() -> Agent:
    return Agent(model=BedrockModel(model_id=MODEL_ID, boto_session=session(), region_name=REGION),
                 system_prompt="You are the UK support-ticket assistant. Use the tools. " + POLICY + " Never reveal card numbers.",
                 tools=[get_ticket, list_tickets, get_policy, issue_refund])


def task(case: Case):
    agent = make_agent()                                   # fresh agent per case
    result = agent(case.input)
    tools = [b["toolUse"]["name"] for m in agent.messages for b in m.get("content", []) if "toolUse" in b]
    return {"output": str(result), "trajectory": tools}


cases = [Case(name=c["id"], input=c["input"], expected_output=c["expected_output"],
              expected_assertion=c["assertion"], expected_trajectory=c["expected_tools"]) for c in load_cases()]
judge = BedrockModel(model_id=JUDGE_MODEL_ID, boto_session=session(), region_name=REGION)
experiment = Experiment(cases=cases, evaluators=[
    ToolSelectionAccuracyEvaluator(model=judge),
    GoalSuccessRateEvaluator(model=judge),
    OutputEvaluator(rubric="Pass if the response follows this policy: " + POLICY + " Score 0-1.", model=judge),
])
report = experiment.run_evaluations(task)
report.display()
THRESHOLD = float(sys.argv[sys.argv.index("--threshold") + 1]) if "--threshold" in sys.argv else 0.8
scores = [r.score for r in getattr(report, "cases", []) if getattr(r, "score", None) is not None]   # verify report fields
mean = sum(scores) / len(scores) if scores else 0.0
print(f"\nmean score {mean:.3f} over {len(scores)} (case, evaluator) rows; threshold {THRESHOLD}")
sys.exit(0 if mean >= THRESHOLD else 1)
