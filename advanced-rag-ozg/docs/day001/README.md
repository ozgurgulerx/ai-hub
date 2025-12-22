## Day001 — Secure RAG “Operating System” (hands-on)

Goal: set up a **measurable security baseline** for a deliberately vulnerable RAG+tool app, then add **two defenses** and re-measure.

Timebox (repeat daily): **Build (60–90m) → Measure (30–45m) → Read (30–45m) → Ship (10–20m)**.

### What you’ll ship today (binary exit criteria)

- [ ] Runnable vulnerable app: RAG + tool + (intentional) logging leakage
- [ ] Attack pack v0 runs reproducibly and outputs metrics + report
- [ ] Threat matrix written (1 page)
- [ ] Two defenses implemented: tool gate + retrieval firewall
- [ ] Re-run attacks and capture delta
- [ ] Lit review notes written (1–2 pages)

---

## Quickstart (no external deps)

1) Run baseline (runs the attack pack, writes metrics + report):

```bash
python3 eval/harness/run_attack_pack.py --compare
```

Outputs:
- `eval/baseline_metrics.json`
- `eval/day001_dashboard.md`
- `reports/day001_baseline.md`

If you want the harness to spawn HTTP servers (instead of running in-process), add `--spawn-server` (requires permission to bind localhost ports).

2) Run just the server (manual exploration):

```bash
python3 apps/vuln_rag_agent/server.py --profile vuln --port 8000
```

Try:

```bash
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/rag -H 'content-type: application/json' \
  -d '{"query":"How do I reset my password?"}'
```

---

## What to learn (Day001 concepts)

- **Instruction–data non-separation:** retrieved text can *become* instructions.
- **Confused deputy:** the model can be tricked into abusing *your* tool/data privileges.
- **Capability vs permission:** “can” must be gated by “may”.
- **Security is an eval problem:** if you can’t measure regressions, you don’t have security.

---

## Where the artifacts live

- Threat matrix: `docs/day001/threat-matrix.md`
- Threat model template: `docs/threat-model-template.md`
- Vulnerable app: `apps/vuln_rag_agent/`
- Defenses: `defenses/`
- Harness + baselines: `eval/harness/`, `eval/baseline_metrics.json`
- Report: `reports/day001_baseline.md`
- Lit review notes: `notes/day001_lit_review.md`
