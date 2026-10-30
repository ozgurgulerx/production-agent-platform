"""Create the ticket-agent test set through the evaluation REST API from data/testset.csv.

Proves: the same set you can build in Monitor → Evaluations exists as a POST (reading map I3); every case carries a
method, and refusal cases carry Custom instructions plus a Tool-use check. Writes TESTSET_ID to .env.
Body keys follow sketches/evaluation_api_shapes.py and are marked verify until the first run against a tenant.
"""
import argparse
import csv
from pathlib import Path

from _common import AGENT_ID, ENVIRONMENT_ID, need, pp_api, show, write_env

HERE = Path(__file__).resolve().parent
need("ENVIRONMENT_ID", "AGENT_ID")


def case_from_row(row: dict) -> dict:
    methods = []
    m = row["method"]
    if m == "GeneralQuality":
        methods.append({"type": "GeneralQuality", "passThreshold": 70})
    elif m == "ContentSafety":
        methods.append({"type": "ContentSafety", "severityThreshold": 2})
    elif m == "CompareMeaning":
        methods.append({"type": "CompareMeaning", "passThreshold": 50})
    elif m == "KeywordMatch":
        methods.append({"type": "KeywordMatch", "keywords": row["custom_instructions"].split(";")})
    elif m == "Custom":
        methods.append({"type": "Custom", "instructions": row["custom_instructions"]})
    if row["expected_tools"] or row["unexpected_tools"]:
        tu = {"type": "ToolUse", "expectedTools": [t for t in row["expected_tools"].split(",") if t]}
        if row["unexpected_tools"]:
            tu["unexpectedTools"] = [t for t in row["unexpected_tools"].split(",") if t]   # verify: supported key
        methods.append(tu)
    case = {"name": row["name"], "utterance": row["utterance"], "testMethods": methods}   # verify: key names
    if row["expected_response"]:
        case["expectedResponse"] = row["expected_response"]
    return case


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="ticket-agent-regression")
    ap.add_argument("--dry-run", action="store_true", help="print the body, do not call the API")
    args = ap.parse_args()
    with open(HERE / "data" / "testset.csv", newline="", encoding="utf-8") as f:
        cases = [case_from_row(r) for r in csv.DictReader(f)]
    body = {"name": args.name, "description": "C05 lab 01: 12 ticket cases", "testSetType": "SingleResponse", "testCases": cases}
    print(f"{len(cases)} cases, {sum(len(c['testMethods']) for c in cases)} method checks")
    if args.dry_run:
        show(body, 2000)
        return
    resp = pp_api("POST", f"/copilotstudio/environments/{ENVIRONMENT_ID}/bots/{AGENT_ID}/api/makerevaluation/testsets", body)
    show(resp)
    write_env("TESTSET_ID", resp.get("id") or resp.get("testSetId", ""))   # verify: id key


if __name__ == "__main__":
    main()
