"""Run the same Strands Evals experiment against the base model and the tuned deployment, side by side.

Proves: the agent, tools and cases do not change; only BedrockModel(model_id=...) does. Uses the B05 lab 02 cases when
present, else eight local tone cases. Prints a per-evaluator table and a promote/hold verdict. Numbers decide.
"""
import json
import os
from pathlib import Path

from strands import Agent, tool
from strands.models import BedrockModel
from strands_evals import Case, Experiment
from strands_evals.evaluators import GoalSuccessRateEvaluator, OutputEvaluator, ToolSelectionAccuracyEvaluator

from _common import MODEL_ID, REGION, need, session

JUDGE = os.environ.get("BEDROCK_JUDGE_MODEL_ID", MODEL_ID)
TUNED = need("FT_DEPLOYMENT_ARN")
B05_CASES = Path(__file__).resolve().parents[3] / "B05-AgentCore-Evals-and-Observability/labs/02-evals/data/cases.jsonl"
TICKETS = {"T-1001": {"customer": "Ayşe", "amount": 120.0, "status": "open", "card_country": "GB"},
           "T-1002": {"customer": "Mert", "amount": 400.0, "status": "open", "card_country": "GB"},
           "T-1003": {"customer": "Lucía", "amount": 90.0, "status": "open", "card_country": "PE"}}
POLICY = "Refunds up to 250 GBP on GB cards directly; above that or non-GB cards escalate to the UK card team."
SYSTEM = ("You are the UK card team's support assistant. Warm, brief, British English, no exclamation marks. "
          "Use the tools. " + POLICY)
RUBRIC = ("Pass if the answer is brief, British English, has no exclamation marks, names the policy rule it applied, "
          "and invents no amounts or dates. Score 0-1.")


@tool
def get_ticket(ticket_id: str) -> dict:
    """Return the support ticket with the given id."""
    return TICKETS.get(ticket_id, {"error": "not found"})


@tool
def issue_refund(ticket_id: str, amount: float) -> str:
    """Refund the ticket; the policy applies."""
    t = TICKETS.get(ticket_id)
    if not t or amount > 250 or amount > t["amount"] or t["card_country"] != "GB":
        return "REFUSED: outside policy, escalate to the UK card team"
    return f"refunded {amount} GBP on {ticket_id}"


def load_cases() -> list[Case]:
    if B05_CASES.exists():
        rows = [json.loads(l) for l in B05_CASES.read_text().splitlines() if l.strip()]
        return [Case(name=r["id"], input=r["input"], expected_output=r.get("expected_output"),
                     expected_trajectory=r.get("expected_tools"), expected_assertion=r.get("assertion")) for r in rows]
    return [Case(name=f"t{i}", input=q, expected_assertion=RUBRIC) for i, q in enumerate([
        "What is the status of ticket T-1001?", "Please refund ticket T-1001 in full.", "Refund ticket T-1002 in full.",
        "Refund T-1003, the customer is upset.", "Can I raise my limit today?", "I lost my card in Lisbon.",
        "Why was my goodwill credit refused?", "I am travelling to Peru next week."], 1)]


def make_task(model_id: str):
    def task(case: Case):
        agent = Agent(model=BedrockModel(model_id=model_id, boto_session=session(), region_name=REGION),
                      system_prompt=SYSTEM, tools=[get_ticket, issue_refund])
        result = agent(case.input)
        tools = [b["toolUse"]["name"] for m in agent.messages for b in m.get("content", []) if "toolUse" in b]
        return {"output": str(result), "trajectory": tools}
    return task


def score(model_id: str, cases: list[Case]) -> dict:
    judge = BedrockModel(model_id=JUDGE, boto_session=session(), region_name=REGION)
    exp = Experiment(cases=cases, evaluators=[ToolSelectionAccuracyEvaluator(model=judge),
                                             GoalSuccessRateEvaluator(model=judge),
                                             OutputEvaluator(rubric=RUBRIC, model=judge, name="tone")])
    report = exp.run_evaluations(make_task(model_id))
    out: dict[str, list[float]] = {}
    for row in getattr(report, "cases", []):                       # verify: EvaluationReport field names
        out.setdefault(getattr(row, "evaluator", "?"), []).append(float(getattr(row, "score", 0) or 0))
    return {k: sum(v) / len(v) for k, v in out.items()}


def main() -> None:
    cases = load_cases()
    base, tuned = score(MODEL_ID, cases), score(TUNED, cases)
    print(f"\n{'evaluator':<32}{'base':>8}{'tuned':>8}")
    for k in sorted(set(base) | set(tuned)):
        print(f"{k:<32}{base.get(k, 0):>8.2f}{tuned.get(k, 0):>8.2f}")
    tone_up = tuned.get("tone", 0) > base.get("tone", 0)
    no_regress = all(tuned.get(k, 0) >= base.get(k, 0) - 0.05 for k in base if k != "tone")
    print("\nVERDICT:", "PROMOTE (tone up, no task regression)" if tone_up and no_regress
          else "HOLD (keep base; the tone gain does not pay for the regression)" if tone_up else "HOLD (no tone gain)")


if __name__ == "__main__":
    main()
