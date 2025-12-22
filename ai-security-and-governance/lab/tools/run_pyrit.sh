#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
import importlib.util
spec = importlib.util.find_spec("pyrit")
if spec is None:
    raise SystemExit(
        "pyrit not found.\n"
        "Install: python3 -m pip install -r lab/tools/requirements-redteam.txt\n"
        "Then expand this runner to target your chosen model/app.\n"
    )
print("PyRIT is installed. Day001 runner is intentionally minimal; expand Day002+.")
print("Next: see docs/day001/red-teaming-tools.md for how to point PyRIT at a model endpoint or lab/apps/vuln_rag_agent.")
PY
