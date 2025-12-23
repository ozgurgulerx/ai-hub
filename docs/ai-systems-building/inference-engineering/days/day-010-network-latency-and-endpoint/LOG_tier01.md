# Day 010 – Network Path & vLLM HTTP Latency
## Tier 1 – HTTP Latency Baseline (Local vLLM Endpoint)

> **Goal**: Measure baseline HTTP p50/p95 latency to your vLLM SLM endpoint at low concurrency and record how it compares to TTFT.
>
> **Outcome**: A small markdown note + CSV that quantify HTTP overhead vs model compute on this node.

---

## Tier 1 – Must Do (Core Block)

**Title** – HTTP Latency Baseline (Local vLLM Endpoint)  
**Time Budget** – ~60–90 min

---

### 0) Confirm the endpoint and SLM

Reuse your Day 007 SLM and vLLM config:

- Endpoint: `http://127.0.0.1:8000/v1/completions` (or your current host:port).  
- Model: same SLM as in Day 007/008 (e.g. `microsoft/Phi-3-mini-4k-instruct`).

Make sure:

- vLLM server is running with a known launch command (keep a copy in your notes).  
- You can successfully run a single `curl` or `ttft_probe.py` call.

---

### 1) Create a minimal HTTP latency probe script

Create:

- `days/day-010-network-latency-and-endpoint/http_latency_probe.py`

Purpose:

- Send a single OpenAI-compatible request to your vLLM endpoint.  
- Measure wall time (`t0→t_done`) and optionally time to first byte/token if you want to extend it later.  
- Print a small JSON blob with `wall_s` and maybe `prompt_tokens` / `completion_tokens`.

You can:

- Start from Day 007’s `ttft_probe.py` and simplify it, or  
- Write a fresh ~20-line script that just posts once and prints a JSON line.

Keep the **prompt and parameters fixed**:

- `max_tokens=64`, `temperature=0.0`, same short prompt as Day 007.

---

### 2) Measure p50/p95 latency at concurrency 1

Use a simple loop to run N=20–50 requests at concurrency 1:

```bash
for i in $(seq 1 30); do
  python days/day-010-network-latency-and-endpoint/http_latency_probe.py >> /tmp/http_latency_raw.jsonl
done
```

Then, either:

- parse `/tmp/http_latency_raw.jsonl` with a quick one-liner (Python, jq) to compute p50/p95, **or**  
- copy a few samples into `network_latency_bench.md` and do rough stats manually.

Goal:

- capture p50/p95 HTTP wall-time numbers at concurrency 1.  
- note how they compare to warm TTFT estimates from Day 007.

---

### 3) Record results in markdown

Create:

- `days/day-010-network-latency-and-endpoint/network_latency_bench.md`

Include:

- Environment summary (GPU, OS, endpoint, SLM).  
- A small table like:

```text
mode,concurrency,n,median_wall_s,p95_wall_s,notes
baseline,1,30,,,,
```

- 3–5 sentences interpreting:
  - How large HTTP/network overhead seems vs TTFT+decode on this node.  
  - Whether variance is small or you see occasional tail spikes even at concurrency 1.

If desired, also create:

- `days/day-010-network-latency-and-endpoint/network_latency_bench.csv`

With header:

```text
mode,concurrency,run_id,wall_s,notes
```

and fill it from your raw runs.

---

### Expected Artifact

- `days/day-010-network-latency-and-endpoint/http_latency_probe.py`  
- `days/day-010-network-latency-and-endpoint/network_latency_bench.md`  
- (Optional) `days/day-010-network-latency-and-endpoint/network_latency_bench.csv`

