# Retrieval Firewall

Goal: reduce indirect prompt injection by treating retrieved text as **untrusted input**.

Current behavior:

- Removes `<<INJECT>> ... <<END_INJECT>>` blocks (Day001 carrier)
- Drops instruction-like lines (e.g., “ignore previous instructions”, tool-call hints)
- Truncates injected content to a max length

Implementation: `defenses/retrieval_firewall/firewall.py`.

