"""Per-call policy gate sketch for S03.06 (untested).

Every model-proposed tool call passes through decide() before dispatch.
Identity and entitlements come from the host session and the task grant,
never from model-supplied arguments. Outcomes are allow, deny, or
approval_required; a missing policy fails closed.
"""

from dataclasses import dataclass, field


@dataclass
class TaskGrant:
    principal: str                      # from the validated token, not the model
    tenant: str
    capabilities: set[str]              # local ids, e.g. "support.tickets.get_ticket"
    resources: set[str]                 # e.g. {"T-104"}
    recipients: set[str]                # permitted destinations; empty = none
    mutation_allowed: bool = False
    budget_calls: int = 20


@dataclass
class Proposal:
    capability: str
    args: dict
    destination: str | None = None      # recipient, URL, filename, query sink
    consequential: bool = False


@dataclass
class Decision:
    outcome: str                        # "allow" | "deny" | "approval_required"
    reason: str
    bound_to: dict = field(default_factory=dict)   # exact action an approval must match


def decide(grant: TaskGrant, p: Proposal, registry: dict, approvals: dict) -> Decision:
    contract = registry.get(p.capability)
    if contract is None or contract.get("quarantined"):
        return Decision("deny", "capability not approved or quarantined")
    if p.capability not in grant.capabilities:
        return Decision("deny", "outside task grant")
    if contract["mutates"] and not grant.mutation_allowed:
        return Decision("deny", "grant allows no mutation")
    res = p.args.get("ticket_id")
    if res and res not in grant.resources:
        return Decision("deny", f"resource {res} not in grant")
    if p.destination and p.destination not in grant.recipients:
        return Decision("deny", f"destination {p.destination} not permitted")
    if p.consequential:
        key = {"capability": p.capability, **p.args}
        if approvals.get(repr(key)) != "accepted":
            return Decision("approval_required", "bound approval missing", bound_to=key)
    return Decision("allow", "within grant")
