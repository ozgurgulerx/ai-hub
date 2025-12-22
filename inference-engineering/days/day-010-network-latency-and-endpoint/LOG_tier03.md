# Day 010 – Network Path & vLLM HTTP Latency
## Tier 3 – Endpoint SLO & “What to Watch” Story

> **Goal**: Turn your HTTP/network measurements into a **first-cut endpoint SLO story** and a list of metrics you’d watch to separate network issues from runtime issues.
>
> **Outcome**: A short, consulting-ready note that describes expected HTTP latency behavior for this node and SLM, and how you’d monitor it.

---

## Tier 3 – Stretch (Optional / Ambitious)

**Title** – Endpoint SLO & “What to Watch” Story  
**Time Budget** – ~60–90 min

---

### 0) Draft an endpoint-level SLO for this node

In `network_latency_bench.md` (or a new `endpoint_slo_notes.md`), add:

- A simple SLO-style statement for the SLM endpoint on this node, e.g.:

  - “For this SLM on localhost, p95 HTTP latency for a 64-token generation should be ≤ X ms under concurrency ≤ 4.”

- A short justification rooted in your numbers (Day 007 TTFT + Day 010 HTTP).

---

### 1) List metrics / dashboards you’d want

Write 4–6 bullets describing **what you’d monitor** to distinguish:

- network issues vs runtime issues vs overload.

For example:

- HTTP p95 / p99 latency per endpoint.  
- TTFT vs E2E breakdown if you can instrument it.  
- Basic network metrics (RTT, retransmits, NIC errors).  
- GPU utilization and queue lengths (from Day 007 Tier 3) to correlate runtime load.

Keep it concrete: names of metrics, not just vague “monitor the network.”

---

### 2) Tie it back to Phase 0 + future work

Add a short section:

- How these Day 010 numbers will help when you:
  - enable jumbo frames / IRQ affinity / `somaxconn` in Day 011+,  
  - move from localhost to **over-the-network** clients in Phase 1.  
- One or two hypotheses you could test later:
  - e.g., “Changing MTU or IRQ affinity should not change localhost HTTP latency much, but will matter when we go cross-rack.”

This keeps Day 010 tight while still pointing at future networking experiments.

---

### 3) Three bullets you’d tell an SRE

End with three opinionated bullets such as:

- “On this node, HTTP overhead is ~X ms; most latency variance will come from TTFT and batching, not the network stack.”  
- “At concurrency up to 4–8, HTTP p95 stays within Y%; beyond that we should look at Tier 3 batching data before raising network alarms.”  
- “Network metrics are still critical in prod, but for this SLM node, they’re mostly about catching rare spikes or misconfigurations, not everyday latency tuning.”

---

### Expected Artifact

- Updated `network_latency_bench.md` (or new `endpoint_slo_notes.md`) with:
  - an endpoint-level SLO statement,  
  - metrics to watch,  
  - 2–3 hypotheses for future networking work,  
  - three SRE-facing bullets.

