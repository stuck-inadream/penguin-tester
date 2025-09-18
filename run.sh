#!/usr/bin/env bash
set -euo pipefail
PORT="${1:-7860}"
env PYTHONUNBUFFERED=1 python gradio_demo.py --summary --ckmm-iterations 100000 --server_port "$PORT" --share
