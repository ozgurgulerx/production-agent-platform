"""Start a test run for TESTSET_ID, poll until it completes, print per-case results, exit 1 under the threshold.

Proves: a pipeline can gate on Copilot Studio's own evaluation (reading map I3). `--connection` passes an
mcsConnectionId so authenticated tools run as a stored user profile. Writes TESTRUN_ID to .env.
"""
import argparse
import os
import sys
import time

from _common import AGENT_ID, ENVIRONMENT_ID, need, pp_api, write_env

need("ENVIRONMENT_ID", "AGENT_ID", "TESTSET_ID")
BASE = f"/copilotstudio/environments/{ENVIRONMENT_ID}/bots/{AGENT_ID}/api/makerevaluation/testruns"
DONE = {"Completed", "Succeeded", "Failed", "Cancelled"}          # verify: state values


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=0.8, help="minimum pass rate")
    ap.add_argument("--connection", default=None, help="mcsConnectionId of the user profile for authenticated tools")
    ap.add_argument("--run-id", default=None, help="read an existing run instead of starting one")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--ci", action="store_true", help="CI mode: no device-code prompt expected (token must be cached or env-provided); same threshold exit code. Used by C07 ci_pipeline.yml")
    args = ap.parse_args()

    run_id = args.run_id
    if not run_id:
        body = {"testSetId": os.environ["TESTSET_ID"]}
        if args.connection:
            body["mcsConnectionId"] = args.connection
        run = pp_api("POST", BASE, body)
        run_id = run.get("id") or run.get("testRunId")       # verify: id key
        write_env("TESTRUN_ID", run_id)
    t0 = time.time()
    while True:
        run = pp_api("GET", f"{BASE}/{run_id}")
        state = run.get("state") or run.get("status")        # verify
        print(f"  {state}  {int(time.time() - t0)}s")
        if state in DONE:
            break
        if time.time() - t0 > args.timeout:
            sys.exit("timed out waiting for the run")
        time.sleep(15)

    results = run.get("metricsResults", [])
    passed = 0
    print(f"\n{'case':<20} {'method':<16} {'score':>6}  pass  reason")
    for r in results:
        ok = bool(r.get("passed"))
        passed += ok
        print(f"{str(r.get('testCaseName', r.get('testCaseId')))[:20]:<20} {str(r.get('metricName'))[:16]:<16} "
              f"{str(r.get('score'))[:6]:>6}  {'yes' if ok else 'NO ':<4}  {str(r.get('reason', ''))[:70]}")
    rate = passed / len(results) if results else 0.0
    print(f"\npass rate {rate:.2f} over {len(results)} checks (threshold {args.threshold})")
    sys.exit(0 if rate >= args.threshold else 1)


if __name__ == "__main__":
    main()
