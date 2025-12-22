# Day001 Harness

The harness runs a small, deterministic **attack pack v0** against `apps/vuln_rag_agent/` and writes:

- `eval/baseline_metrics.json`
- `eval/day001_dashboard.md`
- `reports/day001_baseline.md`

Run:

```bash
python3 eval/harness/run_attack_pack.py --compare
```

By default this runs **in-process** (no localhost ports). To spawn HTTP servers:

```bash
python3 eval/harness/run_attack_pack.py --compare --spawn-server
```

If you want to run against an already-running server:

```bash
python3 apps/vuln_rag_agent/server.py --profile vuln --port 8000
python3 eval/harness/run_attack_pack.py --base-url http://127.0.0.1:8000
```
