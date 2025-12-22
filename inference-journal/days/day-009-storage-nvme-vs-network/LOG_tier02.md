# Day 009 – Storage Paths: NVMe vs Network & Staging
## Tier 2 – Staging Script: Network → NVMe → vLLM

> **Goal**: Prototype a **staging pattern**: copy model weights from a network-like path to local NVMe, then start vLLM from NVMe and compare end-to-end “ready” times.
>
> **Outcome**: A small staging script + benchmark rows that show whether staging is worth it on this node.

---

## Tier 2 – Deepen (If Time/Energy Allow)

**Title** – Staging Script: Network → NVMe → vLLM  
**Time Budget** – ~75–120 min

---

### 0) Decide on a staging directory

Pick:

- `STAGING_ROOT` – a local NVMe-backed directory for staged models, e.g. `/mnt/nvme0/staged_models`.

Ensure:

- There is enough free space for at least one copy of your SLM.  
- You’re comfortable cleaning it up afterward (this is scratch space).

---

### 1) Create a staging script

Create:

- `days/day-009-storage-nvme-vs-network/stage_model_to_nvme.sh`

Purpose:

- Copy or `rsync` weights from `MODEL_PATH_NET` → `STAGING_ROOT/MODEL_NAME`,  
- Optionally verify file count / size,  
- Then launch vLLM pointing at the staged path and measure time-to-ready.

High-level steps:

1. Accept `MODEL_PATH_NET`, `STAGING_ROOT`, and maybe `MODEL_NAME` as env/args.  
2. `t_copy_start = now`; run `rsync` or `cp -a` from net → staging; `t_copy_end = now`.  
3. Launch vLLM using `STAGING_ROOT/MODEL_NAME` and reuse the timing logic from Day 008/009 Tier 1 to measure `load_s_staged`.  
4. Append a row to `storage_layout_bench.csv` with `storage_mode=staged` and an extra note (e.g., “copy_s=..., load_s=...”).

Keep the script simple and well-commented; you don’t need to handle every edge case yet.

---

### 2) Compare three modes: nvme, net, staged

Using `storage_layout_bench.csv`, ensure you have rows for:

- `storage_mode=nvme` (direct NVMe load),  
- `storage_mode=net` (direct network-like load),  
- `storage_mode=staged` (copy from net → NVMe, then load from NVMe).

In `storage_layout_bench.md`, add a small comparison table or bullets that summarize:

- Cold load from NVMe vs network vs staged (net+copy+load).  
- Whether staging:
  - reduces total time-to-ready vs direct network load, and  
  - by how much.

Interpretation prompts:

- If staging is slower overall but gives **more predictable** runtime behavior, is that worth it?  
- If staging is faster (e.g., fast local NVMe vs slow network), how much faster? Enough to justify extra complexity?

---

### Expected Artifact

- `days/day-009-storage-nvme-vs-network/stage_model_to_nvme.sh`  
- Updated `storage_layout_bench.csv` and `storage_layout_bench.md` with `staged` mode and a short discussion of when staging makes sense.

