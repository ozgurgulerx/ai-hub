# Day 011 – Network Tuning: MTU, IRQ Affinity & Backlog

**Phase:** 0 – OS & GPU Setup (Days 1–15)  
**Theme:** Take your Day 010 HTTP baseline and add **OS-level network tuning**: `somaxconn`, MTU/jumbo frames, and IRQ affinity — plus before/after measurements where they actually matter.

**Layers**

- **Hardware / OS** → NIC configuration, MTU, IRQ mapping, TCP backlog  
- **Runtime (vLLM)** → HTTP endpoint behavior under modest load with tuned vs default network settings  
- **Product / SLO** → what you’d be comfortable changing on a real inference node, and what effect you expect

---

## Snapshot (Today’s Focus)

By Day 010 you have:

- A baseline view of **HTTP p50/p95 latency** to your vLLM SLM endpoint at low concurrency.  
- TTFT and runtime decomposition (Days 006–007), plus storage/cold-start behavior (Days 008–009).

Day 011 is about **network tuning knobs**, not theory:

- Inspect current `somaxconn`, MTU, and NIC IRQ mapping.  
- (Optionally, if you own the node) apply sane tuning: `net.core.somaxconn=65535`, MTU 9000 on relevant interfaces, IRQ affinity for the NIC.  
- Reuse Day 010’s HTTP bench to see if anything moves at small/moderate concurrency.

Assumptions:

- You have permission to **inspect** system network configuration.  
- Applying tuning (`sysctl`, `ip link`, IRQ affinity) may require root; you can still structure the experiments and notes even if you don’t flip the switches today.

---

## Tier Breakdown

| Tier  | Time        | Scope |
|------:|------------:|-------|
| Tier 1| ~60–90 min  | Inspect & (optionally) set `net.core.somaxconn`; compare HTTP behavior before/after under modest concurrency |
| Tier 2| ~75–120 min | Inspect MTU, test jumbo frames, and reason about when they matter for vLLM traffic |
| Tier 3| ~60–90 min  | Map NIC IRQs, sketch an affinity plan, and fold all three knobs into a network-tuning SLO story |

---

## Navigation

- **[Tier 1 – Backlog Knob (`somaxconn`) + HTTP Bench](./LOG_tier01.md)**  
- **[Tier 2 – MTU / Jumbo Frames Introspection & Ping Tests](./LOG_tier02.md)**  
- **[Tier 3 – NIC IRQ Affinity & Network Tuning Story](./LOG_tier03.md)**

---

## Cross-Day Context

- **Day 010 – Network Path & vLLM HTTP Latency**: gave you HTTP p50/p95 baseline at low concurrency.  
- **Earlier days**: TTFT, storage, and capacity behaviors are now reasonably well understood.

Day 011 closes the Phase 0 networking loop:

- It doesn’t aim for dramatic perf wins on localhost, but for **measured, documented** defaults and a clear view of **what you’d tune on a real inference node**.

---

## Logging Template (Day 011)

Use this at the end of the day to summarize.

```markdown
# Day 011 – Network Tuning: MTU, IRQ Affinity & Backlog

## Environment
- GPU:
- OS / kernel:
- NIC(s) and relevant interfaces:
- vLLM version:
- Endpoint tested:

## Commands Run
- sysctl / ip / ethtool / /proc/interrupts commands
- HTTP bench runs before/after tuning

## Key Numbers
- net.core.somaxconn before/after:
- MTU on relevant interfaces:
- Any HTTP p50/p95 changes at concurrency 4–8:

## Artifacts Created/Updated
- day-011-network-tuning-and-irq/network_tuning_bench.md
- day-011-network-tuning-and-irq/capture_network_config.sh

## Observations / Surprises
- Did `somaxconn` or MTU changes move HTTP latency or error behavior in your small benches?
- Are there any “never do this in prod” notes (e.g. MTU mismatch gotchas)?
- How confident do you feel about recommending a network-tuning baseline for vLLM nodes?
```

