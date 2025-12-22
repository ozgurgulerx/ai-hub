"""
Fast validator for Azure DPO JSONL format.

Checks:
- required keys: input, preferred_output, non_preferred_output
- input.messages exists and last role is user
- outputs contain >= 1 message
- output roles are only assistant/tool
"""

from __future__ import annotations

import json
import sys


ALLOWED_OUTPUT_ROLES = {"assistant", "tool"}


def die(msg: str) -> None:
    raise ValueError(msg)


def validate_row(obj: dict, line_no: int) -> None:
    for k in ("input", "preferred_output", "non_preferred_output"):
        if k not in obj:
            die(f"line {line_no}: missing key '{k}'")

    inp = obj["input"]
    if "messages" not in inp or not isinstance(inp["messages"], list) or len(inp["messages"]) < 1:
        die(f"line {line_no}: input.messages missing/invalid")

    if inp["messages"][-1].get("role") != "user":
        die(f"line {line_no}: last message must be role=user")

    for out_key in ("preferred_output", "non_preferred_output"):
        out = obj[out_key]
        if not isinstance(out, list) or len(out) < 1:
            die(f"line {line_no}: {out_key} must be a non-empty list")

        for m in out:
            role = m.get("role")
            if role not in ALLOWED_OUTPUT_ROLES:
                die(f"line {line_no}: {out_key} contains illegal role '{role}'")
            if role == "assistant" and ("content" not in m or not isinstance(m["content"], str)):
                die(f"line {line_no}: assistant message must contain string content")


def main(path: str) -> None:
    ok = 0
    with open(path, "r", encoding="utf-8-sig") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            validate_row(obj, i)
            ok += 1
    print(f"OK: validated {ok} rows")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_dpo_jsonl.py <file.jsonl>")
        sys.exit(2)
    main(sys.argv[1])
