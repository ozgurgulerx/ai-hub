from __future__ import annotations

import json
import os
import random
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


REPO_ROOT = Path(__file__).resolve().parents[3]
DAY02_DIR = REPO_ROOT / "days" / "Day02"
DAY01_TRAIN = REPO_ROOT / "days" / "Day01" / "data" / "rft_train.jsonl"
DAY01_VALID = REPO_ROOT / "days" / "Day01" / "data" / "rft_valid.jsonl"


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def make_pair(item: Dict[str, Any], rng: random.Random) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    preferred = {
        "category": item["label_category"],
        "priority": item["label_priority"],
        "route_to": item["label_route_to"],
        "needs_human": item["label_needs_human"],
    }

    # Wrong-but-valid negative: flip category to a different allowed value.
    allowed_categories = list(item.get("allowed_categories", []))
    if not allowed_categories:
        raise ValueError("item missing allowed_categories")
    bad_category = next(c for c in allowed_categories if c != item["label_category"])
    non_preferred = {**preferred, "category": bad_category}
    return preferred, non_preferred


def item_to_dpo_row(item: Dict[str, Any], rng: random.Random) -> Dict[str, Any]:
    preferred, non_preferred = make_pair(item, rng)
    return {
        "input": {"messages": item["messages"], "tools": [], "parallel_tool_calls": True},
        "preferred_output": [
            {"role": "assistant", "content": json.dumps(preferred, separators=(",", ":"))}
        ],
        "non_preferred_output": [
            {"role": "assistant", "content": json.dumps(non_preferred, separators=(",", ":"))}
        ],
    }


def main() -> None:
    rng = random.Random(13)
    train_items = read_jsonl(DAY01_TRAIN)
    valid_items = read_jsonl(DAY01_VALID)

    train_rows = [item_to_dpo_row(item, rng) for item in train_items]
    valid_rows = [item_to_dpo_row(item, rng) for item in valid_items]

    write_jsonl(DAY02_DIR / "data" / "dpo_train.jsonl", train_rows)
    write_jsonl(DAY02_DIR / "data" / "dpo_valid.jsonl", valid_rows)

    print("Wrote:", DAY02_DIR / "data" / "dpo_train.jsonl")
    print("Wrote:", DAY02_DIR / "data" / "dpo_valid.jsonl")


if __name__ == "__main__":
    os.chdir(REPO_ROOT)
    main()
