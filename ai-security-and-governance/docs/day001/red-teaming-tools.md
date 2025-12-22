# Day001 — Red-Teaming Tools (Garak + PyRIT)

Day001’s `eval/harness/` is an internal, deterministic harness for measuring *this repo’s* attack packs and defenses.
`garak` and `PyRIT` are optional external tools that help you do broader, adversarial exploration (“red teaming”) against either a raw model endpoint or an app.

## PyRIT (Python Risk Identification Tool)

PyRIT is an open-source Python framework for red teaming GenAI systems. It’s useful when you want a repeatable workflow for:

- Building/collecting adversarial prompts (prompt injection, jailbreaks, sensitive-info extraction, policy-violations, etc.).
- Targeting either:
  - a **model endpoint** (API/local), or
  - an **application** that wraps a model (agent, RAG app, tool-using assistant).
- Scoring and triaging responses so failures become:
  - mitigations (prompting, filters, policy gates, retrieval firewall, etc.), and
  - regression tests (so fixes stay fixed).

### Typical workflow

1. Pick a target:
   - Model-level testing (quick): point PyRIT at your model provider/backend.
   - App-level testing (realistic): point PyRIT at your app’s HTTP endpoint(s).
2. Choose prompt sources:
   - Built-in prompt sets/strategies, plus your own prompts based on your threat matrix.
3. Run campaigns:
   - Send prompts, capture responses, store artifacts.
4. Score + triage:
   - Identify successful attacks (e.g., secret leakage, policy bypass, tool misuse).
5. Turn wins into engineering work:
   - Add/adjust defenses, then encode the found prompt(s) into your regression suite.

### Using PyRIT against the Day001 app in this repo

The Day001 app is `apps/vuln_rag_agent/server.py` with a `POST /chat` endpoint. To use PyRIT here, the usual pattern is:

- Run the server locally (`python3 apps/vuln_rag_agent/server.py --port 8000`).
- Create a small “target adapter” that takes a prompt string and calls:
  - `POST http://127.0.0.1:8000/chat`
  - JSON body like:
    - `{"message": "<prompt>", "use_rag": true|false, "authenticated_customer_id": "1001"}`
- Feed that adapter into your PyRIT run/campaign and choose the prompt sets/strategies you want to exercise.

This repo intentionally does **not** ship a full PyRIT integration yet (APIs evolve; Day001 focuses on the internal harness). Use `tools/run_pyrit.sh` as an install/smoke-check, then wire PyRIT to either your model provider or the app endpoint as described above.

## garak

`garak` is a model vulnerability scanner that runs a broad set of probes against a configured model backend and writes results to disk.

In this repo:

- Install: `python3 -m pip install -r tools/requirements-redteam.txt`
- Run: `bash tools/run_garak.sh`
- Outputs: `eval/out/garak/` (configurable via `OUT_DIR`)

