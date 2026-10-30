"""Call one tool through the gateway and print the outcome plus the matching gateway log line (map F7).
Usage: python gateway_probe.py --tool lookup_ticket. Status: scaffold only, functionality unverified."""
import argparse


def main(tool: str) -> None:
    # TODO(learner): Runner over agent.root_agent; prompt that forces `tool`; print allowed/denied and the source;
    # then gcloud logging read for the gateway's L7 log filtered by mcp.toolName == tool.
    raise SystemExit("TODO(learner): implement gateway_probe")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    main(ap.parse_args().tool)
