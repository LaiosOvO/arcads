#!/bin/sh
set -e
cd "$(dirname "$0")"
python3 -m venv .venv 2>/dev/null || true
. .venv/bin/activate
pip -q install -r requirements.txt
uvicorn app.main:app --reload --port 8000
