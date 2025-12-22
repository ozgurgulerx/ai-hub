from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


_JSON = dict[str, Any]


@dataclass(frozen=True)
class FirewallSignal:
    kind: str
    detail: str


class RetrievalFirewall:
    def __init__(self, *, max_chars: int = 2000) -> None:
        self._max_chars = max_chars

    def sanitize(self, doc_id: str, text: str) -> tuple[str, list[FirewallSignal]]:
        signals: list[FirewallSignal] = []
        original = text

        # Remove explicit injection blocks used in this repo.
        text = re.sub(
            r"<<INJECT>>.*?<<END_INJECT>>",
            "",
            text,
            flags=re.DOTALL | re.IGNORECASE,
        )
        if text != original:
            signals.append(FirewallSignal(kind="removed_block", detail="inject_block"))

        # Remove HTML comments (common carrier for hidden instructions in docs).
        before = text
        text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
        if text != before:
            signals.append(FirewallSignal(kind="removed_block", detail="html_comment"))

        suspicious_line_patterns = [
            r"(?i)ignore( all)? (previous|above) instructions",
            r"(?i)system override",
            r"(?i)get_customer_record\s*\(",
            r"(?i)internal_secret",
            r"(?i)print (the )?system prompt",
        ]

        kept_lines: list[str] = []
        for line in text.splitlines():
            if any(re.search(p, line) for p in suspicious_line_patterns):
                signals.append(FirewallSignal(kind="dropped_line", detail=line.strip()[:120]))
                continue
            kept_lines.append(line)

        sanitized = "\n".join(kept_lines).strip()
        if len(sanitized) > self._max_chars:
            sanitized = sanitized[: self._max_chars].rstrip()
            signals.append(FirewallSignal(kind="truncated", detail=str(self._max_chars)))

        if not sanitized.strip():
            # Avoid empty doc injections; keep minimal provenance.
            sanitized = f"[{doc_id}] (content removed by retrieval firewall)"
            signals.append(FirewallSignal(kind="empty_doc", detail=doc_id))

        return sanitized, signals
