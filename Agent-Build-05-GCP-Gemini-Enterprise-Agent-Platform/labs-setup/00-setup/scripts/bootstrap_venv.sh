#!/usr/bin/env bash
# Creates labs-setup/.venv with Python 3.13 and installs the pinned deps. Never installs into the system Python.
set -euo pipefail

setup_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"   # labs-setup/
cd "$setup_root"

python_bin="${PYTHON_BIN:-}"
if [ -z "$python_bin" ]; then
  for candidate in python3.13 python3.12 python3.11 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then python_bin="$candidate"; break; fi
  done
fi
[ -n "$python_bin" ] || { echo "No python3 found. Install Python 3.11+ (google-adk 2.13 requires >=3.11)." >&2; exit 1; }

venv_dir="${VENV_DIR:-.venv}"
"$python_bin" -m venv "$venv_dir"
# shellcheck disable=SC1091
source "$venv_dir/bin/activate"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "Ready: $venv_dir ($(python --version))"
echo "Next: source $venv_dir/bin/activate && gcloud auth login && gcloud auth application-default login"
