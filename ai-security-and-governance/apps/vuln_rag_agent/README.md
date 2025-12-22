# `vuln_rag_agent` (intentionally insecure)

Minimal “LLM app” playground for Day001: a chat endpoint, a RAG endpoint, and a mocked high-impact tool.

## Run

```bash
python3 apps/vuln_rag_agent/server.py --port 8000
```

Health:

```bash
curl -s http://127.0.0.1:8000/healthz | python3 -m json.tool
```

Chat (example):

```bash
curl -s http://127.0.0.1:8000/chat \
  -H 'content-type: application/json' \
  -d '{"message":"What is the refund policy?","use_rag":true,"authenticated_customer_id":"1001"}' \
  | python3 -m json.tool
```

## Endpoints

- `GET /healthz` → status
- `POST /chat` → chat with optional RAG + (naive) tool calling
- `POST /rag` → retrieve top documents for a query

## Intentional weaknesses (Day001)

- Indirect prompt injection: retrieved docs are injected verbatim.
- Naive tool routing: model-suggested tool calls execute without authorization.
- Sensitive logging: prompts and model outputs are written to `apps/vuln_rag_agent/logs/`.

## Toggle the two Day001 defenses

Start the server with:

```bash
ENABLE_TOOL_GATE=1 ENABLE_RETRIEVAL_FIREWALL=1 python3 apps/vuln_rag_agent/server.py --port 8000
```

These defenses are implemented in `defenses/` and are meant to be measurable (re-run the Day001 attack pack).

