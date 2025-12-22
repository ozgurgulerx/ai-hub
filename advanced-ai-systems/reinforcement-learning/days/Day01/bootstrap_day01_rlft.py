from __future__ import annotations

import json
import os
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


REPO_ROOT = Path(__file__).resolve().parents[2]
DAY_DIR = REPO_ROOT / "days" / "Day01"


@dataclass(frozen=True)
class Ticket:
    text: str
    category: str
    priority: str
    route_to: str
    needs_human: bool


CATEGORIES = ["billing", "login", "bug", "feature_request", "security", "account_closure"]
PRIORITIES = ["p0", "p1", "p2", "p3"]
ROUTES = ["support_l1", "support_l2", "billing_team", "security_team", "retention_team"]


def _route_rules(category: str, priority: str) -> str:
    if category == "security":
        return "security_team"
    if category == "billing":
        return "billing_team"
    if category == "account_closure":
        return "retention_team"
    if priority in {"p0", "p1"}:
        return "support_l2"
    return "support_l1"


def _needs_human_rules(category: str, priority: str, text: str) -> bool:
    if category in {"security", "account_closure"}:
        return True
    if priority == "p0":
        return True
    if "lawsuit" in text.lower() or "attorney" in text.lower():
        return True
    return False


def make_ticket(rng: random.Random) -> Ticket:
    templates = [
        ("I can't log into my account. It says my password is wrong.", "login", "p2"),
        ("My card was charged twice for the same invoice. Please refund.", "billing", "p1"),
        ("The app crashes when I click Export. Steps: open report -> export -> crash.", "bug", "p1"),
        ("Can you add SSO support for our org?", "feature_request", "p3"),
        ("I think my account was hacked. I see logins from new countries.", "security", "p0"),
        ("Please close my account and delete my data.", "account_closure", "p2"),
        ("We were billed for 12 seats but only have 9 users. Fix this.", "billing", "p2"),
        ("Password reset email never arrives; I've tried 3 times.", "login", "p2"),
        ("Your API returns 500 on /v1/export. This blocks our nightly job.", "bug", "p0"),
        ("Feature request: export to parquet for our data pipeline.", "feature_request", "p3"),
        ("Suspicious MFA prompts started today; I didn't request them.", "security", "p0"),
        ("Close my account immediately or my attorney will contact you.", "account_closure", "p1"),
    ]
    text, category, priority = rng.choice(templates)
    route_to = _route_rules(category, priority)
    needs_human = _needs_human_rules(category, priority, text)
    return Ticket(text=text, category=category, priority=priority, route_to=route_to, needs_human=needs_human)


def ticket_to_item(ticket: Ticket) -> Dict[str, Any]:
    return {
        "messages": [
            {
                "role": "developer",
                "content": (
                    "You are a support-triage router. Output STRICT JSON only. "
                    "Do not include prose. Follow the JSON schema."
                ),
            },
            {"role": "user", "content": ticket.text},
        ],
        "label_category": ticket.category,
        "label_priority": ticket.priority,
        "label_route_to": ticket.route_to,
        "label_needs_human": ticket.needs_human,
        "allowed_categories": CATEGORIES,
        "allowed_priorities": PRIORITIES,
        "allowed_routes": ROUTES,
    }


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _safe_read_first_row(jsonl_path: Path) -> Optional[Dict[str, Any]]:
    if not jsonl_path.exists():
        return None
    with jsonl_path.open("r", encoding="utf-8-sig") as f:
        line = f.readline().strip()
    return json.loads(line) if line else None


def main() -> None:
    rng = random.Random(7)
    n_train, n_valid = 240, 60

    tickets = [make_ticket(rng) for _ in range(n_train + n_valid)]
    train_rows = [ticket_to_item(t) for t in tickets[:n_train]]
    valid_rows = [ticket_to_item(t) for t in tickets[n_train:]]

    write_jsonl(DAY_DIR / "data" / "rft_train.jsonl", train_rows)
    write_jsonl(DAY_DIR / "data" / "rft_valid.jsonl", valid_rows)

    # Response format schema (strict).
    response_format = {
        "name": "support_ticket_route",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "category": {"type": "string"},
                "priority": {"type": "string"},
                "route_to": {"type": "string"},
                "needs_human": {"type": "boolean"},
            },
            "required": ["category", "priority", "route_to", "needs_human"],
            "additionalProperties": False,
        },
    }
    (DAY_DIR / "schema").mkdir(parents=True, exist_ok=True)
    (DAY_DIR / "schema" / "response_format.json").write_text(
        json.dumps(response_format, indent=2), encoding="utf-8"
    )

    # Local smoke test.
    (DAY_DIR / "eval").mkdir(parents=True, exist_ok=True)
    first_valid_item = _safe_read_first_row(DAY_DIR / "data" / "rft_valid.jsonl") or valid_rows[0]
    good_output = {
        "category": first_valid_item["label_category"],
        "priority": first_valid_item["label_priority"],
        "route_to": first_valid_item["label_route_to"],
        "needs_human": first_valid_item["label_needs_human"],
    }
    bad_category = next(
        c for c in first_valid_item["allowed_categories"] if c != first_valid_item["label_category"]
    )
    bad_output = {**good_output, "category": bad_category}
    (DAY_DIR / "eval" / "smoke_test_payload.json").write_text(
        json.dumps(
            {
                "item": first_valid_item,
                "samples": [
                    {"output_text": json.dumps(good_output, separators=(",", ":"))},
                    {"output_text": json.dumps(bad_output, separators=(",", ":"))},
                    {"output_text": "not json"},
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print("Generated Day01 artifacts in:", DAY_DIR)


if __name__ == "__main__":
    os.chdir(REPO_ROOT)
    main()
