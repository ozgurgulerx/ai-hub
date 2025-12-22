from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple


DEFAULT_ALLOWED_SOURCES = {"internal_policy", "internal_wiki"}


_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


_SUSPICIOUS_LINE_RES = [
    re.compile(r"(?i)\\bignore\\b.*\\b(instruction|instructions)\\b"),
    re.compile(r"(?i)^\\s*(system|developer|assistant|user)\\s*:"),
    re.compile(r"(?i)\\b(system prompt|developer message)\\b"),
    re.compile(r"(?i)\\bcall\\s+the\\s+tool\\b"),
    re.compile(r"(?i)\\bget_customer_record\\b"),
    re.compile(r"(?i)^\\s*BEGIN\\b"),
]


@dataclass(frozen=True)
class FirewallDecision:
    blocked: bool
    reasons: List[str]
    content: str


class RetrievalFirewall:
    def __init__(
        self,
        allowed_sources: set[str] | None = None,
        max_doc_chars: int = 2500,
        max_doc_age_days: int = 365 * 5,
    ) -> None:
        self.allowed_sources = allowed_sources or set(DEFAULT_ALLOWED_SOURCES)
        self.max_doc_chars = max_doc_chars
        self.max_doc_age_days = max_doc_age_days

    def filter(self, retrieved_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        filtered: List[Dict[str, Any]] = []
        for doc in retrieved_docs:
            decision = self._decide(doc)
            out = dict(doc)
            out["blocked"] = decision.blocked
            out["reasons"] = decision.reasons
            out["content"] = decision.content
            filtered.append(out)
        return filtered

    def _decide(self, doc: Dict[str, Any]) -> FirewallDecision:
        reasons: List[str] = []
        source = str(doc.get("source", "") or "unknown")
        created = str(doc.get("created", "") or "unknown")
        raw_content = str(doc.get("content", "") or "")

        if source not in self.allowed_sources:
            reasons.append(f"blocked:untrusted_source:{source}")
            return FirewallDecision(blocked=True, reasons=reasons, content="")

        is_too_old, age_reason = self._is_too_old(created)
        if is_too_old:
            reasons.append(age_reason)
            return FirewallDecision(blocked=True, reasons=reasons, content="")

        content = _HTML_COMMENT_RE.sub("", raw_content)
        if content != raw_content:
            reasons.append("sanitized:html_comments_removed")

        kept_lines: List[str] = []
        removed = 0
        for line in content.splitlines():
            if any(r.search(line) for r in _SUSPICIOUS_LINE_RES):
                removed += 1
                continue
            kept_lines.append(line)
        if removed:
            reasons.append(f"sanitized:suspicious_lines_removed:{removed}")

        sanitized = "\n".join(kept_lines).strip()
        if len(sanitized) > self.max_doc_chars:
            sanitized = sanitized[: self.max_doc_chars].rstrip() + "\n[TRUNCATED]"
            reasons.append("sanitized:truncated")

        return FirewallDecision(blocked=False, reasons=reasons, content=sanitized)

    def _is_too_old(self, created: str) -> Tuple[bool, str]:
        try:
            dt = datetime.fromisoformat(created).replace(tzinfo=timezone.utc)
        except ValueError:
            return False, ""
        age_days = (datetime.now(timezone.utc) - dt).days
        if age_days > self.max_doc_age_days:
            return True, f"blocked:doc_too_old:{age_days}d"
        return False, ""

