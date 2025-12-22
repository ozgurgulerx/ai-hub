import json
from typing import Any, Dict, Optional


def _fail(score: float, reason: str) -> float:
    # Keep the interface scalar, but make debugging possible by printing.
    print(f"[grade] {reason}")
    return score


def _get_output_json(sample: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    # Prefer structured output if available, otherwise fall back to parsing text.
    output_json = sample.get("output_json")
    if isinstance(output_json, dict):
        return output_json

    output_text = sample.get("output_text", "")
    if not isinstance(output_text, str) or not output_text.strip():
        return None
    try:
        return json.loads(output_text)
    except Exception:
        return None


def grade(sample: Dict[str, Any], item: Dict[str, Any]) -> float:
    output = _get_output_json(sample)
    if output is None:
        return _fail(0.0, "invalid_json")

    # Anti-cheat #1: strict keys only (assumes schema, but enforce anyway).
    required_keys = {"category", "priority", "route_to", "needs_human"}
    if set(output.keys()) != required_keys:
        return _fail(0.0, f"bad_keys: {sorted(output.keys())}")

    # Anti-cheat #2: enforce allowed vocab (prevents arbitrary strings).
    allowed_categories = set(item.get("allowed_categories", []))
    allowed_priorities = set(item.get("allowed_priorities", []))
    allowed_routes = set(item.get("allowed_routes", []))

    category = output.get("category")
    priority = output.get("priority")
    route_to = output.get("route_to")
    needs_human = output.get("needs_human")

    if category not in allowed_categories:
        return _fail(0.0, f"bad_category: {category}")
    if priority not in allowed_priorities:
        return _fail(0.0, f"bad_priority: {priority}")
    if route_to not in allowed_routes:
        return _fail(0.0, f"bad_route_to: {route_to}")
    if not isinstance(needs_human, bool):
        return _fail(0.0, "needs_human_not_bool")

    # Anti-cheat #3: fail closed if labels are missing (don’t reward empty targets).
    required_labels = ("label_category", "label_priority", "label_route_to", "label_needs_human")
    if any(k not in item for k in required_labels):
        return _fail(0.0, "missing_labels_in_item")

    # Deterministic reward: exact-match against labels.
    score = 0.0
    score += 0.40 if category == item.get("label_category") else 0.0
    score += 0.30 if priority == item.get("label_priority") else 0.0
    score += 0.20 if route_to == item.get("label_route_to") else 0.0
    score += 0.10 if needs_human == item.get("label_needs_human") else 0.0
    return float(score)
