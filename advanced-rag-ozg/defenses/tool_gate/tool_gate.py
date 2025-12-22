from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


_JSON = dict[str, Any]


@dataclass(frozen=True)
class ToolDecision:
    allowed: bool
    reason: str


class ToolGate:
    def __init__(self, policy: _JSON) -> None:
        self._policy = policy

    @classmethod
    def from_path(cls, path: Path) -> "ToolGate":
        return cls(json.loads(path.read_text(encoding="utf-8")))

    def authorize(self, tool_name: str, tool_args: _JSON, user_context: _JSON) -> ToolDecision:
        tools = self._policy.get("tools") or {}
        rule = tools.get(tool_name) if isinstance(tools, dict) else None
        if not isinstance(rule, dict):
            return ToolDecision(allowed=False, reason="tool_not_configured")

        deny_by_default = bool(rule.get("deny_by_default", True))
        allowed_roles = rule.get("allowed_roles") or []
        role = str(user_context.get("role", "")).strip()

        if allowed_roles and role not in {str(x) for x in allowed_roles}:
            return ToolDecision(allowed=False, reason="role_not_allowed")

        allowlist_field = str(rule.get("allowed_customer_ids_context_field", "allowed_customer_ids"))
        allowlist = user_context.get(allowlist_field) or []
        if not isinstance(allowlist, list):
            allowlist = []

        customer_id_arg = str(rule.get("customer_id_arg", "customer_id"))
        customer_id = str(tool_args.get(customer_id_arg, "")).strip()

        if not customer_id:
            return ToolDecision(allowed=False, reason="missing_customer_id")

        if customer_id not in {str(x) for x in allowlist}:
            return ToolDecision(allowed=False, reason="customer_id_not_allowed")

        if deny_by_default is False:
            return ToolDecision(allowed=True, reason="allow_by_rule")
        return ToolDecision(allowed=True, reason="allowlist_match")

    def sanitize_result(self, tool_name: str, result: _JSON, user_context: _JSON) -> _JSON:
        tools = self._policy.get("tools") or {}
        rule = tools.get(tool_name) if isinstance(tools, dict) else None
        if not isinstance(rule, dict):
            return result

        redact_fields = rule.get("redact_fields") or []
        if not isinstance(redact_fields, list):
            return result

        if "error" in result:
            return result

        sanitized = dict(result)
        for field in redact_fields:
            if field in sanitized:
                sanitized[field] = "[REDACTED]"
        return sanitized

