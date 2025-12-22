"""
Pairwise win-rate evaluator for DPO regression sets.

Definition:
A model "wins" a pair if it assigns higher log-probability to preferred_output than non_preferred_output
given the same input.

For Azure-hosted models, you typically can't get token logprobs in chat APIs.
So you have two workable proxies:
1) Use an open model locally to compute logprobs (true pairwise metric).
2) Use a *judge* (deterministic rubric or model-judge) to compare outputs (proxy).
This script implements the judge-proxy path by default.

Upgrade path:
- If you have access to logprobs for your stack, swap in true logprob scoring.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass
class PairResult:
    idx: int
    preferred_score: float
    non_preferred_score: float
    preferred_wins: bool
    reason: str


def rubric_judge(
    input_messages: List[Dict[str, str]], preferred: str, non_preferred: str
) -> Tuple[float, float, str]:
    """
    Replace this with YOUR rubric.
    Keep it deterministic and cheap.
    Example rubric below: no emojis + concise.
    """

    def score(text: str) -> float:
        s = 0.0
        if "😊" not in text and "😢" not in text and "😂" not in text:
            s += 1.0
        if len(text) <= 220:
            s += 1.0
        # add more checks tied to your Day02 rubric
        return s

    _ = input_messages
    ps = score(preferred)
    ns = score(non_preferred)
    reason = "rubric:no-emoji + len<=220"
    return ps, ns, reason


def load_jsonl(path: str) -> List[Dict[str, Any]]:
    rows = []
    with open(path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def eval_pairs(path: str) -> List[PairResult]:
    rows = load_jsonl(path)
    results: List[PairResult] = []
    for i, ex in enumerate(rows):
        inp = ex["input"]["messages"]
        pref = ex["preferred_output"][0]["content"]
        nonp = ex["non_preferred_output"][0]["content"]
        ps, ns, reason = rubric_judge(inp, pref, nonp)
        results.append(PairResult(i, ps, ns, ps > ns, reason))
    return results


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="Path to DPO regression JSONL")
    args = ap.parse_args()

    results = eval_pairs(args.file)
    win = sum(1 for r in results if r.preferred_wins)
    total = len(results)
    print(f"win_rate={win/total:.3f} ({win}/{total})")

    # Show failures
    fails = [r for r in results if not r.preferred_wins]
    if fails:
        print("\nTop failures:")
        for r in fails[:10]:
            print(
                f"- idx={r.idx} pref={r.preferred_score} nonpref={r.non_preferred_score} reason={r.reason}"
            )


if __name__ == "__main__":
    main()
