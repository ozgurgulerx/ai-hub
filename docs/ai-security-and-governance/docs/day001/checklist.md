# Day001 — AI Security Operating System (Checklist + Commands)

Goal: build a runnable vulnerable mini-app, establish a measurable baseline, and implement two concrete defenses you can re-measure.

## Prereqs

- Python 3.10+ (`python3 --version`)

Optional (for garak + PyRIT):

- A model endpoint (local or API) and credentials, if required by your chosen backend.

## 1) Run the vulnerable mini-app

Terminal 1:

```bash
python3 lab/apps/vuln_rag_agent/server.py --port 8000
```

Smoke check:

```bash
curl -s http://127.0.0.1:8000/healthz | python3 -m json.tool
```

## 2) Generate Day001 baseline metrics (internal harness)

Terminal 2:

Option A (no sockets required): run the harness in-process

Vulnerable mode:

```bash
python3 lab/eval/harness/run_baseline.py --transport local --mode vuln --out lab/eval/baseline_metrics.vuln.json
```

With two defenses enabled (tool gate + retrieval firewall):

```bash
python3 lab/eval/harness/run_baseline.py --transport local --mode defended --out lab/eval/baseline_metrics.defended.json
```

Option B (HTTP): run against a live server (useful for external scanners)

```bash
python3 lab/eval/harness/run_baseline.py --transport http --start-server --mode vuln --out lab/eval/baseline_metrics.vuln.json
python3 lab/eval/harness/run_baseline.py --transport http --start-server --mode defended --out lab/eval/baseline_metrics.defended.json
```

## 3) Optional: run garak + PyRIT

These require network/package installs.

What they are:

- `garak`: a fast “scanner” that runs many probes against a model endpoint and saves findings to an output directory.
- `PyRIT` (Python Risk Identification Tool): a red-teaming framework for GenAI systems that helps you (a) generate/curate adversarial prompts, (b) send them to a target (model endpoint or your app), and (c) score/triage responses so you can turn failures into mitigations + regression tests.

More details + suggested workflow: `docs/day001/red-teaming-tools.md`

Install red-team tooling:

```bash
python3 -m pip install -r lab/tools/requirements-redteam.txt
```

Run garak:

```bash
bash lab/tools/run_garak.sh
```

Run PyRIT (skeleton runner; expand Day002+):

```bash
bash lab/tools/run_pyrit.sh
```

## 4) Write Day001 artifacts

- Threat matrix: `docs/day001/threat-matrix.md`
- Lit review notes: `notes/day001_lit_review.md`
- Baseline report: `lab/reports/day001_baseline.md`
