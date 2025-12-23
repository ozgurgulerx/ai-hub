# Day 009 – Storage Paths: NVMe vs Network & Staging

**Phase:** 0 – OS & GPU Setup (Days 1–15)  
**Theme:** Go from “model files live somewhere” to a **measured storage strategy**: NVMe vs (future) network paths, simple staging patterns, and how they impact cold-start latency and SLOs.

**Layers**

- **Hardware / OS** → NVMe vs network-backed volumes, basic storage topology  
- **Runtime (vLLM)** → model load path under different storage layouts  
- **Product / SLO** → when to stage models to local NVMe vs read from network directly

---

## Snapshot (Today’s Focus)

By Day 008 you have:

- Measured cold vs warm model load times from a local NVMe path for your SLM.  
- Built a simple page-cache pre-warm script and captured how much it helps.  
- Clarified the storage slice of the cold-start stack (page cache vs HBM).

Day 009 is about **storage layout decisions**:

- How bad is it (or would it be) to run models directly from a network-backed path?  
- When is it worth **staging weights to local NVMe** before starting vLLM?  
- How would you explain that trade-off to an SRE or platform team?

Assumptions:

- You have at least one **fast local NVMe mount**.  
- You either have:
  - a real network-backed path (NFS/EFS/SMB/FUSE) where models could live, **or**  
  - you can treat a second, “slower” path as a stand-in and at least design the experiment.

---

## Tier Breakdown

| Tier  | Time        | Scope |
|------:|------------:|-------|
| Tier 1| ~60–90 min  | Compare cold model load from NVMe vs a “network-like” path |
| Tier 2| ~75–120 min | Add a **staging script**: copy from network → NVMe, then start vLLM |
| Tier 3| ~60–90 min  | Turn results into a storage layout + bootstrap recommendation |

---

## Navigation

- **[Tier 1 – NVMe vs Network Path Model Load](./LOG_tier01.md)**  
- **[Tier 2 – Staging Script: Network → NVMe → vLLM](./LOG_tier02.md)**  
- **[Tier 3 – Storage Layout & Bootstrap Story](./LOG_tier03.md)**

---

## Cross-Day Context

- **Day 006 – SLM + OS Memory & vLLM Path**: introduced SLM as an OS/runtime probe, and page cache vs HBM.  
- **Day 007 – Runtime Probes**: mapped TTFT, KV scaling, and batching behavior as capacity knobs.  
- **Day 008 – Storage & Cold Starts**: quantified cold vs warm model load from NVMe and pre-warm strategies.

Day 009 extends the storage story from **“how fast?”** to **“where should models live?”**:

- Putting weights solely on a network path may simplify deployment but hurt cold-start behavior.  
- Staging models to local NVMe introduces extra steps but can de-risk cold starts and network jitter.

---

## Logging Template (Day 009)

Use this at the end of the day to summarize.

```markdown
# Day 009 – Storage Paths: NVMe vs Network & Staging

## Environment
- GPU:
- OS / kernel:
- Storage layout (NVMe mount, any network mounts):
- vLLM version:
- Model (SLM):

## Commands Run
- Storage comparison scripts
- Any staging / copy commands

## Key Numbers
- Cold load time from NVMe:
- Cold load time from network-like path:
- Staging time (network → NVMe):
- Load time from staged path:

## Artifacts Created/Updated
- day-009-storage-nvme-vs-network/compare_storage_paths.sh
- day-009-storage-nvme-vs-network/storage_layout_bench.csv
- day-009-storage-nvme-vs-network/storage_layout_bench.md
- day-009-storage-nvme-vs-network/stage_model_to_nvme.sh

## Observations / Surprises
- Is network-backed load viable for this model/GPU combo?
- When does staging to NVMe look worth it?
- How would you encode these findings into a node/bootstrap script?
```

