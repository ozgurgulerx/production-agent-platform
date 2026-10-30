#!/usr/bin/env bash
# Creates labs-setup/.venv on Python 3.13 with the pinned requirements. Idempotent.
set -euo pipefail
here="$(cd "$(dirname "$0")/../.." && pwd)"           # labs-setup/
py="${PYTHON:-python3.13}"
[ -d "$here/.venv" ] || "$py" -m venv "$here/.venv"
"$here/.venv/bin/pip" install -q --upgrade pip
"$here/.venv/bin/pip" install -q -r "$here/requirements.txt"
echo "venv ready: $here/.venv  ($("$here/.venv/bin/python" --version))"
