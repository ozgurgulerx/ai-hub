from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Dict, List, Optional


NUMERIC_FIELDS = {
    "train_reward_mean",
    "valid_reward_mean",
    "train_reasoning_tokens_mean",
    "valid_reasoning_tokens_mean",
}


def _to_float(value: str) -> Optional[float]:
    try:
        x = float(value)
    except Exception:
        return None
    return None if math.isnan(x) else x


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def summarize(rows: List[Dict[str, str]]) -> None:
    if not rows:
        print("No rows.")
        return

    fields = rows[0].keys()
    available = [f for f in NUMERIC_FIELDS if f in fields]
    if not available:
        print("No expected numeric fields found. Available columns:")
        for name in sorted(fields):
            print("-", name)
        return

    print(f"rows={len(rows)}")
    for field in available:
        values = [_to_float(r.get(field, "")) for r in rows]
        values = [v for v in values if v is not None]
        if not values:
            print(f"{field}: no numeric values")
            continue
        print(
            f"{field}: last={values[-1]:.4g} max={max(values):.4g} min={min(values):.4g}"
        )


def main(argv: List[str]) -> None:
    if len(argv) < 2:
        print("Usage: python analyze_results_csv.py /path/to/results.csv")
        raise SystemExit(2)

    path = Path(argv[1]).expanduser().resolve()
    rows = read_csv(path)
    summarize(rows)


if __name__ == "__main__":
    main(sys.argv)

