#!/usr/bin/env bash
set -euo pipefail

if ! command -v garak >/dev/null 2>&1; then
  echo "garak is not installed. Create a venv and install it, e.g.:"
  echo "  python3 -m venv .venv && source .venv/bin/activate && pip install garak"
  exit 1
fi

echo "Set your target model/provider and run garak."
echo "Example (OpenAI):"
echo "  export OPENAI_API_KEY=...  # and any provider-specific env vars"
echo "  garak --model_type openai --model_name gpt-4o-mini"

