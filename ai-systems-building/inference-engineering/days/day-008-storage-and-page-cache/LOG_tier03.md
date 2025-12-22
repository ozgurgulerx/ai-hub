# Day 008 – Storage & Cold Starts
## Tier 3 – Cold-Start SLOs & Capacity Story

> **Goal**: Turn your storage measurements into a **cold-start SLO story**: how often cold starts happen, how bad they are, and what mitigation you recommend.
>
> **Outcome**: A short, consulting-ready note that you can reuse when advising teams on cold-start behavior for vLLM-based services.

---

## Tier 3 – Stretch (Optional / Ambitious)

**Title** – Cold-Start SLOs & Capacity Story  
**Time Budget** – ~60–90 min

---

### 0) Summarize the cold-path stack (Day 006–008)

In a short section of `storage_load_bench.md` (or a new `cold_start_slo_notes.md`), summarize:

- Storage → RAM (page cache fill).  
- RAM → HBM (weights into GPU).  
- Runtime warm-up (CUDA graphs, allocator, KV/buffer allocations).  
- First prefill + scheduling.

Use your Day 006/007 notes plus Day 008 storage numbers to assign rough time-slices (e.g., “~X s page cache fill, ~Y s runtime warm-up”).

---

### 1) Draft a first-cut cold-start SLO for a single node

Assume:

- A single-GPU vLLM SLM service (your SLM of choice).  
- A simple deploy model (rolling restarts, occasional reboots).

Write 4–6 bullets answering:

- How long a cold start takes on this node (best/typical/worst from your samples).  
- How often you expect cold starts (deploys, node rotations, rare crashes).  
- Whether you recommend:
  - pre-warming model weights on deploy,  
  - keeping a minimum pool of warm replicas,  
  - or accepting cold-start spikes as rare but tolerable.

Try to phrase it in language you’d use with an SRE or PM (“In practice, you’ll see one slow request (~X s) after each deploy per node; we can hide it by…”).

---

### 2) Connect storage behavior to concurrency & capacity

Using your Tier 3 concurrency results (Day 007 Tier 3) plus Day 008 load timings:

- Explain how **storage + page cache** affect:
  - the very first requests after a restart (cold TTFT path),  
  - how quickly the system reaches its steady-state concurrency regime.  
- Note whether cold starts meaningfully change your capacity envelope (e.g., “cold load uses only ~Y% extra VRAM but takes X s; once loaded, capacity is as per Tier 3”).

Optional: sketch a **small table** like:

```text
phase,description,typical_duration_s,notes
cold_load,weights + page cache fill,,
runtime_warmup,cuda graphs + alloc,,
steady_state,normal TTFT at target concurrency,,
```

---

### 3) Capture “what I’d do in prod” as 3 bullets

End the day by writing **three concrete recommendations** you’d give a team about storage & cold starts, for this GPU + model class, e.g.:

- “On this node, always pre-warm the SLM on deploy to avoid a 10–15 s cold request.”  
- “Avoid putting this service behind a cold autoscaler; use minimum N warm replicas instead.”  
- “If you must cold-start on demand, use a small SLM probe to hide cold path from user-facing traffic.”

Keep it short, opinionated, and tied directly to your numbers.

---

### Expected Artifact

- Updated `days/day-008-storage-and-page-cache/storage_load_bench.md` (or new `cold_start_slo_notes.md`) with:
  - cold-path breakdown,  
  - first-cut cold-start SLO,  
  - 3 production recommendations.

