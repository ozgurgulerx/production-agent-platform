"""Skeleton of the S04.09 harness loop for the support-ticket agent.

Shows the eight harness responsibilities as named steps around one model
call: compile context, compile capabilities, infer, gate the proposal with
policy and approval binding, record an effect intent, execute, record the
observation, check budgets and stop conditions, emit a trace span.

Untested sketch. No model, no tools, no storage; every collaborator is a
stub so the control flow can be read in one screen.
"""

from dataclasses import dataclass, field
from hashlib import sha256
import json


@dataclass
class TaskState:
    task_id: str
    principal: dict
    budget: dict
    events: list = field(default_factory=list)   # append-only session log
    effects: dict = field(default_factory=dict)  # action_id -> ledger entry
    turns: int = 0


def compile_context(state: TaskState) -> list:
    """Render the slice the next decision needs; never the whole log."""
    return [{"role": "system", "content": "stable prefix"}] + state.events[-12:]


def compile_capabilities(state: TaskState) -> list:
    """Expose only what this principal may call; keep the hot set small."""
    hot = ["get_ticket", "list_tickets", "get_policy"]
    if "tickets.refund" in state.principal["scopes"]:
        hot.append("issue_refund")
    return hot


def action_hash(tool: str, args: dict) -> str:
    return sha256(json.dumps([tool, args], sort_keys=True).encode()).hexdigest()


def policy_gate(state: TaskState, tool: str, args: dict) -> str:
    """Deterministic. Returns ALLOW, DENY or REQUIRE_APPROVAL."""
    if tool != "issue_refund":
        return "ALLOW"
    if args["amount"] > 200:
        return "DENY"
    return "REQUIRE_APPROVAL"


def approval_valid(state: TaskState, tool: str, args: dict) -> bool:
    """An approval binds to the exact action hash, principal and expiry."""
    rec = state.effects.get(action_hash(tool, args))
    return bool(rec and rec.get("approved_by") and not rec.get("expired"))


def budget_exhausted(state: TaskState) -> bool:
    return state.turns >= state.budget["max_turns"]


def task_resolved(state: TaskState) -> bool:
    """A predicate over backend state, never the model's claim."""
    return any(e.get("effect") == "ticket.closed" for e in state.events)


def run(state: TaskState, model, execute, trace):
    while not task_resolved(state) and not budget_exhausted(state):
        state.turns += 1
        proposal = model(compile_context(state), compile_capabilities(state))
        if proposal["type"] == "final":
            state.events.append({"model_claims_done": True})
            continue  # the predicate above decides, not the model
        tool, args = proposal["tool"], proposal["args"]
        decision = policy_gate(state, tool, args)
        if decision == "DENY":
            state.events.append({"denied": tool})
            continue
        if decision == "REQUIRE_APPROVAL" and not approval_valid(state, tool, args):
            state.events.append({"awaiting_approval": action_hash(tool, args)})
            return "PAUSED"
        key = action_hash(tool, args)
        state.effects.setdefault(key, {})["status"] = "INTENT_RECORDED"
        result = execute(tool, args, idempotency_key=key)  # timeout -> UNKNOWN
        state.effects[key]["status"] = result.get("status", "UNKNOWN")
        state.events.append({"tool": tool, "result": result})
        trace(state.task_id, state.turns, tool, decision, state.effects[key])
    return "RESOLVED" if task_resolved(state) else "BUDGET_EXHAUSTED"
