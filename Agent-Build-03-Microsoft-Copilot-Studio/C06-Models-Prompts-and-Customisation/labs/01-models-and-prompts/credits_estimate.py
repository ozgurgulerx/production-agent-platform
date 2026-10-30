"""Turn a described support session into Copilot Credits and a monthly projection (Standard-harness rates, K6).

Proves: credits, not tokens, are the budget an admin can cap; a single 10-credit feature (tenant graph grounding)
or a 5-credit action per turn (deep reasoning) changes the bill more than any model choice.
Usage: python credits_estimate.py --answers 3 --tool-calls 1 --flow-actions 2 --deep-reasoning 0 --grounding --conversations 40000
"""
import argparse

RATES = {  # reading map K6, 2026-08-03
    "classic_answer": 1,
    "generative_answer": 2,
    "agent_action": 5,            # trigger run, deep reasoning turn, topic transition, computer-use step
    "tenant_graph_grounding": 10,  # per answer that uses it
    "flow_actions_per_100": 13,
}
PACK_CREDITS, PACK_USD = 25_000, 200   # K7


def session_credits(a) -> dict:
    lines = {}
    lines["generative answers"] = a.answers * RATES["generative_answer"]
    if a.grounding:
        lines["tenant graph grounding"] = a.answers * RATES["tenant_graph_grounding"]
    lines["deep reasoning turns"] = a.deep_reasoning * RATES["agent_action"]
    lines["agent flow actions"] = round(a.flow_actions * RATES["flow_actions_per_100"] / 100, 2)
    lines["tool calls (connector / MCP)"] = 0  # a tool call inside a generative answer is not billed separately on K6; verify for REST tools
    return lines


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--answers", type=int, default=3, help="generative answers per conversation")
    p.add_argument("--tool-calls", type=int, default=1)
    p.add_argument("--flow-actions", type=int, default=0, help="agent-flow actions per conversation")
    p.add_argument("--deep-reasoning", type=int, default=0, help="turns that use deep reasoning")
    p.add_argument("--grounding", action="store_true", help="tenant graph grounding on")
    p.add_argument("--conversations", type=int, default=10_000, help="conversations per month")
    p.add_argument("--m365-copilot-users", action="store_true", help="all users hold an M365 Copilot licence (B2E: no charge)")
    a = p.parse_args()
    lines = session_credits(a)
    per = sum(lines.values())
    print(f"{'line':34} {'credits':>8}")
    for k, v in lines.items():
        print(f"{k:34} {v:>8}")
    print(f"{'per conversation':34} {per:>8}")
    monthly = per * a.conversations
    packs = int(-(-monthly // PACK_CREDITS))
    print(f"\n{a.conversations:,} conversations/month -> {monthly:,.0f} credits -> {packs} packs -> USD {packs * PACK_USD:,} prepaid (or PAYG, rate on the pricing page)")
    if a.m365_copilot_users:
        print("all users licensed for Microsoft 365 Copilot in B2E: these features are no charge (K6); agent flows only via 'When an agent calls the flow'")
    print("\nCap it: PPAC > Licensing > Copilot Studio > per-agent monthly limit (C09). Prepaid agents stop at 125 %.")


if __name__ == "__main__":
    main()
