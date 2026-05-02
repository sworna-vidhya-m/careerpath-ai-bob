#!/usr/bin/env bash
# One-command startup: activate venv, ensure deps, launch app.
set -euo pipefail

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
exec uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
