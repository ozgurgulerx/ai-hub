"""
Deterministic regression checks for DPO runs.

This is a placeholder harness you extend for your preference axis:
- strict JSON schema checks
- length caps
- forbidden tokens/phrases
- emoji bans

Goal: catch "format regressions" even when the overall preference win-rate improved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def check_no_emojis(text: str) -> bool:
    return all(e not in text for e in ["😊", "😢", "😂"])


def main(argv: List[str]) -> None:
    if len(argv) != 2:
        print("Usage: python format_checks.py path/to/dpo_regression.jsonl")
        raise SystemExit(2)

    path = Path(argv[1]).expanduser().resolve()
    rows = load_jsonl(path)

    failures = 0
    for i, ex in enumerate(rows):
        pref = ex["preferred_output"][0]["content"]
        nonp = ex["non_preferred_output"][0]["content"]
        if not check_no_emojis(pref):
            failures += 1
            print(f"[fail] idx={i} preferred contains emoji")
        if not check_no_emojis(nonp):
            # non-preferred may violate checks by design; still useful to surface.
            print(f"[note] idx={i} non_preferred contains emoji")

    print(f"checked={len(rows)} failures={failures}")


if __name__ == "__main__":
    main(sys.argv)
