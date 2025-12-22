#!/usr/bin/env bash
set -euo pipefail

python_bin="${PYTHON_BIN:-python3}"

if ! "$python_bin" -c "import pyrit" >/dev/null 2>&1; then
  echo "PyRIT is not installed in this Python environment."
  echo "Create a venv and install it, then configure your provider keys."
  exit 1
fi

echo "PyRIT is installed, but requires provider configuration (e.g., Azure/OpenAI)."
echo "Create a Day001 scenario set and run it against your app/model."

