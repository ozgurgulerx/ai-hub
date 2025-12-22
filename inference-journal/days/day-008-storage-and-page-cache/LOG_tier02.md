# Day 008 – Storage & Cold Starts
## Tier 2 – Page Cache Pre-Warm & I/O Scheduler

> **Goal**: Add a minimal **page-cache pre-warm script** and sanity-check the NVMe I/O scheduler, so you can control cold-start behavior instead of guessing.
>
> **Outcome**: A pre-warm script + notes on what changed (or didn’t) in your load timings and `storage_load_bench.md`.

---

## Tier 2 – Deepen (If Time/Energy Allow)

**Title** – Page Cache Pre-Warm & NVMe I/O Scheduler  
**Time Budget** – ~75–120 min

---

### 0) Inspect current storage layout & scheduler

Quick probes:

- `lsblk -o NAME,TYPE,MOUNTPOINT`  
- `cat /sys/block/nvme0n1/queue/scheduler` (adjust device as needed)

Record:

- Which device holds your model weights? (e.g., `/dev/nvme0n1`.)  
- Which scheduler is in use (`none`, `mq-deadline`, etc.)?

If you’re not comfortable changing schedulers on this node, just record the current value and leave it at that.

---

### 1) Add a page-cache pre-warm script

Create:

- `days/day-008-storage-and-page-cache/prewarm_page_cache.sh`

Purpose:

- Touch the model weight files in a controlled way so Linux’s page cache is filled before you launch vLLM.

Skeleton steps:

1. Accept `MODEL_PATH` as env/arg.  
2. Use a safe traversal (e.g., `find "$MODEL_PATH" -type f -name '*.bin' -o -name '*.safetensors'`) and read a small amount from each file (`head -c` or similar).  
3. Optionally measure pre-warm time (`time` or shell timing).

Document in the script header that it **assumes a local NVMe-backed path** and that it should not be used blindly on shared systems.

---

### 2) Re-run load timings with pre-warm

Procedure:

1. Drop caches only if safe (`echo 3 > /proc/sys/vm/drop_caches` as root; otherwise, simulate by rebooting once and then using only pre-warm afterwards).  
2. Run `prewarm_page_cache.sh` on your SLM’s `MODEL_PATH`.  
3. Immediately run `measure_model_load.sh` again and record a new `mode` (e.g., `prewarm_cold`, `prewarm_warm`).

Update `storage_load_bench.csv` and add a new section to `storage_load_bench.md` for “pre-warm vs no pre-warm.”

Questions to answer:

- Did pre-warm meaningfully reduce cold load time?  
- How big is the pre-warm overhead itself vs the saved time on first request?  
- From a product/SRE point of view, is that trade-off worth it?

---

### 3) Optional: Experiment with I/O scheduler (only if safe)

If you own this node and understand the risk:

1. Note current scheduler: `cat /sys/block/nvme0n1/queue/scheduler`.  
2. Temporarily set to `none` (or back to previous) and re-run one or two cold/warm runs, noting any change in variance or throughput.

If not safe or allowed on this box, just document what you *would* test on a dedicated lab node.

---

### Expected Artifact

- `days/day-008-storage-and-page-cache/prewarm_page_cache.sh`  
- Updated `days/day-008-storage-and-page-cache/storage_load_bench.csv`  
- Updated `days/day-008-storage-and-page-cache/storage_load_bench.md` with a “pre-warm vs no pre-warm” section and a short conclusion.

