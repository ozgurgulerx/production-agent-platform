"""Quarantine the ticket agent and release it (F5).

Proves: an admin can darken every channel in one call without deleting anything; the maker test pane keeps
working; the inventory flips isQuarantined. Needs CopilotStudio.AdminActions.Invoke and an admin role.
Revert: python quarantine.py --off
"""
import argparse

from _common import AGENT_ID, ENVIRONMENT_ID, need, pp_api, show

API_VERSION = "2022-03-01-preview"   # verify against F5


def set_quarantine(on: bool) -> None:
    op = "SetAsQuarantined" if on else "SetAsUnquarantined"   # verify release operation name (F5)
    with pp_api() as c:
        r = c.post(f"/copilotstudio/environments/{ENVIRONMENT_ID}/bots/{AGENT_ID}/botQuarantine/{op}",
                   params={"api-version": API_VERSION})
        show(f"{op}", r)
        r2 = c.get(f"/copilotstudio/environments/{ENVIRONMENT_ID}/bots/{AGENT_ID}", params={"api-version": API_VERSION})  # verify
        body = show("agent after", r2)
    state = body.get("isQuarantined", body.get("properties", {}).get("isQuarantined"))
    print(f"\nisQuarantined = {state}  (inventory refresh is about 20 minutes, E7)")
    print("expected now:" + (" Teams / web / Direct Line return an error; maker test pane still answers."
                             if on else " all channels answer again."))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--on", action="store_true")
    g.add_argument("--off", action="store_true")
    args = ap.parse_args()
    need("ENVIRONMENT_ID", "AGENT_ID")
    set_quarantine(args.on)
