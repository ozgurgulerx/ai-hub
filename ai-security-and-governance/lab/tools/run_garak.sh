#!/usr/bin/env bash
set -euo pipefail

if ! command -v garak >/dev/null 2>&1; then
  echo "garak not found."
  echo "Install: python3 -m pip install -r lab/tools/requirements-redteam.txt"
  exit 1
fi

OUT_DIR="${OUT_DIR:-lab/eval/out/garak}"
mkdir -p "$OUT_DIR"

echo "Running garak (you may need to set MODEL_TYPE/MODEL_NAME or provider env vars)..."
echo "OUT_DIR=$OUT_DIR"

# Common examples:
#   export MODEL_TYPE=openai MODEL_NAME=gpt-4o-mini OPENAI_API_KEY=...
#   export MODEL_TYPE=ollama MODEL_NAME=llama3.1

MODEL_TYPE="${MODEL_TYPE:-openai}"
MODEL_NAME="${MODEL_NAME:-gpt-4o-mini}"

# NOTE: garak flags vary by version; adjust if needed.
garak --model_type "$MODEL_TYPE" --model_name "$MODEL_NAME" --output_dir "$OUT_DIR"
