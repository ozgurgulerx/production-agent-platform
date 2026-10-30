"""Print the outbound auth matrix with a status per row: which rows have the inputs they need in .env, run those,
and report which principal the downstream saw. Rows without inputs are listed as SKIPPED with what is missing.

Proves: you can name all seven rows and say which ones carry the user.
Run: python run_matrix.py
"""

import os
import subprocess
import sys

from _common import ENV_PATH  # noqa: F401  (loads .env)

ROWS = [
    ("GATEWAY_IAM_ROLE",          "the Gateway role",          [],                                                  None),
    ("API_KEY",                   "stored key, no user",       ["TICKETS_API_KEY"],                                 "01_api_key_provider.py"),
    ("OAUTH client_credentials",  "agent's client, no user",   ["COGNITO_DISCOVERY_URL", "COGNITO_CLIENT_SECRET"],  "02_oauth_client_credentials.py"),
    ("OAUTH authorization_code",  "the user (consent once)",   ["OAUTH_3LO_PROVIDER", "TICKETS_API_BASE"],          "03_oauth_authorization_code.py"),
    ("OAUTH token_exchange (OBO)","the user (no consent)",     ["ENTRA_TENANT_ID", "ENTRA_CLIENT_ID", "ENTRA_CLIENT_SECRET"], "04_obo_token_exchange.py"),
    ("CALLER_IAM_CREDENTIALS",    "the caller's IAM role",     ["TICKET_AGENT_RUNTIME_ARN"],                        "../06-a2a-and-runtime-targets/runtime_as_gateway_target.py"),
    ("JWT_PASSTHROUGH",           "the caller's JWT",          ["TICKET_AGENT_JWT_ARN"],                            None),
]


def main() -> None:
    print(f"{'row':28} {'downstream sees':26} status")
    for row, sees, needs, script in ROWS:
        missing = [k for k in needs if not os.environ.get(k)]
        if missing:
            print(f"{row:28} {sees:26} SKIPPED (set {', '.join(missing)})"); continue
        if not script:
            print(f"{row:28} {sees:26} covered by lab 03 / 06"); continue
        print(f"{row:28} {sees:26} RUN {script}")
        subprocess.run([sys.executable, script], check=False)


if __name__ == "__main__":
    main()
