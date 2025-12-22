# Day 010 – Network Path & vLLM HTTP Latency
## Tier 2 – Network Latency Bench & Correlation to TTFT

> **Goal**: Add a tiny HTTP latency bench (with small concurrency) and relate HTTP p50/p95 numbers to your TTFT measurements from Day 007.
>
> **Outcome**: A slightly richer CSV + interpretation that makes it clear how much network+HTTP overhead matters for your SLM on this node.

---

## Tier 2 – Deepen (If Time/Energy Allow)

**Title** – Network Latency Bench & TTFT Correlation  
**Time Budget** – ~75–120 min

---

### 0) Extend the probe into a tiny bench

You can either:

- extend `http_latency_probe.py` with a `--repeat` flag, or  
- create a new lightweight script:

  - `days/day-010-network-latency-and-endpoint/network_latency_bench.py`

that:

- accepts `--concurrency` (default 1) and `--n` (default 32),  
- sends N requests using a thread pool or simple loop (for 1–4 concurrency, threads are fine),  
- prints a JSON summary (`mode`, `concurrency`, `median_wall_s`, `p95_wall_s`, `n`).

Keep it under ~25 lines if possible; you don’t need a full load generator yet.

---

### 1) Run at small concurrency levels

Run at:

- `concurrency=1`, `n=32` (baseline),  
- `concurrency=4`, `n=32` (light multi-request case),  
- optionally `concurrency=8` if it’s trivial.

Append results to:

- `network_latency_bench.md` (table),  
- and optionally `network_latency_bench.csv`.

Example table:

```text
mode,concurrency,n,median_wall_s,p95_wall_s,notes
baseline,1,32,,,,
baseline,4,32,,,,
baseline,8,32,,,,
```

---

### 2) Correlate with TTFT (Day 007)

In `network_latency_bench.md`, add a short **“TTFT vs HTTP latency”** section:

- Compare your Day 007 warm TTFT (per request) to the HTTP wall-time numbers at concurrency 1.  
- Answer:
  - Is HTTP/network overhead negligible (e.g., a few ms on top of TTFT)?  
  - Or is there a non-trivial gap (e.g., framework overhead, JSON encode/decode, HTTP stack)?  
- Note whether small concurrency (4–8) changes wall-time significantly for the same prompt.

Try to distill a 1–2-sentence rule of thumb, e.g.:

> “On this node, HTTP overhead is ~X ms on top of warm TTFT; meaningful latency changes will mostly come from model/runtime tuning, not network.”

---

### Expected Artifact

- `days/day-010-network-latency-and-endpoint/network_latency_bench.py` (or extended probe script)  
- Updated `network_latency_bench.md` (and optionally `.csv`) with entries for concurrency 1–4(–8) and a TTFT vs HTTP comparison section.

