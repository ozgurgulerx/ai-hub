from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Tuple


@dataclass(frozen=True)
class ToolPolicy:
    """Hard boundary for tool execution.

    Day001 policy: only allow access to the authenticated customer's record.
    """

    def is_allowed(
        self,
        tool_name: str,
        tool_args: Dict[str, Any],
        user_context: Dict[str, Any],
    ) -> Tuple[bool, str]:
        if tool_name != "get_customer_record":
            return False, "unknown_tool"

        requested_id = str(tool_args.get("customer_id", "") or "")
        if not requested_id:
            return False, "missing_customer_id"

        authorized = self._authorized_customer_ids(user_context)
        if requested_id not in authorized:
            return False, "customer_id_not_authorized"

        return True, ""

    def _authorized_customer_ids(self, user_context: Dict[str, Any]) -> set[str]:
        ids: set[str] = set()
        auth_id = str(user_context.get("authenticated_customer_id", "") or "")
        if auth_id:
            ids.add(auth_id)

        extra: Iterable[Any] = user_context.get("authorized_customer_ids", []) or []
        for v in extra:
            s = str(v or "").strip()
            if s:
                ids.add(s)
        return ids

