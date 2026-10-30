"""Call one Toolbox tool as a signed-in Google user to prove the `sub` → customer binding (map D7).
Usage: python call_as_user.py my_open_tickets. Status: scaffold only, functionality unverified."""
import os
import sys

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))


def main(tool: str) -> None:
    # TODO(learner): obtain (a) an ID token for TICKET_MCP_URL (Cloud Run door) and (b) a Google user ID token for
    # GOOGLE_OAUTH_CLIENT_ID; send tools/call for `tool` with Authorization: Bearer (a) and header google-user_token: (b);
    # print the rows; then repeat without (b) and print the refusal.
    raise SystemExit("TODO(learner): implement call_as_user")


if __name__ == "__main__":
    main(sys.argv[1])
