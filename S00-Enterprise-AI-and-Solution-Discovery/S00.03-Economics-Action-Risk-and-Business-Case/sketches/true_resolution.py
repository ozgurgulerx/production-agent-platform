"""True-resolution rate with an explicit denominator and a recontact reversal (S00.04, section 2).

A contained contact counts as resolved only if the same customer does not recontact on the
same intent within the window; exclusions are reported beside the rate. Illustrative and untested.
"""

# illustrative: the measurement, so the denominator and the reversal rule are explicit
from collections import defaultdict
from datetime import timedelta

WINDOW = timedelta(days=7)

def true_resolution(contacts, eligible_intents):
    """contacts: [{customer, intent, ts, disposition}], sorted by ts."""
    eligible = [c for c in contacts if c["intent"] in eligible_intents]
    excluded = len(contacts) - len(eligible)
    threads = defaultdict(list)
    for c in eligible:                               # same customer + same intent
        threads[(c["customer"], c["intent"])].append(c)
    resolved = 0
    for thread in threads.values():
        for i, c in enumerate(thread):
            if c["disposition"] != "contained":
                continue                             # escalated/abandoned never count
            nxt = thread[i + 1] if i + 1 < len(thread) else None
            if nxt and nxt["ts"] - c["ts"] <= WINDOW:
                continue                             # a recontact REVERSES the verdict
            resolved += 1
    return {"true_resolution_rate": resolved / max(len(eligible), 1),
            "eligible": len(eligible),               # denominator EXPLICIT
            "excluded": excluded}                    # exclusions REPORTED
