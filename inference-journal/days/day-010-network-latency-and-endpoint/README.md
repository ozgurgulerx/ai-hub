# Day 010 – Network Path & vLLM HTTP Latency

**Phase:** 0 – OS & GPU Setup (Days 1–15)  
**Theme:** Move from “localhost is fast” to a **measured network + HTTP baseline** for your vLLM endpoint: RTT, HTTP p50/p95, and how they relate to TTFT and cold-start work.

**Layers**

- **Hardware / OS** → basic NIC + TCP stack behavior (no risky tuning yet)  
- **Runtime (vLLM)** → OpenAI-compatible HTTP endpoint behavior under low concurrency  
- **Product / SLO** → how much of user-visible latency is network vs runtime on this node

---

## Snapshot (Today’s Focus)

By Day 009 you have:

- A good handle on **storage** and cold-start from NVMe vs network-like paths.  
- A detailed decomposition of **TTFT** into weights, runtime, KV alloc, and scheduling.  
- Capacity intuition around **KV + concurrency** and batching.

Day 010 is about getting a **clean network + HTTP baseline**:

- What do p50/p95 HTTP latencies to your vLLM endpoint look like at low concurrency?  
- How much of that is **network/HTTP overhead** vs model compute?  
- What simple signals (ping, curl, small probe script) would you watch in prod?

Assumptions:

- vLLM SLM server (Day 007 config) is reachable on `localhost:8000` or a known host:port.  
- You can run basic CLI networking tools (`ping`, `curl`) on this node.

---

## Tier Breakdown

| Tier  | Time        | Scope |
|------:|------------:|-------|
| Tier 1| ~60–90 min  | Measure baseline HTTP latency (p50/p95) to the vLLM endpoint |
| Tier 2| ~75–120 min | Add a simple **network latency bench script** and relate it to TTFT numbers |
| Tier 3| ~60–90 min  | Turn the numbers into a first-cut network/endpoint SLO story |

---

## Navigation

- **[Tier 1 – HTTP Latency Baseline (Local vLLM Endpoint)](./LOG_tier01.md)**  
- **[Tier 2 – Network Latency Bench & Correlation to TTFT](./LOG_tier02.md)**  
- **[Tier 3 – Endpoint SLO & “What to Watch” Story](./LOG_tier03.md)**

---

## Cross-Day Context

- **Day 006 – SLM + OS Memory & vLLM Path**: gave you TTFT decomposition and OS-level probes.  
- **Day 007 – Runtime Probes**: added detailed TTFT, KV, and batching capacity math.  
- **Days 008–009 – Storage**: covered cold-start from NVMe vs network-like paths and staging patterns.

Day 010 counts the **wire + HTTP stack** as another part of the latency budget:

- Even on a single node, you want to know whether **network/HTTP overhead** is negligible or meaningful compared to TTFT and decode.  
- Later, this sets you up for **multi-node** and **external client** measurements in Phase 1.

---

## Logging Template (Day 010)

Use this at the end of the day to summarize.

```markdown
# Day 010 – Network Path & vLLM HTTP Latency

## Environment
- GPU:
- OS / kernel:
- NIC(s) and relevant interface:
- vLLM version:
- Endpoint tested (host:port):

## Commands Run
- ping / curl invocations
- http_latency_probe.py / network bench commands

## Key Numbers
- ping RTT stats (min/avg/max) for relevant host:
- HTTP p50 / p95 latency at concurrency 1:
- HTTP p50 / p95 latency at small concurrency (e.g. 4–8):

## Artifacts Created/Updated
- day-010-network-latency-and-endpoint/http_latency_probe.py
- day-010-network-latency-and-endpoint/network_latency_bench.csv
- day-010-network-latency-and-endpoint/network_latency_bench.md

## Observations / Surprises
- How big is HTTP/network overhead vs TTFT on this node?
- Any obvious variance or tails even at low concurrency?
- Which metrics would you watch in prod to catch network issues vs runtime issues?
```

