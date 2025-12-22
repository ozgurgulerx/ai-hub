# Eval Dashboard (Day001)

Generate metrics:

```bash
python3 lab/eval/harness/run_baseline.py --transport local --mode vuln --out lab/eval/baseline_metrics.vuln.json
python3 lab/eval/harness/run_baseline.py --transport local --mode defended --out lab/eval/baseline_metrics.defended.json
```

Quick view:

```bash
cat lab/eval/baseline_metrics.vuln.json | python3 -m json.tool | less
cat lab/eval/baseline_metrics.defended.json | python3 -m json.tool | less
```

Compare (basic):

```bash
python3 - <<'PY'
import json
from pathlib import Path

v = json.loads(Path("lab/eval/baseline_metrics.vuln.json").read_text())
d = json.loads(Path("lab/eval/baseline_metrics.defended.json").read_text())

def pick(m, key, default=None):
    cur = m
    for part in key.split("."):
        cur = cur.get(part, {})
    return cur or default

for fam in sorted(set(v["by_family"]) | set(d["by_family"])):
    v_asr = v["by_family"].get(fam, {}).get("asr", None)
    d_asr = d["by_family"].get(fam, {}).get("asr", None)
    print(f"{fam:32}  vuln={v_asr}  defended={d_asr}")
PY
```
