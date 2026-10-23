"""Gate-then-score screen for candidate workflows (S00.01, step 3).

Shows the order of operations: hard gates first (never averaged away), then the
risk band from the three-party reading, then the eligible denominator and value.
Illustrative and untested; shapes are placeholders for a real scoring sheet.
"""

# illustrative: the screen as code, so the order of operations is unambiguous
HARD_GATES = ("lawful_data_access", "system_access", "accountable_owner",
              "measurable", "safe_operation")

def screen(wf):
    blocked = [g for g in HARD_GATES if not wf.get(g)]
    if blocked:
        return {"eligible": False, "blocked_by": blocked}   # never averaged away

    # the three-party reading decides the RISK BAND, not the system operation
    third_party_money = wf["money_moves_from"] != "customer_on_call"
    discloses_others = bool(wf.get("discloses_third_party_data"))
    if third_party_money or wf["writes"] == "irreversible":
        band = "value_moving"      # four-eyes, value ceiling, audit trail
    elif wf["writes"] == "reversible" or discloses_others:
        band = "reversible"        # typed tool, idempotency key, reversal owner
    else:
        band = "read_only"         # entitlement check, grounded answer, refusal

    eligible = wf["annual_contacts"] * wf["eligible_share"]  # population, not a %
    return {"eligible": True, "band": band, "denominator": eligible,
            "value": eligible * wf["cost_per_contact"],
            "signature_owners": wf["signature_owners"]}      # empty => not a candidate
