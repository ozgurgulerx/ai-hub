# Day 008 – Storage, Page Cache, and Cold Starts

**Phase:** 0 – OS & GPU Setup (Days 1–15)  
**Theme:** Turn “storage is fast enough” into **measured cold-start behavior**: NVMe vs (future) network, page cache, pre-warm scripts, and what they do to TTFT and startup latency.

**Layers**

- **Hardware / OS** → NVMe vs network path, I/O scheduler, page cache behavior  
- **Runtime (vLLM)** → cold-start model load, interaction with page cache & hugepages  
- **Product / SLO** → how often you can afford cold starts, and how much you should invest in pre-warm strategies

---

## Snapshot (Today’s Focus)

By Day 7 you’ve:

- Brought up a GPU node with basic OS tuning, NUMA awareness, and THP/hugepages configured.  
- Built an SLM-based probe and measured TTFT, prefix caching, KV scaling, and batching regimes for vLLM.

Day 008 is about **making storage + page cache behavior explicit**:

- How long does a cold model load actually take on this GPU + NVMe box?  
- How much does the **Linux page cache** change second/third model loads?  
- What would a simple **pre-warm script** look like, and how much does it buy you?

Assumptions:

- You have at least one local NVMe mount for model weights.  
- vLLM + your SLM from Day 006/007 still run correctly on this node.

---

## Tier Breakdown

| Tier  | Time        | Scope |
|------:|------------:|-------|
| Tier 1| ~60–90 min  | Measure cold vs warm model load from NVMe and record page-cache effects |
| Tier 2| ~75–120 min | Add a page-cache pre-warm script + I/O scheduler sanity check |
| Tier 3| ~60–90 min  | Tie storage results into a cold-start SLO story (how often, how bad, how to hide it) |

---

## Navigation

- **[Tier 1 – NVMe Cold/Warm Model Load Probe](./LOG_tier01.md)**  
- **[Tier 2 – Page Cache Pre-Warm & I/O Scheduler](./LOG_tier02.md)**  
- **[Tier 3 – Cold-Start SLOs & Capacity Story](./LOG_tier03.md)**

---

## Cross-Day Context

- **Day 003 – vLLM Capacity & OOM**: introduced capacity grids and benchmarks.  
- **Day 006 – SLM + OS Memory & vLLM Path**: established SLM as an OS/runtime probe, and clarified page cache vs HBM.  
- **Day 007 – TTFT, Prefix Caching, KV Scaling**: mapped the runtime-level latency stack (weights, runtime warm-up, KV allocations, batching).

Day 008 focuses on the **storage + page cache slice** of that stack:

- “How long does it take to get weights into page cache and HBM the first time?”  
- “How much can I reduce that cost with a simple pre-warm script?”  
- “What cold-start penalty should I expect in prod, and how do I budget for it?”

---

## Logging Template (Day 008)

Use this at the end of the day to summarize.

```markdown
# Day 008 – Storage & Cold Starts

## Environment
- GPU:
- OS / kernel:
- Storage layout (NVMe vs network):
- vLLM version:
- Model (SLM):

## Commands Run
- Model load timing scripts
- Any I/O scheduler / page cache commands

## Key Numbers
- Cold model load time (NVMe):
- Warm model load time (after page cache warm):
- Estimated page cache pre-warm time:
- Any observed differences after scheduler tweaks:

## Artifacts Created/Updated
- days/day-008-storage-and-page-cache/measure_model_load.sh
- days/day-008-storage-and-page-cache/storage_load_bench.md
- days/day-008-storage-and-page-cache/storage_load_bench.csv

## Observations / Surprises
- Did cold-start load time match your expectations from Day 006/007 TTFT decompositions?
- How much did page cache change second/third loads?
- Would you invest in pre-warm on this node for a real product?
```

