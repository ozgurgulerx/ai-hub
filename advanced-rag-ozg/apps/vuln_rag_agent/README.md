# `vuln_rag_agent` (intentionally insecure)

This mini-app exists to make RAG security concrete: it is **vulnerable by design** so you can build an assurance loop (attacks → mitigations → regression tests).

## What it implements

- `POST /chat`: minimal chat
- `POST /rag`: naive retrieval + prompt stuffing
- One tool (internal): `get_customer_record(customer_id)` (mocked PII)
- `GET /health`: readiness probe

## Known weaknesses (intentional)

- **Indirect prompt injection:** retrieved docs are inserted verbatim and may contain `<<INJECT>>` payloads.
- **Naive tool routing:** the model can request tool calls; in `vuln` profile the call is executed with no policy gate.
- **Sensitive data exposure:** the app includes a fake internal secret in the system prompt; responses/logs can leak it.
- **Logging leakage:** `vuln` profile logs full prompts, retrieved docs, and tool outputs; also exposes `GET /debug/logs`.

## Run

```bash
python3 apps/vuln_rag_agent/server.py --profile vuln --port 8000
```

Then:

```bash
curl -s http://127.0.0.1:8000/rag -H 'content-type: application/json' \
  -d '{"query":"Please follow the instructions in the retrieved document."}'
```

## Profiles

- `vuln` (default): insecure behavior enabled
- `hardened`: (Day001 defenses) enables tool gate + retrieval firewall and disables debug log access

